# 어느 쇼핑몰의 고객 행동 데이터를 이용해 군집 분류(가공된 데이터 사용)
# 고객마다 소비 패턴이 다르므로 여러 그룹이 형성됨.

import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.preprocessing import StandardScaler
import seaborn as sns
from sklearn.cluster import DBSCAN
import pandas as pd
import numpy as np

import os
os.environ['OMP_NUM_THREADS'] = '1'  # 경고 무시

# 일반적으로 계층적/비계층적 군집 분석을 선행하고 마음에 들지 않으면 DBSCAN을 함

np.random.seed(42)

# 고객 데이터 생성

# vip 고객
vip = pd.DataFrame({
    'annual spending':np.random.normal(700, 40, 80),
    'visit_per_month':np.random.normal(20, 2, 80),
    'avg_purchase':np.random.normal(80, 10, 80),
    'group':'vip'
})

# 일반 고객 - 평균적 소비 패턴, 가장 많은 비중 차지
normal = pd.DataFrame({
    'annual spending':np.random.normal(300, 100, 150),
    'visit_per_month':np.random.normal(10, 4, 150),
    'avg_purchase':np.random.normal(30, 15, 150),
    'group':'normal'
})

# 휴면 고객 - 방문 적음, 구매 적음
low = pd.DataFrame({
    'annual spending':np.random.normal(100, 30, 70),
    'visit_per_month':np.random.normal(3, 1, 70),
    'avg_purchase':np.random.normal(10, 5, 70),
    'group':'low'
})

print(vip.head(3))
print(normal.head(3))
print(low.head(3))

# 특이 패턴 고객
t = np.linspace(0, 3 * np.pi, 60)
curve = pd.DataFrame({
    'annual spending': 200 + 100 * np.cos(t) + np.random.normal(0, 10, len(t)) + 200 + 100 * np.cos(t),
    'visit_per_month':np.random.normal(0, 1, len(t)) + 10 + 5 * np.sin(t),
    'avg_purchase': 40 + 10 * np.sin(t),
    'group':'curve'
})

# 이상 고객 (이상치)
outliers = pd.DataFrame({
    'annual spending': [900, 50, 850],
    'visit_per_month':[10, 1, 25],
    'avg_purchase': [120, 5, 100],
    'group':'outliers'
})

print(curve.head(3))
print(outliers.head(3))

# 데이터 합치기
df = pd.concat([vip, normal, low, curve, outliers], ignore_index=True)
print(df.shape) # (363, 4)

# 초기 데이터 시각화
plt.figure(figsize=(6,5))
sns.scatterplot(
    x='annual spending', 
    y='visit_per_month', 
    hue='group', 
    palette='Set2',
    data=df
)
plt.title('고객 데이터')
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.legend(title='소비 행태')
plt.show()

# DBSCAN 
scaler = StandardScaler()
x_scaled = scaler.fit_transform(df.drop(columns=['group']))
dbscan = DBSCAN(eps=0.5, min_samples=5, metric='euclidean')
clusters = dbscan.fit_predict(x_scaled)
df['cluster'] = clusters
print(df.head(3))

# 군집 결과 시각화
plt.figure(figsize=(6,5))
sns.scatterplot(
    x='annual spending', 
    y='visit_per_month', 
    hue='cluster', 
    palette='Set1',
    data=df
)
plt.title('군집 결과')
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.legend(title='소비 행태')
plt.show() # 매출에 따라 3개의 군집으로 분류함