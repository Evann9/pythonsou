# Naive Bayes 알고리즘을 이용한 분류 - weather.csv
import pandas as pd
import numpy as np

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv")
print(df.head(2))
print(df.info())

# 전처리 작업 ---
df = df.drop('Date', axis=1)
df['Sunshine'] = df['Sunshine'].fillna(df['Sunshine'].mean())
print(df.isnull().sum())

# 범주형 처리
df['RainToday'] = df['RainToday'].map({'Yes':1, 'No':0})
df['RainTomorrow'] = df['RainTomorrow'].map({'Yes':1, 'No':0})
print(df.head(2))

x = df.drop('RainTomorrow', axis=1) 
y = df['RainTomorrow']

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, stratify=y, random_state=0)

# Naive Bayes 모델 학습
from sklearn.naive_bayes import GaussianNB
model = GaussianNB().fit(x_train, y_train)

# 예측 및 평가
from sklearn.metrics import accuracy_score, confusion_matrix
pred = model.predict(x_test)
print('acc : ', accuracy_score(y_test, pred)) # acc :  0.8108108108108109
print(confusion_matrix(y_test, pred))
# [[52  9]
#  [ 5  8]]

print()
# 교차 검증
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, x, y, cv=5)
print(scores)
print('교차 검증 평균 정확도 : ', np.round(np.mean(scores), 5))   # 0.80896

print()
# feature 중요도 분석
# feature가 정규분포를 따른다는 가정하에 클래스별 평균
mean_0 = model.theta_[0]   # RainTomorrow = 0 (비오는날 평균)
mean_1 = model.theta_[1]   # RainTomorrow = 1 (비 안오는날 평균)

# 각 feature가 '비오는날 vs 비 안오는날'에서 얼마나 차이가 날까?
importance = np.abs(mean_1 - mean_0)

feat_impo = pd.DataFrame({
    'feature': x.columns,
    'importance': importance
}).sort_values(by='importance', ascending=False)
print('feature 중요도 : \n', feat_impo)

# importance에 대한 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
plt.figure()
plt.bar(feat_impo['feature'], feat_impo['importance'])
plt.xlabel('feature')
plt.ylabel('importance(중요도)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print('새로운 자료 예측')
newdata = pd.DataFrame([{
    'MinTemp': 12.3,
    'MaxTemp': 27.0,
    'Rainfall': 0.0,
    'Sunshine': 10.0,
    'WindSpeed': 8.0,
    'Humidity': 40,
    'Pressure': 1005.0,
    'Cloud': 1,
    'Temp': 20.0,
    'RainToday': 0 
}])
new_pred = model.predict(newdata)
print('예측값 : ', '비옴' if new_pred == 1 else '비 안옴')
print('확률은 ', model.predict_proba(newdata))
