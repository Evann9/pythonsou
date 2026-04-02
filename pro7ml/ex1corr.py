# 공분산 / 상관계수
# 변수가 하나인 경우에는 분산은 거리와 관련이 있다.
# 변수가 두개인 경우에는 분산은 방향을 가진다.

import numpy as np

# 공분산
# 결과 행렬에서 비대각 요소(1행 2열 또는 2행 1열)의 값이 양수(+)이면 우상향 관계임
print(np.cov(np.arange(1,6), np.arange(2,7)))     # 우상향
# [[2.5 2.5]
#  [2.5 2.5]]  <- 2.5가 양수이므로 우상향
print(np.cov(np.arange(10,60,10), np.arange(20,70,10)))     # 우상향
print(np.cov(np.arange(100,600,100), np.arange(200,700,100)))     # 우상향
print(np.cov(np.arange(1,6), (3,3,3,3,3)))        # 직선(변화X)
# [[0. 0.]
#  [0. 0.]]
print(np.cov(np.arange(1,6), np.arange(6,1,-1)))  # 우하향
# [[ 2.5 -2.5]
#  [-2.5  2.5]]

# 참고: 공분산 행렬은 대칭 행렬이므로 1행 2열과 2행 1열은 항상 같은 값을 가집니다.
# 즉, 한쪽이 양수면 다른 한쪽도 반드시 양수여야 합니다.

print()
x = [8,3,6,6,9,4,3,9,3,4]
print('x 평균 : ', np.mean(x))   # 5.5
print('x 분산 : ', np.var(x))    # 5.45
y = [6,2,4,6,9,5,1,8,4,5]
print('x 평균 : ', np.mean(y))   # 5.0
print('x 분산 : ', np.var(y))    # 5.4

import matplotlib.pyplot as plt
# plt.plot(x,y,'o')
# plt.show()
# print('x,y의 공분산 : ', np.cov(x,y))
print('x,y의 공분산 : ', np.cov(x,y)[0,1])  # x,y의 공분산 :  5.222222222222222
x2 = [80,30,60,60,90,40,30,90,30,40]
y2 = [6,2,4,6,9,5,1,8,4,5]
print('x2,y2의 공분산 : ', np.cov(x2,y2)[0,1])  # x,y의 공분산 :  52.2222222222222
# plt.plot(x2,y2,'o')
# plt.show()

print()
# 두 데이터의 단위(스케일)에 따라 패턴이 일치할지라도 공분산의 크기가 달라진다.
# 그러므로 절대적 크기 판단이 어렵다. -> 공분산을 표준화해서 -1 < r < 1 범위로 만든 것이 상관계수(r)
# 피어슨 상관계수
print('x,y의 상관계수 : ', np.corrcoef(x,y)[0,1]) 
# 0.8663686463212855
print('x2,y2의 상관계수 : ', np.corrcoef(x2,y2)[0,1]) 
# 0.866368646321285
# => 매우 비슷한 값을 출력.

from scipy import stats
print("scipy 모듈 사용 : ", stats.pearsonr(x,y))

print()
# 비선형 데이터인 경우 공분산, 상관계수 의미없음.
m = [-3,-2,-1,0,1,2,3]
n = [9,4,1,0,1,4,9]
print('m,n의 공분산 : ', np.cov(m,n)[0,1])         # 0.0
print('m,n의 상관계수 : ', np.corrcoef(m,n)[0,1])  # 0.0
plt.plot(m,n,'o')
plt.show()



