# KMeans : iris dataset - 군집분석, 정량평가, 클러스터별 평균 비교(ANOVA)
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score
# adjusted_rand_score : 군집 vs 실제 라벨 비교
# normalized_mutual_info_score : 정보량 기반 유사도(같은 정보 공유)
# silhouette_score : 군집 자체 품질 평가(군집에 잘 속해 있는가 확인)
from sklearn.decomposition import PCA  # 4차원 -> 2차원 (압축)

import os
os.environ['OMP_NUM_THREADS'] = '1'  # 경고 무시

iris = load_iris()
x =  iris.data
y = iris.target
feature_names = iris.feature_names

df = pd.DataFrame(x, columns=feature_names)
print('iris data shape : ', df.shape) # (150, 4)

# 스케일링
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)
print(x_scaled[:2])

# PCA (여기서는 시각화용으로 준비함)
pca = PCA(n_components=2)
x_pca = pca.fit_transform(x_scaled)
print('PCA 설명 분산 비율 : ', pca.explained_variance_ratio_) # [0.72962445 0.22850762]
# 해석: 
# 첫 번째 주성분(PC1)이 전체 데이터 변동성의 약 73%를 설명하고, 
# 두 번째 주성분(PC2)이 약 23%를 설명함. 
# 두 성분을 합치면 전체 데이터의 약 96%에 해당하는 정보를 유지하면서 4차원 데이터를 2차원으로 축소했음을 의미함.

# KMeans 모델
k = 3
kmeans = KMeans(
    n_clusters=k,
    init='k-means++', 
    n_init=10,  # 10회 수행 시 가장 오차(inertia)가 작은 결과를 선택
    random_state=42
)

clusters = kmeans.fit_predict(x_scaled)
df['cluster'] = clusters
print('클러스터 중심 값 : ', kmeans.cluster_centers_)
x_pca = pca.fit_transform(x_scaled)
print('PCA 설명 분산 비율 : ', pca.explained_variance_ratio_)
print(x_pca[:2])

plt.figure(figsize=(6,5))
sns.scatterplot(x=x_pca[:,0], y=x_pca[:,1], hue=clusters, palette='Set1')
plt.title('군집결과')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# 실제 라벨과 군잡 비교
ct = pd.crosstab(y, clusters)
print(ct)

print('클래스별 대표 군집')
for i in range(ct.shape[0]):
    max_cluster = ct.iloc[i].idxmax()
    print(f"실제 클래스 {i}가 가장 많이 속한 군집 : {max_cluster} (갯수 : {ct.iloc[i].max()})")

print('정량 평가 ---')
ari = adjusted_rand_score(y, clusters)
nmi = normalized_mutual_info_score(y, clusters)
sil_score = silhouette_score(x_scaled, clusters)
print(f'ARI : {ari:.4f}')   # 0.6201
print(f'NMI : {nmi:.4f}')   # 0.6595
print(f'Silhouette Score : {sil_score:.4f}') # 0.4599
# 군집 자체 품질 평가 : 0.4599  - 1에 근사할수록 좋음. 0 또는 음수면 잘못된 군집
# 좋은 군집이란 군집 내 요소끼리 가깝고, 다른 군집 간 거리는 멀다.

# k=3을 사용했는데 과연 3이 적합한지 확인 : 엘보우
initia_list = []
k_range = range(1, 11)
for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(x_scaled)
    initia_list.append(km.inertia_)

plt.figure(figsize=(6,4))
plt.plot(k_range, initia_list, marker='o')
plt.title('Elbow 기법')
plt.xlabel('클러스터 수(k)')
plt.ylabel('initia')
plt.show()  # k가 3인 경우가 가장 적당함

# 실제 vs 군잡 비교 시각화
plt.figure(figsize=(12,5))
# 실제 라벨
plt.subplot(1,2,1)
sns.scatterplot(x=x_pca[:,0], y=x_pca[:,1], hue=y, palette='Set1')
plt.title('실제 라벨')
plt.xlabel('PC1')
plt.ylabel('PC2')

# 군집 라벨
plt.subplot(1,2,2)
sns.scatterplot(x=x_pca[:,0], y=x_pca[:,1], hue=clusters, palette='Set1')
plt.title('군집 라벨')
plt.xlabel('PC1')
plt.ylabel('PC2')
plt.show()

# 군집별 평균 분석
cluster_mean = df.groupby('cluster').mean()
print('클러스터 별 평균 : ', cluster_mean)

# 군집 3개 : 군집 간 평균차이 검정(ANOVA)
# 귀무 : 군집 간 평균의 차이가 없다.
# 대립 : 군집 간 평균의 차이가 있다.
from scipy.stats import f_oneway
for col in feature_names:
    group0 = df[df['cluster'] == 0][col]
    group1 = df[df['cluster'] == 1][col]
    group2 = df[df['cluster'] == 2][col]
    # ANOVA
    f_stat, p_val = f_oneway(group0, group1, group2)
    print(f"{col} : f-statistic:{f_stat:.4f}, p-value:{p_val:.4f}")

    # 해석
    if p_val >= 0.05:
        print('군집 간 평균의 차이가 없다(유의하지 않다. 우연O)')
    else:
        print('군집 간 평균의 차이가 있다(유의하다. 우연X)')

# KMeans가 꽃잎, 꽃받침 길이/너비를 제대로 군집분석 했음을 알 수 있다.

# 사후검정
from statsmodels.stats.multicomp import pairwise_tukeyhsd
feature = 'petal length (cm)'
tukey = pairwise_tukeyhsd(
    endog=df[feature], 
    groups=df['cluster'],
    alpha=0.05,
)
print('tukeyhsd 결과 (petal length) : ', tukey)
# ===================================================
# group1 group2 meandiff p-adj  lower   upper  reject
# ---------------------------------------------------
#      0      1  -2.9078   0.0 -3.1405 -2.6751   True
#      0      2   1.1408   0.0  0.9043  1.3773   True
#      1      2   4.0486   0.0  3.8088  4.2884   True
# ---------------------------------------------------

# 사후검정 시각화
tukey.plot_simultaneous(figsize=(6,4))
plt.title(f'Tukey HSD 결과 ({feature})')
plt.xlabel('평균차이')
plt.show()

print()
# 군집 별 Boxplot
for col in feature_names:
    plt.figure(figsize=(6,4))
    sns.boxplot(x='cluster', y=col, data=df)
    plt.title(f'군집별 Boxplot ({col})')
    plt.xlabel('군집')
    plt.ylabel(col)
    plt.show()

print()
# 클러스터 평균 분석 - 마지막 열에 Type 추가
cluster_mean['label'] = ['type A','type B','type C']
print(cluster_mean)