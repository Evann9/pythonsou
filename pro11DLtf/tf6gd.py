# cost function(비용함수)
# 예측값과 실제값의 차이(오차)를 수치화하여 모델의 성능을 평가하는 지표 
# 주로 전체 데이터셋에 대한 오차의 평균을 최소화하는 파라미터를 찾기 위해 사용
# 수식(MSE) : Cost(W, b) = 1/n * Σ(y_pred - y_actual)²
# 인공신경망은 델타 규칙(경사하강법)으로 W(weight)와 B(bias)를 갱신
# 경사하강법은 최소제곱법 대신 평균제곱오차(MSE)를 정의하고, 
# 그 오차를 최소화 하기 위해 경사하강법을 반복적으로 사용해 파라미터를 갱신한다.

# 비용 함수 구하기
import math
import numpy as np


real = [10, 9, 3, 2, 11]  # y의 실제값
# pred = [11, 5, 2, 4, 3]   # 모델 예측값
pred = np.array([10, 8, 3, 4, 10])
cost = 0
for i in range(len(real)):
    cost += math.pow(pred[i] - real[i], 2)
    print(cost)

print('cost : ', cost / len(real))
# 실제값과 예측값의 차이가 작을 때 cost는 0에 근사한다.
# wx + b 수식에서 w와 b를 최적의 추세선이 만들어지도록 갱신해야 한다.

print('최적의 W(weight, 가중치) 얻기')
import tensorflow as tf
import matplotlib.pyplot as plt
import koreanize_matplotlib

x = [1,2,3,4,5]
y = [1,2,3,4,5]
b = 0          # bias는 편의상 0으로 둔다

# 선형회귀 모델 수식 hypothesis = w * x + b

# 시각화를 위한 변수 선언
w_val = []
cost_val = []
for i in range(-50, 50):
    feed_w = i * 0.1
    hypothesis = tf.multiply(feed_w, x) + b
    cost = tf.reduce_mean(tf.square(hypothesis - y))
    cost_val.append(cost)
    w_val.append(feed_w)
    print(f"{i} , cost : {cost}, w : {feed_w}")

plt.plot(w_val, cost_val, marker='o')
plt.xlabel('W(가중치)')
plt.ylabel('cost(손실, 비용)')
plt.show()