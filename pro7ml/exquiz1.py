# tv,radio,newspaper 간의 상관관계를 파악하시오. 
# 또한 sales와 관계를 알기 위해 sales에 상관 관계를 정렬한 후 TV, radio, newspaper에 대한 영향을 해석하시오.
# 그리고 이들의 관계를 heatmap 그래프로 표현하시오. 

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

url = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv"
data = pd.read_csv(url, index_col=0) # 첫 번째 인덱스 컬럼 제외
print(data.head())

print('상관계수')
print(data.corr(method='pearson')) 

print('-'*40)
# sales와 관계를 알기 위해 상관 관계 정렬
co_re = data.corr()
print(co_re['sales'].sort_values(ascending=False))
# sales        1.000000
# tv           0.782224
# radio        0.576223
# newspaper    0.228299

# 해석:
# 1. TV(0.78)가 매출(sales)에 가장 큰 양의 상관관계를 가짐.
# 2. Radio(0.58)도 매출과 상당한 상관관계가 있음.
# 3. Newspaper(0.23)는 매출과 상관관계가 상대적으로 낮음.
# 결론: 매출 증대를 위해서는 TV 광고의 영향력이 가장 크며, 신문보다는 라디오 광고가 더 효율적일 수 있음.

# 시각화
# data.plot(kind='scatter', x='sales', y='tv')
# data.plot(kind='scatter', x='sales', y='radio')
# data.plot(kind='scatter', x='sales', y='newspaper')
# plt.show()

# 산점도
# from pandas.plotting import scatter_matrix
# attr = ['sales','tv','radio','newspaper']
# scatter_matrix(data[attr], figsize=(12,8))
# plt.show()

# 히트맵 시각화
sns.heatmap(data.corr(), annot=True, cmap='RdBu')
plt.show()