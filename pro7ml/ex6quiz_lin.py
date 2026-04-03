# 회귀분석 문제 : make_regression 사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy import stats



df = pd.read_csv('ex6quiz.csv')
print(df.head())
print(df.info())

# 결측치 처리 및 이상치 제거
df = df.fillna(df.mean()) # 모든 칼럼의 결측치를 각 칼럼의 평균으로 채움
df = df[df['운동'] <= 10] # 운동 10시간 초과인 행 제거

print('-'*40)
print('문제 1번')

x = df.지상파
y = df.운동
print(x[:3])
# 0    0.9
# 1    1.2
# 2    1.2
print(y[:3])
# 0    4.2
# 1    3.8
# 2    3.5
print('상관계수 : ', np.corrcoef(x,y)[0,1])  # 상관계수 :  -0.8655346605559782

print('-'*60)
# 단순 선형회귀 분석 (인과관계가 있다는 가정하에 진행)
model = stats.linregress(x,y)
print(model)
# linregress_results
# slope = -0.668455
# intercept = 4.709676
print('기울기 : ', model.slope)   # -0.6684550167105406
print('절편 : ', model.intercept) # 4.709676019780582
print('p-value : ', model.pvalue) # 6.347578533142469e-05

plt.scatter(x,y)
plt.plot(x, model.slope * x + model.intercept, c='r')
plt.show()

new_df = pd.DataFrame({'지상파':[5,6,7]})
print('점수예측 : \n', np.polyval([model.slope, model.intercept],new_df))
# 점수예측 : 
#  [[1.36740094]
#  [0.69894592]
#  [0.0304909 ]]

print('-'*40)
print('문제 2번')

x = df.지상파
y = df.종편
print(x[:3])
# 0    0.9
# 1    1.2
# 2    1.2
print(y[:3])
# 0    0.7
# 1    1.0
# 2    1.3
print('상관계수 : ', np.corrcoef(x,y)[0,1])  # 상관계수 : 0.8875299693193012

print('-'*40)
# 단순 선형회귀 분석 (인과관계가 있다는 가정하에 진행)
model = stats.linregress(x,y)
print(model)
# linregress_results
# slope = 0.77268698
# intercept = 0.295163336
print('기울기 : ', model.slope)   # 0.7726869861042756
print('절편 : ', model.intercept) # 0.29516333605064626
print('p-value : ', model.pvalue) # 2.2838747299772628e-05

plt.scatter(x,y)
plt.plot(x, model.slope * x + model.intercept, c='r')
plt.show()

new_df = pd.DataFrame({'지상파':[10,11,12]})
print('점수예측 : \n', np.polyval([model.slope, model.intercept],new_df))
# 점수예측 : 
#  [[8.0220332 ]
#  [8.79472018]
#  [9.56740717]]