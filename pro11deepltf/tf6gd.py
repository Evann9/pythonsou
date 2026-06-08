# 비용 함수(Cost Function)은 머신러닝 모델의 예측값과 실제값 간의 오차를 
# 수치화하여 모델의 성능을 평가하는 함수입니다.
# 목적은 이 비용 함수의 값을 최소화하는 파라미터를 찾는 것입니다.
# 수식은
# 인공 신경망은 델타규칙(경사하강법)으로 W(weight)와 B(bias)를 갱신한다.
# 경사하강법은 최소제곱법 대신에 평균제곱오차(MSE)를 정의하고,
# 그 오차를 최소화 하기 위해 경사하강법을 반복적으로 사용해 파라미터를 갱신한다.

# 비용 함수 구하기
import math
import numpy as np

real = np.array([10, 9, 3, 2, 11])    # y의 실제값
# pred = np.array([11, 5, 2, 4, 3])     # 모델 예측값 차이가 큰 경우
pred = np.array([10, 8, 3, 4, 10])    # 모델 예측값 차이가 작은 경우
cost = 0
for i in range(len(real)):
    cost += math.pow(pred[i] - real[i], 2)
    print(cost)

print('cost : ' , cost / len(real))
# 실제값과 예측값의 차이가 작을 때 cost는 0에 근사한다.
# wx + b 수식에서 w와 b를 최적의 추세선이 만들어지도록 갱신해야 한다.

print('최적의 W(weight, 가중치) 얻기의 이해')
import tensorflow as tf
import matplotlib.pyplot as plt
import koreanize_matplotlib

x = [1,2,3,4,5]
y = [1,2,3,4,5]
b = 0   # bias는 편의상 0을 준다.

# 선형회귀 모델 수식 hypothesis = w * x + b
# cost = tf.reduce_sum(tf.pow(hypothesis - y, 2)) / len(y)

# 시각화를 위한 변수 선언
w_val = []
cost_val = []

for i in range(-30, 50):
    feed_w = i * 0.1
    # print('feed_w : ', feed_w)
    hypothesis = tf.multiply(feed_w, x) + b
    cost = tf.reduce_mean(tf.square(hypothesis - y))
    cost_val.append(cost)
    w_val.append(feed_w)
    print(f'{i} ,cost:{cost.numpy()}, weight:{feed_w}')

plt.plot(w_val, cost_val, marker='o')
plt.xlabel('w(가중치)')
plt.ylabel('cost(손실,비용)')
plt.show()