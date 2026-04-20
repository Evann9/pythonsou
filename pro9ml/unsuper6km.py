# 쇼핑몰 고객 세분화 연습
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.cluster import KMeans

# 가상의 고객 데이터 생성
np.random.seed(0)
n_customers = 200  # 고객은 200명
annul_spending = np.random.normal(50000, 15000, n_customers) # 연간 지출액
monthly_visit = np.random.normal(5,2,n_customers)  # 월 방문 횟수

# 구간 나누기(음수 제거-clip)
# a = np.array([-3.2, -0.5, 1.7]) -> np.clip(a, 0, 1) -> [0, 0, 1]
annul_spending = np.clip(annul_spending, 0, None)
monthly_visit = np.clip(monthly_visit, 0, None)

data = pd.DataFrame({
    "annul_spending": annul_spending,
    "monthly_visit": monthly_visit
})

print(data.head(), data.shape)

# 산포도
plt.scatter(data['annul_spending'], data['monthly_visit'])
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.title('고객 데이터')
plt.grid(True)
plt.show()

# KMeans 군집화
kmeans = KMeans(n_clusters=3, random_state=0)
clusters = kmeans.fit_predict(data)

# cluster 별로 데이터 보기
data['cluster'] = clusters

# 군집 결과 시각화
for cluster_id in np.unique(clusters):
    cluster_data = data[data['cluster'] == cluster_id]
    plt.scatter(cluster_data['annul_spending'], 
                cluster_data['monthly_visit'], 
                label=f'군집{cluster_id}'
                )
# 중심점
plt.scatter(kmeans.cluster_centers_[:,0], 
            kmeans.cluster_centers_[:, 1], 
            c='black', 
            marker='X', 
            s=200, 
            label='중심점'
            )
plt.xlabel('연간 지출액')
plt.ylabel('월 방문 횟수')
plt.title('소비자 군집화 결과')
plt.legend()
plt.grid(True)
plt.show()