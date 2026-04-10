"""
[Randomforest 문제1] 
kaggle.com이 제공하는 'Red Wine quality' 분류 ( 0 - 10)
winequality-red.csv

Input variables (based on physicochemical tests):
    1 - fixed acidity
    2 - volatile acidity
    3 - citric acid
    4 - residual sugar
    5 - chlorides
    6 - free sulfur dioxide
    7 - total sulfur dioxide
    8 - density
    9 - pH
    10 - sulphates
    11 - alcohol

Output variable (based on sensory data):
12 - quality (score between 0 and 10)
"""

import pandas as pd
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.pipeline import Pipeline  # 전처리 + 모델 => 실행
from sklearn.compose import ColumnTransformer  # 칼럼별 전처리를 다르게 적용
from sklearn.impute import SimpleImputer   # 결측치 처리
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score, roc_curve

df = pd.read_csv("winequality-red.csv")
print(df.head(2))
print(df.shape)  # (1596, 12)

x = df.drop('quality', axis=1)  # feature
y = df['quality']
print(x.info())

print('\n데이터 분리')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=100)
print(x_train.shape, x_test.shape)  # (1117, 11) (479, 11)
print(y_train.shape, y_test.shape)  # (1117,) (479,)

# 분류 모델 생성
model = RandomForestClassifier(criterion='entropy', n_estimators=300, random_state=1)
print(model)
model.fit(x_train, y_train)

# 분류 예측
y_pred = model.predict(x_test)
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10].values)
# 예측값 :  [5 6 7 5 5 6 6 6 5 6]
# 실제값 :  [5 6 6 5 4 6 5 6 5 7]
print(f"총 갯수: {len(y_test)}, 오류수: {(y_test != y_pred).sum()}")
print(f"분류 정확도: {accuracy_score(y_test, y_pred)}")
# 총 갯수: 479, 오류수: 161
# 분류 정확도 : 0.6638830897703549

# 교차검증 (K-Fold)
cross_vali = cross_val_score(model, x, y, cv=5)
print(cross_vali)
# [0.525      0.56739812 0.62382445 0.5830721  0.60815047]
print('교차 검증 평균 정확도 : ', np.round(np.mean(cross_vali), 5))
# 교차 검증 평균 정확도 :  0.58149

print('\n 중요 변수 확인----')
print('특성(변수) 중요도 : ', model.feature_importances_) 
# [0.06992165 0.11430742 0.07386071 0.06742068 0.07579101 0.0621615
#  0.09909892 0.09046408 0.0699085  0.1225321  0.15453344]=

# 시각화
import matplotlib.pyplot as plt
n_features = x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align='center')
plt.xlabel('Feature importance Score')
plt.ylabel('Features')
plt.yticks(np.arange(n_features), x.columns)
plt.show()