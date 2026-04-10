# RandomForest 분류 알고리즘
# 랜덤 포레스트(Random Forest)는 수많은 의사결정 나무(Decision Tree)를 생성하고, 
# 이들의 예측 결과를 다수결(분류)이나 평균(회귀)으로 종합하여 정확도를 높이는 대표적인 앙상블 학습 알고리즘입니다. 
# 데이터 무작위 샘플링(Bagging)과 피처 배깅을 통해 과적합을 방지하고 이상치에 강한 장점이 있습니다. 
# 앙상블 기법 중 배깅(Bagging. Bootstrap, Aggregation)
# : 복수의 샘플 데이터와 DisisionTree를 학습시키고 결과를 집계
# 참고 : 우수한 성능은 Bootsting, 과적합이 걱정된다면 Bagging

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import accuracy_score

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/titanic_data.csv")
print(df.head(2))
print(df.info())
print(df.isnull().any())
df = df.dropna(subset=['Pclass','Age','Sex'])
print(df.shape) # (714, 12)

df_x = df[['Pclass','Age','Sex']]  # 독립변수(feature)
print(df_x.head(3))

# 전처리 성별 열 : Label Encoding(문자범주형 -> 정수형)
from sklearn.preprocessing import LabelEncoder
encoder = LabelEncoder()
df_x.loc[:,'Sex'] = encoder.fit_transform(df_x['Sex'])  # feature
print(df_x.head(3)) # [ 0 : female, 1 : male]

df_y = df['Survived']  # 종속변수(label)
print(df_y.head(3))  # [ 0 : 사망, 1 : 생존]

print()
print('데이터 분리 : 학습용(train data), 검증용(test data) ----')
train_x, test_x, train_y, test_y = train_test_split(df_x, df_y, test_size=0.3, random_state=12)
print(train_x.shape) # (499, 3)
print(test_x.shape) # (215, 3)
print(train_y.shape) # (499,)
print(test_y.shape) # (215,)

print('\n분류 모델 생성 ----')
model = RandomForestClassifier(criterion='gini', n_estimators=500, random_state=12)
# n_estimators : 결정트리 수
model.fit(train_x, train_y)
pred = model.predict(test_x)

print('예측값 : ', pred[:5])
# 예측값 :  [1 0 0 0 0]
print('실제값 : ', np.array(test_y[:5]))
# 실제값 :  [1 0 0 0 1]
print(f"총 갯수: {len(test_y)}, 오류수: {(test_y != pred).sum()}")
# 총 갯수: 215, 오류수: 37
print('전체 대비 맞춘 비율 : ', (len(test_y) - (test_y != pred).sum()) / len(test_y))
# 전체 대비 맞춘 비율 :  0.827906976744186
print('분류 정확도 : ', accuracy_score(test_y, pred))
# 분류 정확도 :  0.827906976744186

# 교차검증 (K-Fold)
cross_vali = cross_val_score(model, df_x, df_y, cv=5)
print(cross_vali)
# [0.75524476 0.8041958  0.81818182 0.83216783 0.83098592]
print('교차 검증 평균 정확도 : ', np.round(np.mean(cross_vali), 5))
# 교차 검증 평균 정확도 :  0.80816

print('\n 중요 변수 확인----')
print('특성(변수) 중요도 : ', model.feature_importances_) # [0.16172779 0.49842824 0.33984396]
# model.feature_importances_  : 각 특성이 예측에 기여한 정도(중요도)를 수치로 표현
# 값의 합은 1.0, 수치가 클수록 해당 변수가 불순도 감소에 더 많이 기여함.

# 시각화
import matplotlib.pyplot as plt
n_features = df_x.shape[1]
plt.barh(range(n_features), model.feature_importances_, align='center')
plt.xlabel('Feature importance Score')
plt.ylabel('Features')
plt.yticks(np.arange(n_features), df_x.columns)
plt.ylim(-1, n_features)
plt.show()

print()
# 전체 변수 대상으로 중요도 확인
# Name, Ticket, Cabin : 문자형 - 바로 사용 불가 (Encoding 필요)
# PassengerId, Name : Survived와 관련 없는 변수

df_x2 = df[['Pclass', 'Age', 'Sex', 'Fare', 'SibSp', 'Parch']]

df_x2.loc[:, 'Sex'] = encoder.fit_transform(df_x2['Sex'])

model2 = RandomForestClassifier(n_estimators=500, random_state=12)
model2.fit(df_x2, df_y)

importances = model2.feature_importances_
feature_df = pd.DataFrame({'feature': df_x2.columns, 'importance': importances})
feature_df = feature_df.sort_values(by='importance', ascending=False)
print('\n전체 변수 대상 중요도:\n', feature_df)
#    feature  importance
# 1     Age    0.290795
# 3    Fare    0.268924
# 2     Sex    0.257513
# 0  Pclass    0.098518
# 4   SibSp    0.047120
# 5   Parch    0.037130

# 시각화 
import seaborn as sns
plt.figure(figsize=(8,5))
sns.barplot(x='importance', y='feature', data=feature_df, orient='h')
plt.xlabel('Feature importance Score')
plt.ylabel('Features')
plt.tight_layout()
plt.show()