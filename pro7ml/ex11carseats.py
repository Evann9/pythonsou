# Carseats 데이터를 활용한 다중선형회귀분석 및 모델 적절성 검정
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

# 1. 데이터 로드 및 전처리
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Carseats.csv")
print(df.head(3), df.shape)
print(df.info()) 
# 범주형 변수 및 불필요한 컬럼 제거 (수치형 변수 위주로 분석)
df = df.drop([df.columns[6], df.columns[9], df.columns[10]], axis = 1)
print(df.corr())

# 2. 다중선형회귀 모델 생성 (Sales를 종속변수로 설정)
lm = smf.ols(formula='Sales ~ Income + Advertising + Price + Age', data=df).fit()
print(lm.summary())

print("\n선형회귀 모델의 적절성 조건 체크 후 모델 사용")
print(df.columns) 
# ['Sales', 'CompPrice', 'Income', 'Advertising', 'Population', 'Price', 'Age', 'Education']
df_lm = df.iloc[:,[0,2,3,5,6]]
print(df_lm.head(2))

# 잔차(Residual) 계산: 실제값과 예측값의 차이
fitted = lm.predict(df_lm)
residual = df_lm['Sales'] - fitted
print('residual :', residual[:3])
print('잔차 평균 : ', np.mean(residual))

print("잔차의 정규성: 잔차가 정규성을 따르는지 확인")
from scipy.stats import shapiro
import statsmodels.api as sm

stat, p = shapiro(residual)
print(f"통계량 : {stat}, p-value : {p}")
print("정규성 만족" if p > 0.05 else "정규성 위배")
# Q-Q plot으로 잔차의 정규성 시각화
sm.qqplot(residual, line='s')
plt.title("Q-Q plot으로 정규성 만족 확인")
plt.show()

print("선형성 검정: 독립변수와 종속변수 간의 선형 관계 확인")
from statsmodels.stats.diagnostic import linear_reset
reset_result = linear_reset(lm, power=2, use_f=True)
print(f'reset_result 결과 : ', reset_result.pvalue)
print('선형성 만족' if reset_result.pvalue > 0.05 else '선형성 위배')
# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color':'red'})
plt.plot([fitted.min(), fitted.max()], [0,0], '--', color='grey')
plt.show()

print('등분산성 검정 : 모든 x 값 에서 오차의 퍼짐이 유사해야한다')
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(df_lm['Sales']))
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f"breuschpagan : 통계량 : {bp_stat}, p-value : {bp_pvalue}")
# 통계량 : 48.037965662293594, p-value : 4.180455907755742e-12
# 해석 : p-value(4.18e-12) < 0.05 이므로 귀무가설(등분산성)을 기각.
print("등분산성 만족"  if bp_pvalue > 0.05 else "등분산성 위배")
# 시각화는 선형성 시각화 참조

print('독립성 검정 : 다중회귀 분석 시 독립변수의 값이 서로 관련되지 않아야 한다')
# 잔차가 자기상관(인접 관측치의 오차가 상관됨)이 있는지 확인
# Durbin-Watson : 잔차의 자기상관(autocorrelation) 검정 지표. 잔차들이 서로 독립적인가? 시간 흐름 데이터에서 중요 (시계열)
# 값의 범위는 0 ~ 4 이고   2이면 정상 (자기상관 없음).   < 2이면 양의 자기상관,  > 2이면 음의 자기상관
# model.summary로 확인가능
import statsmodels.api as sm
print('Durbin-Watson : ', sm.stats.stattools.durbin_watson(residual))
# Durbin-Watson :  1.9314981270829592 이므로 잔차에 자기상관 없음

print("다중공선성 검정 : 다중회귀 분석 시 독립변수 간에 강한 상관관계가 있어서는 안된다.")
# VIF(Variance Inflation Factor, 분산 인플레 요인, 분산 팽창 지수)
#  :  값이 10을 넘으면 다중 공선선이 발생하는 변수라고 할 수 있다.
from statsmodels.stats.outliers_influence import variance_inflation_factor
df_ind = df[['Income','Advertising','Price','Age']] # 독립변수들
vifdf = pd.DataFrame()
vifdf['변수'] = df_ind.columns
vifdf['vif_value'] = [variance_inflation_factor(df_ind.values, i) for i in range(df_ind.shape[1])]

print(vifdf)   # 10을 초과하지 않았으므로 모두 만족
#    vif_value
# 0   5.971040
# 1   1.993726
# 2   9.979281
# 3   8.267760

# 시각화
sns.barplot(x='변수', y='vif_value', data=vifdf)
plt.title("VIF")
plt.show()

print('-----------------------')
# 4. 모델 저장 및 재사용
import joblib

# 학습된 모델을 파일로 저장
joblib.dump(lm, 'carseat.model')

# 저장된 모델 불러오기
# 이후부터는 아래처럼 읽어 사용하면 됨(lm은 없어도 됨)
mymodel = joblib.load('carseat.model')
print('새로운 값으로 Sales 예측')
new_df = pd.DataFrame({'Income':[35,62],'Advertising':[6,3], 'Price':[105, 88], 'Age':[32,55]})
pred = mymodel.predict(new_df)
print("Sales 예측 결과 : ", pred.values)
# Sales 예측 결과 :  [8.71289759 8.49715914]
