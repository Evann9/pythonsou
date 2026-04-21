# DBSCAN
# DBSCAN(Density-Based Spatial Clustering of Applications with Noise)은 밀도 기반의 비지도 학습 클러스터링 알고리즘입니다. 
# 데이터가 촘촘하게 모여 있는 고밀도 지역을 군집으로 묶고, 저밀도 지역의 점들을 이상치(Noise)로 처리하며, 
# 불규칙한 형태의 군집을 탐지하고 군집 수를 미리 지정하지 않아도 되는 장점이 있습니다.

import matplotlib.pyplot as plt
from matplotlib import style
from sklearn.datasets import make_moons
from sklearn.cluster import DBSCAN, KMeans

import os
os.environ['OMP_NUM_THREADS'] = '1'  # 경고 무시

# 샘플 데이터 생성
x, y = make_moons(n_samples=200, noise=0.05, random_state=0, shuffle=True)
print(x[:5], x.shape) #  (200, 2)

plt.scatter(x[:, 0], x[:, 1])
plt.show()

print('KMeans로 군집 분류')
km = KMeans(n_clusters=2,init='k-means++', random_state=0)
pred1 = km.fit_predict(x)
print('km 예측 군집 id : ',pred1[:10])

# km 결과 시각화
def plotResult(x, pr, title, show_centers=False):
    plt.scatter(x[pr == 0, 0], x[pr == 0, 1], c='b', marker='o', s=40, label='cluster1')
    plt.scatter(x[pr == 1, 0], x[pr == 1, 1], c='r', marker='s', s=40, label='cluster2')
    # KMeans는 '중심점(centroid)'을 실제로 계산하는 알고리즘이므로
    # KMeans 결과를 그릴 때만 중심점을 함께 표시한다.
    if show_centers:
        plt.scatter(km.cluster_centers_[:, 0], km.cluster_centers_[:,1], c='black', marker='+', label='centroid')
    plt.title(title)
    plt.legend()
    plt.show()

plotResult(x, pred1, 'KMeans Clustering Result', show_centers=True)

print('DBSCAN으로 군집 분류')
db = DBSCAN(eps=0.2, min_samples=5, metric='euclidean')
# eps : 이웃을 정의하기 위한 최대 거리(반지름)
# min_samples : 핵심 포인트(Core Point)가 되기 위해 eps 내에 존재해야 하는 최소 샘플 수
pred2 = db.fit_predict(x)
print('db 예측 군집 id : ',pred2[:10])
print('군집 종류 : ', set(pred2)) # 0, 1 이상치는 없는 상태
plotResult(x, pred2, 'DBSCAN Clustering Result')  # 분류 완료

# DBSCAN과 KMeans와 다른 이유
# 1) KMeans는 각 데이터가 '어떤 중심점과 더 가까운가'만 보고 군집을 나눈다.
#    그래서 군집 경계가 직선/원형에 가까워지고, 반달(moons)처럼 휘어진 모양은 잘 반영하지 못한다.
# 2) DBSCAN은 중심점이 아니라 '주변에 점이 얼마나 촘촘히 모여 있는가'를 기준으로 묶는다.
#    그래서 반달처럼 길게 휘어진 비정형 모양도 한 덩어리 군집으로 더 자연스럽게 찾을 수 있다.
# 3) DBSCAN은 조건에 맞지 않는 점을 -1(이상치)로 따로 뺄 수 있지만,
#    이번 설정(eps=0.2, min_samples=5)에서는 이상치가 거의 없어 0, 1 두 군집만 나온 상태다.
# 4) 즉, '같은 데이터'라도 군집을 나누는 기준 자체가 달라서 화면 아래 결과 모양에 차이가 난다.