# 이원분산분석 : 요인 복수 - 각 요인의 레벨(그룹)도 복수
# 두 개의 요인에 대한 집단(독립변수) 각각이 종속변수(평균)에 영향을 주는지 검정
# 주효과(개별효과) : 독립변수들이 독립적으로 종속변수에 미치는 영향을 검정하는 것.
# 상호작용효과(교호작용) : 분산분석(ANOVA)이나 회귀분석에서 한 독립변수가 종속변수에 미치는 영향이 
#                         다른 독립변수의 수준에 따라 달라지는 현상

import numpy as np
import pandas as pd
import scipy.stats as stats
import matplotlib.pyplot as plt
import koreanize_matplotlib
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

# 실습 1. 태아 수와 관측자 수가 태아의 머리둘레 평균에 영향을 주는가?
# 주효과 가설
# 귀무 : 태아 수와 태아의 머리둘레 평균은 차이가 없다.
# 대립 : 태아 수와 태아의 머리둘레 평균은 차이가 있다.
# 귀무 : 관측자 수와 태아의 머리둘레 평균은 차이가 없다.
# 대립 : 관측자 수와 태아의 머리둘레 평균은 차이가 있다.

# 교호작용 가설
# 귀무 : 교호작용이 없다 (태아 수와 관측자 수는 관련이 없다)
# 대립 : 교호작용이 있다 (태아 수와 관측자 수는 관련이 있디)

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/group3_2.txt")
print(data.head(3), data.shape)   # (36, 3)
print(data['태아수'].unique())    # [1 2 3]
print(data['관측자수'].unique())  # [1 2 3 4]

# 시각화
# data.boxplot(column='머리둘레', by='태아수')
# plt.show()
# data.boxplot(column='머리둘레', by='관측자수')
# plt.show()

# ols
# linreg = ols("머리둘레 ~ C(태아수) + C(관측자수)", data=data).fit() # 교호작용 X
# linreg = ols("머리둘레 ~ C(태아수) + C(관측자수) + C(태아수):C(관측자수)", data=data).fit  # 교호작용 O ( + )
linreg = ols("머리둘레 ~ C(태아수) * C(관측자수)", data=data).fit()    # 교호작용 O ( * )
result = anova_lm(linreg, typ=1)
print(result)
#                         df      sum_sq     mean_sq         F        PR(>F)
# C(태아수)               2.0  324.008889  162.004444  2113.101449  1.051039e-27  
# C(관측자수)             3.0    1.198611    0.399537     5.211353  6.497055e-03
# C(태아수):C(관측자수)   6.0    0.562222    0.093704     1.222222  3.295509e-01

# 태아수 : PR(>F) 1.051039e-27 < 0.05 => 귀무기각. 태아 수와 태아의 머리둘레 평균은 차이가 있다.(유의함)
# C(관측자수) : PR(>F) 6.497055e-03(0.00647) < 0.05 : 귀무기각. 관측자 수에 따라 태아의 머리둘레 평균은 차이가 있다(유의함)
# C(태아수):C(관측자수) : PR(>F) 3.295509e-01 > 0.05 : 귀무채택. 태아 수와 관측자 수는 관련이 없다.
# 해석 : 
# 태아 수와 관측자 수는 종속변수에 유의한 영향을 미친다.
# 그러나 태아 수와 관측자 수 간의 교호작용 효과는 무의미 하다.

print('-'*40)
# 실습 2. poison과 treat가 독 퍼짐 시간의 평균에 영향을 주는가?
# 주효과 가설
# 귀무 : poison 종류와 독 퍼짐 시간의 평균은 차이가 없다.
# 대립 : poison 종류와 독 퍼짐 시간의 평균은 차이가 있다.
# 귀무 : treat(응급처치) 방법과 독 퍼짐 시간의 평균은 차이가 없다.
# 대립 : treat(응급처치) 방법과 독 퍼짐 시간의 평균은 차이가 있다.

# 교호작용 가설
# 귀무 : 교호작용이 없다 (poison 종류와 treat(응급처치) 방법는 관련이 없다)
# 대립 : 교호작용이 있다 (poison 종류와 treat(응급처치) 방법는 관련이 있디)

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/poison_treat.csv", index_col=0)
print(data2.head(3), data2.shape)   # (48, 3)
#    time  poison treat
# 1  0.31       1     A
# 2  0.45       1     A
# 3  0.46       1     A 
# ...
print(data2.groupby('poison').agg(len))
print(data2.groupby('treat').agg(len))
print(data2.groupby(['poison', 'treat']).agg(len))  
# 요인 별 레벨의 표본수는 4로 동일 (모든 집단 별 표본수는 동일하므로 균형설계가 잘됨)

result2 = ols("time ~ C(poison) * C(treat)", data=data2).fit()
print(anova_lm(result2, typ=1))
#                       df    sum_sq   mean_sq          F        PR(>F)
# C(poison)            2.0  1.033013  0.516506  23.221737  3.331440e-07
# C(treat)             3.0  0.921206  0.307069  13.805582  3.777331e-06
# C(poison):C(treat)   6.0  0.250138  0.041690   1.874333  1.122506e-01

# 해석 :
# C(poison)  : PR(>F) 3.331440e-07 < 0.05 => 귀무기각. poison 종류와 독 퍼짐 시간의 평균은 차이가 있다.(유의함)
# C(treat) : PR(>F) 3.777331e-063 < 0.05 : 귀무기각. treat(응급처치) 방법과 독 퍼짐 시간의 평균은 차이가 있다.(유의함)
# C(poison):C(treat) : PR(>F) 1.122506e-01 > 0.05 : 귀무채택. poison 종류와 treat(응급처치) 방법는 관련이 없다.

# 사후분석
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tkResult = pairwise_tukeyhsd(endog=data2['time'], groups=data2['poison'])
print(tkResult)
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      1      2  -0.0731 0.5882 -0.2525  0.1063  False
#      1      3  -0.3412 0.0001 -0.5206 -0.1619   True
#      2      3  -0.2681 0.0021 -0.4475 -0.0887   True
# ----------------------------------------------------
tkResult.plot_simultaneous(xlabel='mean of time', ylabel='poison')
plt.show()

print()
tkResult2 = pairwise_tukeyhsd(endog=data2['time'], groups=data2['treat'])
print(tkResult2)
# group1 group2 meandiff p-adj   lower   upper  reject
# ----------------------------------------------------
#      A      B   0.3625  0.001  0.1253  0.5997   True
#      A      C   0.0783 0.8143 -0.1589  0.3156  False
#      A      D     0.22 0.0778 -0.0172  0.4572  False
#      B      C  -0.2842 0.0132 -0.5214 -0.0469   True
#      B      D  -0.1425  0.387 -0.3797  0.0947  False
#      C      D   0.1417 0.3922 -0.0956  0.3789  False
# ----------------------------------------------------
tkResult2.plot_simultaneous(xlabel='mean of time', ylabel='treat')
plt.show()
