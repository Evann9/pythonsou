# 회귀분석 문제 : statsmodels ols()사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from scipy import stats
import statsmodels.formula.api as smf

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
print(x.ndim)  # 1차원
print(y.ndim)  # 1차원

data = np.array([x,y])
df2 = pd.DataFrame(data.T)
df2.columns = ['x','y']
print(df2.head(3))
#      x    y
# 0  0.9  4.2
# 1  1.2  3.8
# 2  1.2  3.5

model = smf.ols(formula="y ~ x",data=df2).fit()
print(model.summary()) 
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                      y   R-squared:                       0.749
# Model:                            OLS   Adj. R-squared:                  0.728
# Method:                 Least Squares   F-statistic:                     35.84
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):           6.35e-05
# Time:                        12:51:58   Log-Likelihood:                -10.714
# No. Observations:                  14   AIC:                             25.43
# Df Residuals:                      12   BIC:                             26.71
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      4.7097      0.323     14.596      0.000       4.007       5.413
# x             -0.6685      0.112     -5.986      0.000      -0.912      -0.425
# ==============================================================================
# Omnibus:                        0.302   Durbin-Watson:                   2.599
# Prob(Omnibus):                  0.860   Jarque-Bera (JB):                0.017
# Skew:                           0.041   Prob(JB):                        0.991
# Kurtosis:                       2.849   Cond. No.                         6.81
# ==============================================================================

print(model.params['x'])          # -0.6684550167105405
print(model.params['Intercept'])  # 4.709676019780581

new_df = pd.DataFrame({'x': [5,6,7]})  # 새로운 자료
print('예측값 : ', model.predict(new_df))
# 예측값 :  
# 0    1.367401
# 1    0.698946
# 2    0.030491


print('-'*40)
print('문제 2번')

x = df.지상파
y = df.종편
print(x.ndim)  # 1차원
print(y.ndim)  # 1차원

data = np.array([x,y])
df = pd.DataFrame(data.T)
df.columns = ['x','y']
print(df.head(3))
#      x    y
# 0  0.9  0.7
# 1  1.2  1.0
# 2  1.2  1.3

model2 = smf.ols(formula="y ~ x",data=df).fit()
print(model2.summary()) 
#                             OLS Regression Results
# ==============================================================================
# Dep. Variable:                      y   R-squared:                       0.788
# Model:                            OLS   Adj. R-squared:                  0.770
# Method:                 Least Squares   F-statistic:                     44.53
# Date:                Fri, 03 Apr 2026   Prob (F-statistic):           2.28e-05
# Time:                        12:57:58   Log-Likelihood:                -11.223
# No. Observations:                  14   AIC:                             26.45
# Df Residuals:                      12   BIC:                             27.72
# Df Model:                           1
# Covariance Type:            nonrobust
# ==============================================================================
#                  coef    std err          t      P>|t|      [0.025      0.975]
# ------------------------------------------------------------------------------
# Intercept      0.2952      0.335      0.882      0.395      -0.434       1.024
# x              0.7727      0.116      6.673      0.000       0.520       1.025
# ==============================================================================
# Omnibus:                        2.821   Durbin-Watson:                   1.628
# Prob(Omnibus):                  0.244   Jarque-Bera (JB):                1.752
# Skew:                           0.857   Prob(JB):                        0.416
# Kurtosis:                       2.749   Cond. No.                         6.81
# ==============================================================================

print(model2.params['x'])          # 0.7726869861042749
print(model2.params['Intercept'])  # 0.29516333605064715

new_df2 = pd.DataFrame({'x': [10,11,12]})  
print('예측값 : ', model2.predict(new_df2))
# 예측값 :  
# 0    8.022033
# 1    8.794720
# 2    9.567407