# 회귀분석 문제 : LinearRegression 사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.linear_model import LinearRegression

df = pd.read_csv('ex6quiz.csv')
print(df.head())

# 결측치 처리 및 이상치 제거
df = df.fillna(df.mean()) # 모든 칼럼의 결측치를 각 칼럼의 평균으로 채움
df = df[df['운동'] <= 10] # 운동 10시간 초과인 행 제거

print('-'*40)
print('문제 1번')

x = df.지상파
y = df.운동

xx = np.array(x).reshape(-1, 1)
yy = np.array(y)

model = LinearRegression()
fit_model = model.fit(xx,yy)  # 최소 제곱법으로 기울기 절편을 반환
print('기울기(slope) : ', fit_model.coef_)   # 기울기 :  [-0.66845502]
print('절편(bias) : ', fit_model.intercept_) # 절편 :  4.709676019780581

y_newpred = fit_model.predict(np.array([[5],[6],[7]]))
print('예측값 : ', y_newpred) 
# 예측값 :  [1.36740094 0.69894592 0.0304909 ]

print('-'*40)
print('문제 2번')

x = df.지상파
y = df.종편

xx = np.array(x).reshape(-1, 1)
yy = np.array(y)

model = LinearRegression()
fit_model = model.fit(xx,yy)  # 최소 제곱법으로 기울기 절편을 반환
print('기울기(slope) : ', fit_model.coef_)   # 기울기 :  [0.77268699]
print('절편(bias) : ', fit_model.intercept_) # 절편 :  0.29516333605064693

y_newpred = fit_model.predict(np.array([[10],[11],[12]]))
print('예측값 : ', y_newpred) 
# 예측값 :  [8.0220332  8.79472018 9.56740717]