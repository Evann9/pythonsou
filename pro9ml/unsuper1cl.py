# 군집분석 : 데이터 간의 유사도를 정의하고 그 유사도에 가까운 것부터 순서대로
# 합쳐가는 방법으로, 거리나 상관계수 등을 이용한다.
# 이는 비슷한 특성를 가진 개체를 그룹으로 만들고, 군집 분리 후 t-test, ANOVA 분석등을 
# 통해 그룹간 평균의 차이를 확인할 수도 있다.
# 군집분석은 데이터만 주고 label은 제공하지 않는 비지도학습이다.

# 클러스터링 기법 중 계층적 클러스터링 연습
# 응집형(군집의 크기를 점점 늘리기 - 상향식)과 분리형(군집의 크기를 줄여나가기 - 하향식)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(123)
var = ['x', 'y']
labels = ['점0','점1','점2','점3','점4']
x = np.random.random_sample([5, 2]) * 10
df = pd.DataFrame(x, columns=var, index=labels)
print(df)

plt.scatter(x[:, 0], x[:, 1], c='blue', marker='o', s=50)
# text 추가
for i, txt in enumerate(labels):
    plt.text(x[i, 0], x[i, 1], txt)

plt.grid(True)
plt.show()

# 각 점 간의 거리 계산
from scipy.spatial.distance import pdist, squareform
dist_vec = pdist(df, metric='euclidean')
print('dist_vec : ', dist_vec)
# pdist의 결과를 사각형 형식으로 보기
row_dist = pd.DataFrame(squareform(dist_vec), columns=labels, index=labels)
print(row_dist)

print()
from scipy.cluster.hierarchy import linkage
# linkage : 응집형 계층적 클러스터링
row_clusters = linkage(dist_vec, method='ward')

df2 = pd.DataFrame(row_clusters, columns=['클러스터id1', '클러스터id2', '거리', '클러스터멤버'])
print(df2)

# 클러스터의 계층 구조를 계통도(dendrogram)롤 출력
from scipy.cluster.hierarchy import dendrogram
dendrogram(row_clusters, labels=labels)
plt.tight_layout()
plt.ylabel('유클리드 거리')
plt.show()