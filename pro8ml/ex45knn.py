# 최근접 이웃(K-Nearest Neighbors)
# 알고리즘은 우리가 예측하려고 임의의 데이터와 가장 가까운 거리의
# 데이터 k개를 찾아 다수결에ㅐ 의해 데이터를 예측하는 방법

from sklearn.neighbors import KNeighborsClassifier
import matplotlib.pyplot as plt

train = [
    [5,3,2],
    [1,3,5],
    [4,5,6]
]
label = [0, 1, 1]


plt.plot(train, 'o')
plt.xlim([-1, 5])
plt.ylim([0, 8])
plt.show()

kmodel = KNeighborsClassifier(n_neighbors=3, weights='distance')
kmodel.fit(train, label)
pred = kmodel.predict(train)
print('예측값 : ', pred)
print('실제값 : ', label)
print('정확도 : ', kmodel.score(train, label))

# 새로운 데이터
new_data = [[1, 2, 9], [6,2,1]]
new_pred = kmodel.predict(new_data)
print('새로운 데이터 예측 결과 : ', new_pred)
