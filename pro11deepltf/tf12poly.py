# 다항회귀 : 데이터가 비선형 분포인 경우
# 회귀선이 2차 3차 함수... 등의 곡선이 됨
# 다항회귀는 하나의 feature에 대해 차수를 확장해가며 단항식을 다항식으로 도출

import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

np.random.seed(7)
tf.random.set_seed(7)

# 가상의 feature와 label 만들기
x = np.linspace(-3, 3, 40).reshape(-1, 1)
print(x[:3])
# y = x제곱 + x + 2 + noise
y = (x[:, 0] ** 2) + x[:, 0] + 2 + np.random.normal(0, 1.5, size=len(x))
print(y[:3])

# plt.scatter(x, y)
# plt.show()

# R2 score 계산 함수
def r2_score_np(y_true, y_pred):
    ss_res = np.sum((y_true - y_pred) ** 2) # 잔차제곱의 합
    ss_tot = np.sum((y_true - np.mean(y_true)) ** 2)
    return 1 - (ss_res / ss_tot)

# 선형회귀 모델
linear_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(1,)),
    tf.keras.layers.Dense(units=1, activation='linear')
])

linear_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.05), loss='mse')
linear_model.fit(x, y, epochs=500, verbose=0)
y_pred_linear = linear_model.predict(x, verbose=0)

# 다항회귀
# x_poly = [x, x^2]
x_poly = np.column_stack([
    x[:, 0], x[:, 0] ** 2
]).astype(np.float32)
print(x_poly[:3])

poly_model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(2,)),
    tf.keras.layers.Dense(units=1, activation='linear')
])

poly_model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=0.05), loss='mse')
poly_model.fit(x_poly, y, epochs=500, verbose=0)
y_pred_poly = poly_model.predict(x_poly, verbose=0)

# 부드러운 곡선을 그리기 위한 x축 데이터
x_plot = np.linspace(x.min(), x.max(), 300).reshape(-1, 1).astype(np.float32)
y_plot_linear = linear_model.predict(x_plot, verbose=0)

# 예측할 때도 x와 x^2을 함께 넣어야 함 (그래프에 그릴 x값(x_plot)도 다항회귀 모델이 입력받을 수 있도록 변환)
x_plot_poly = np.column_stack([
    x_plot[:, 0],
    x_plot[:, 0] ** 2
]).astype(np.float32)
y_plot_poly = poly_model.predict(x_plot_poly, verbose=0)

# 성능 계산
r2_linear = r2_score_np(y, y_pred_linear)
r2_poly = r2_score_np(y, y_pred_poly)
print('r2_linear : ', r2_linear)
print('r2_poly : ', r2_poly)

# 시각화
plt.figure(figsize=(9, 6))
plt.scatter(x, y, label='data')
plt.plot(x_plot, y_plot_linear, label=f'Linear Regression(R2={r2_linear:.3f})')
plt.plot(x_plot, y_plot_poly, label=f'Poly Regression(R2={r2_poly:.3f})')
plt.xlabel('feature')
plt.ylabel('label')
plt.legend()
plt.grid(True)
plt.show()