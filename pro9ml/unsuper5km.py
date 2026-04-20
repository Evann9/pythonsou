# 비계층적 군집분석 (KMeans)
# 학생 10명의 시험점수 사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

students =['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10']
scores = np.array([76,95,65,85,60,92,55,88,83,72]).reshape(-1, 1)
print('점수 : ', scores)

kmeans = KMeans(n_clusters=3, init='k-means++', random_state=0)
km_clusters = kmeans.fit_predict(scores)
print(km_clusters) # [2 0 1 2 1 0 1 0 2 2]

df = pd.DataFrame({
    'student': students,
    'score': scores.ravel(),
    'cluster': km_clusters
})
print(df)

# 군집 별 평균 점수
print('\n군집 별 평균 점수')
avg_scores = df.groupby('cluster')['score'].mean()
print(avg_scores)
# cluster
# 0    91.666667
# 1    60.000000
# 2    79.000000

# 시각화(산점도)
x_positions = np.arange(len(students))
y_scores = scores.ravel()
colors = {0:'red', 1:'blue', 2:'green'}
plt.figure(figsize=(10, 6))
for i, (x, y, cluster) in enumerate(zip(x_positions, y_scores, km_clusters)):
    plt.scatter(x, y, color=colors[cluster], s=100)
    plt.text(x, y + 1.5, students[i], fontsize=12, ha='center')

# 중심점 
centers = kmeans.cluster_centers_
for center in centers:
    plt.scatter(len(students)//2, center[0], marker='X', c='black', s=200)

# 학생 별 군집 색으로 구분해 산점도 출력
plt.xticks(x_positions, students)
plt.xlabel('학생명')
plt.ylabel('점수')
plt.grid(True)
plt.show() 