# <선호도 분석 실습>
# 일원카이제곱 검정
# 5개의 스포츠 음료에 대한 선호도 차이가 있는지 검정하기

# 귀무가설(H0) : 기대치와 관찰치는 차이가 없다. 스포츠 음료의 선호도에 차이가 없다.
# 대립가설(H1) : 기대치와 관찰치는 차이가 있다. 스포츠 음료의 선호도에 차이가 있다.

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/drinkdata.csv")
print(data)
print(stats.chisquare(data['관측도수']))
# statistic = 20.488, pvalue = 0.0003999
exp = [data['관측도수'].sum() / 5] * 5
print(exp)  # 기대빈도 50.8
stat, p = stats.chisquare(f_obs=data['관측도수'], f_exp = exp)
print('stat', stat)
print('p', p)

# 판정: p-value가 0.05보다 작으므로 선호도에 유의미한 차이가 있다.'
# 스포츠 음료의 선호도에 차이가 있다 라는 의견이 박아들여짐.

# 시각화
import matplotlib.pyplot as plt
import koreanize_matplotlib
import numpy as np

# 기대도수 
total = data['관측도수'].sum()
expected = [total / len(data)] * len(data)
x = np.arange(len(data))  # 음료 수 만큼 x축 좌표
width = 0.35  # 막대 너비
plt.figure(figsize=(10, 5))
plt.bar(x - width/2, data['관측도수'], width=width, label='관측도수')
plt.bar(x + width/2, expected, width=width, label='기대도수', alpha=0.6)
plt.xticks(x, data['음료종류'])
plt.ylabel('도수')
plt.legend()
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()

# 카이제곱 검정 결과와 그래프를 근거로 어떤 음료가 더 인기 있는지 분석
data['기대도수'] = expected
data['차이(관측-기대)'] = data['관측도수'] - data['기대도수']
data['차이비율(%)'] = round(data['차이(관측-기대)'] / expected * 100, 2)
# print(data)
data.sort_values(by='차이(관측-기대)', ascending=False, inplace=True)
data.reset_index(drop=True, inplace=True)
print(data)

