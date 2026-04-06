# 선형회귀분석 모형의 적절성 선행조건
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import statsmodels.formula.api as smf

advdf = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv", usecols=[1,2,3,4])
print(advdf.head(3), advdf.shape)
print(advdf.info())
print(advdf.corr())

print()
# 단순선형회귀모델 - ols
# x : tv, y : sales
lm = smf.ols(formula='sales ~ tv', data=advdf).fit()
print(f"coeffients:{lm.params}, p-value:{lm.pvalues}, r-squared:{lm.rsquared}")
# print(0.782224 ** 2)
print(lm.summary())
print(lm.summary().tables[1])
print()
# 예측 
x_new = pd.DataFrame({'tv':advdf.tv[:3]})
print(x_new)
print('실제값 : ', advdf.sales[:3].values)
print('예측값 : ', lm.predict(x_new).values)
print('직접 계산 : ', lm.params.tv * 230.1 + lm.params.Intercept)

print()
# 경험하지 않은 tv 광고비에 따른 상품 판매량 예측 
my_new = pd.DataFrame({'tv':[100, 350, 780]})
print('예측 상품 판매량 : ', lm.predict(x_new).values)

# 시각화
plt.scatter(advdf.tv, advdf.sales)
plt.xlabel('tv광고비')
plt.ylabel('상품판매량')
ypred = lm.predict(advdf.tv)
plt.plot(advdf.sales, ypred, c='red')
plt.title('단순선형회귀')
plt.grid(True)
plt.show()

print('\n단순선형회귀모델이므로 적절성 선행조건 중 잔차의 정규성, 선형성 확인')
# 잔차(Resudual): 실제 관측값과 모델이 예측한 값의 차이를 의미
# 모델이 데이터를 얼마나 잘 설명하는지 보여주는 척도
fitted = lm.predict(advdf)
residual = advdf['sales'] - fitted
print('실제값:', advdf['sales'][:5].values)
print('예측값:', fitted[:5].values)
print('잔차값 : ', residual[:5].values)
print('잔차평균값 : ', np.mean(residual[:5].values))        # 1.6738829920227805

print('잔차의 정규성 : 잔차가 정규성을 따르는지 확인')
from scipy.stats import shapiro
import statsmodels.api as sm

stat, p = shapiro(residual)
print(f"통계량 :{stat}, p-vlaue:{p}")
# 통계량 :0.9905306561484953, p-vlaue:0.21332551436720226 > 0.05 이므로 정규성 만족
print("정규성 만족" if p > 0.05 else "정규성 만족")
# Q-Q plot으로 시각화
sm.qqplot(residual, line='s')
plt.title("Q-Q plot으로 정규성 만족 확인")
plt.show()

print("선형성 검정 : 독립변수의 변화에 종속변수도 변화하나 특정한 패턴이 있으면 안 됨")
# 독립변수와 종속변수 간에 선형형태로 적절하게 모델링 되었는지 검정
from statsmodels.stats.diagnostic import linear_reset       # 선형성 확인 모듈
reset_result = linear_reset(lm, power=2, use_f=True)
print('reset_result 결과', reset_result.pvalue)
print('선형성 만족' if reset_result.pvalue > 0.05 else '선형성 위배')
# 시각화
sns.regplot(x=fitted, y=residual, lowess=True, line_kws={'color': 'red'})
plt.plot([fitted.min(), fitted.max()], [0, 0], '--', color='grey')
plt.show()

print("등분산성 검정 : 모든 x값에서 오차의 퍼짐이 유사해야 한다")
from statsmodels.stats.diagnostic import het_breuschpagan
bp_test = het_breuschpagan(residual, sm.add_constant(advdf['tv']))
bp_stat, bp_pvalue = bp_test[0], bp_test[1]
print(f"breuschpagan test : 통계량:{bp_stat}, p-value:{bp_pvalue}")
print('등분산성 만족' if bp_pvalue > 0.05 else '등분산성 위배')

print()
# 참고 : Cook's distance - 특정 데이터가 회귀모델에 얼마나 영향을 주는지 확인
# 영향력 있는 관측치(이상치)를 탐지하는 진단 방법
# 데이터가 적을 때 , 이상치가 의심스러울 때, 모델 결과가 이상하게 나올 때...
from statsmodels.stats.outliers_influence import OLSInfluence
cd, _ = OLSInfluence(lm).cooks_distance  # 쿡거리, 인덱스 반환

# 쿡거리가 가장 큰 5개 확인
print(cd.sort_values(ascending=False).head())
# 35     0.060494
# 178    0.056347
# 25     0.038873
# 175    0.037181
# 131    0.033895

# 쿡거리가 가장 큰(영향력이 큰) 관측치 원본 확인
print(advdf.iloc[[35, 178, 25, 175, 131]])
#         tv  radio  newspaper  sales
# 35   290.7    4.1        8.5   12.8
# 178  276.7    2.3       23.7   11.8
# 25   262.9    3.5       19.5   12.0
# 175  276.9   48.9       41.8   27.0
# 131  265.2    2.9       43.0   12.7
# 대부분 tv 광고비는 매우 높으나  sales가 낮음 - 모델이 예측하기 어려운 포인트들

# 시각화 
fig = sm.graphics.influence_plot(lm, alpha=0.05, criterion='cooks')
plt.show()

print("------" * 10)
# 다중선형회귀모델 - ols
# x : tv, radio, newspaper, y : sales
lm_mul = smf.ols(formula='sales ~ tv + radio + newspaper', data=advdf).fit()
print(lm_mul.summary())
