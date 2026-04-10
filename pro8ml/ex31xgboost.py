# XGBoost: Boosting 알고리즘을 구현한 분류/예측 모델
# Boosting은 약한 분류기에 대해 샘플에 일부를 보완해가며 순차적으로 학습해 강한 분류기를 만듦

# brest_cancer dataset
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
# pip install xgboost
# pip install lightgbm
import xgboost as xgb
from lightgbm import LGBMClassifier  # xgboost 보다 성능 우수하나 자료가 적으면 과적합 발생
import lightgbm as lgb

data = load_breast_cancer()
x = pd.DataFrame(data.data, columns=data.feature_names)
y = pd.Series(data.target)
print(x[:3], x.shape)  # (569, 30)
print(y[:3], y.shape)  # (569,)
print('레이블 분포 : ', {name:(y == i).sum() for i,name in enumerate(data.target_names)})
# malignant(악성): 212, benign(양성): 357

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)
print(x_train.shape, x_test.shape)  # (455, 30) (114, 30)

# 모델 1
xgb_clf = xgb.XGBClassifier(
    booster='gbtree', # 'gbtree' : 트리기반  /  'gblinear' : 선형모델
    max_depth=6,    # 개별 결정트리 최대 깊이
    n_estimators=200,  # 약한 분류기의 갯수
    eval_metric = 'logloss',
    random_state=42
)
xgb_clf.fit(x_train, y_train)

# 모델 2
lgb_clf = LGBMClassifier(
    n_estimators=200, 
    random_state=42,
    verbose=-1
)
lgb_clf.fit(x_train, y_train)

pred_xgb = xgb_clf.predict(x_test)
pred_lgb = lgb_clf.predict(x_test)
print(f"xgb acc : {accuracy_score(y_test, pred_xgb):.4f}") # 0.9649
print(f"lgb acc : {accuracy_score(y_test, pred_lgb):.4f}") # 0.9912

# 피처 중요도 : gain 기준으로 통일
booster = xgb_clf.get_booster()
xgb_gain = pd.Series(booster.get_score(importance_type='gain'))

lgb_gain = pd.Series(
    lgb_clf.booster_.feature_importance(importance_type='gain'),
    index=x_train.columns
)
# print(xgb_gain)
# print(lgb_gain)

# xgb_gain / xgb_gain.sum() : 각 피처의 기여도를 비율로 만들기
xgb_gain_pct = 100 * xgb_gain / (xgb_gain.sum() if xgb_gain.sum() != 0 else 1)
lgb_gain_pct = 100 * lgb_gain / (lgb_gain.sum() if lgb_gain.sum() != 0 else 1)

# 사용되지 않은 피처는 0으로 채움
xgb_gain_pct = xgb_gain_pct.reindex(x_train.columns).fillna(0)
lgb_gain_pct = lgb_gain_pct.reindex(x_train.columns).fillna(0)

comp_df = pd.DataFrame({
    'XGBoost (gain %)': xgb_gain_pct,
    'LightGBM (gain %)': lgb_gain_pct
}).sort_values('XGBoost (gain %)', ascending=False)
print(comp_df.head(10))  
# 중요 피처(변수) top 10
#                              XGBoost (gain %)  LightGBM (gain %)
# worst concave points            32.424126          45.738001
# worst perimeter                 28.726392           2.445518
# mean concave points             12.725215          17.430096
# worst area                       6.905697          18.552560
# mean area                        2.890564           0.772640
# mean radius                      2.302999           0.035359
# fractal dimension error          2.125163           0.082650
# perimeter error                  1.894145           0.426760
# worst texture                    1.612025           3.412547
# radius error                     1.452665           0.402968

# 시각화
topk = 5
top = comp_df.head(topk)[::-1]

fig, axes = plt.subplots(1, 2 , figsize=(8, 5))
xmax = float(np.ceil(top.max()).max())  # 두 모델의 최대값

for ax, col in zip(axes, ['XGBoost (gain %)', 'LightGBM (gain %)']):
    ax.barh(top.index, top[col])

    ax.set_title(f"{col.split()[0]} Feature importance")
    ax.set_xlabel('Importance (%)')
    ax.set_xlim(0, xmax)

plt.tight_layout()
plt.show()