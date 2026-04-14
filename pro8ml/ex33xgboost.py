# kaggle의 Santander coustomer satisfaction dataset 사용
# 산탄데르 은행의 고객 만족 여부 분류 처리
# 클래스 (label)명은 target이고 0: 만족, 1: 불만족

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import GridSearchCV
from xgboost import plot_importance
from sklearn.model_selection import train_test_split
import warnings ; warnings.filterwarnings('ignore')

df = pd.read_csv("train_san.csv", encoding='latin-1')
# print(df.head(2))
print(df.shape) # (76020, 371)
print(df.info())  # dtypes: float64(111), int64(260)

# 전체 데이터에서 만족과 불만족의 비율
print(df['TARGET'].value_counts())
# 0(만족)    73012
# 1(불만족)   3008

unsatisfied_cnt = df[df['TARGET'] == 1].TARGET.count()
total_cnt = df.TARGET.count()
print(f"불만족 비율은 {unsatisfied_cnt / total_cnt * 100:.2f}")
# 불만족 비율은 3.96

print(df.describe())  # feature의 분포 확인

# var3 이상치 제거
df['var3'].replace(-999999, 2, inplace=True)
df.drop('ID', axis=1, inplace=True)  # ID는 식별자이므로 제거
print(df.describe())  

# feature / label 분리
x_features = df.iloc[:, :-1]
y_label = df.iloc[:, -1]
print(x_features.shape, y_label.shape)  # (76020, 369) (76020,)

# train / test split
x_train, x_test, y_train, y_test = train_test_split(x_features, y_label, test_size=0.2, random_state=0, stratify=y_label)

print('학습데이터 레이블 값 분포 비율\n', y_train.value_counts() / y_train.count())
print('테스트데이터 레이블 값 분포 비율\n', y_test.value_counts() / y_test.count())

# 모델 생성 및 학습
xgb_clf = XGBClassifier(
    n_estimators=5, 
    eval_metric="auc"
)

# 성능 평가 지표를 auc로 설정하여 학습 (조기 종료 설정)
xgb_clf.fit(x_train, y_train, eval_set=[(x_test, y_test)])
xgb_roc_score = roc_auc_score(y_test, xgb_clf.predict_proba(x_test)[:, 1])
print(f"ROC AUC: {xgb_roc_score:.5f}")  # ROC AUC: 0.81877

pred = xgb_clf.predict(x_test)
print('예측값 : ', pred[:5])
print('실제값 : ', y_test[:5].values)
# 예측값 :  [0 0 0 0 0]
# 실제값 :  [0 0 0 0 0]
from sklearn import metrics
print('분류정확도 : ', metrics.accuracy_score(y_test, pred))  # 0.9605

# 하이퍼 파라미터 튜닝 (GridSearchCV) 
params = {
    'max_depth': [5, 7],
    'min_child_weight': [1, 3],
    'colsample_bytree': [0.5, 0.75]
}

gridcv = GridSearchCV(xgb_clf, param_grid=params)
gridcv.fit(x_train, y_train, eval_set=[(x_test, y_test)])

print('GridSearchCV 최적 파라미터:', gridcv.best_params_)
xgb_roc_score = roc_auc_score(y_test, gridcv.predict_proba(x_test)[:, 1], average='macro')
# macro : 
# 다중 클래스 분류(Multi-class Classification) 문제에서 
# 각 클래스별 성능 지표(Precision, Recall, F1-score 등)를 개별적으로 계산한 후, 
# 그 값들의 단순 평균을 내는 방식
print(f"GridSearchCV ROC AUC: {xgb_roc_score:.4f}")

print() # 위 파라미터로 모델 생성
xgb_clf2 = XGBClassifier(
    n_estimators=5, 
    random_state=12, 
    max_depth=5, 
    min_child_weight=3, 
    colsample_bytree=0.5
)

xgb_clf2.fit(x_train, y_train, eval_set=[(x_test, y_test)])
xgb_roc_score2 = roc_auc_score(y_test, xgb_clf2.predict_proba(x_test)[:, 1], average='macro')
print(f"ROC AUC: {xgb_roc_score2:.5f}")  # ROC AUC: 0.81231

pred2 = xgb_clf2.predict(x_test)
print('예측값 : ', pred2[:5])
print('실제값 : ', y_test[:5].values)
# 예측값 :  [0 0 0 0 0]
# 실제값 :  [0 0 0 0 0]
print('분류정확도 : ', metrics.accuracy_score(y_test, pred2))  # 0.9604

# 중요 피처 시각화
fig, ax = plt.subplots(1, 1,figsize=(10, 8))
plot_importance(xgb_clf2, ax=ax, max_num_features=20)
plt.show()