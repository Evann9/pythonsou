# 단순선형회귀 모델 작성
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

# feature, label을 2차원 형태로 입력하기 위함
xdata = np.array([1,2,3,4,5], dtype=np.float32).reshape(-1,1)
ydata = np.array([1.2,2.0,3.0,3.5,5.5]).reshape(-1,1)
print('상관계수 : ', np.corrcoef(xdata.ravel(), ydata.ravel()))  # 0.97494708

model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(units=5, activation='relu'))
model.add(Dense(units=1, activation='linear'))  # 선형회귀 모델 : 계산된 값을 그대로 출력
print(model.summary())

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])
# loss='mse' : 회귀분석 모델에서는 mean_squared_error 사용

model.fit(xdata, ydata, epochs=100, batch_size=1, verbose=1, shuffle=True)
loss_eval = model.evaluate(xdata, ydata)
print('loss_eval : ', loss_eval)

pred = model.predict(xdata)
print('예측값 : ', pred.ravel())
print('실제값 : ', ydata.ravel())

print('결정 계수(R2, 설명력)')
from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, pred)) # 0.9426

import matplotlib.pyplot as plt
plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, pred, 'b--', label='pred')
plt.show()

# 새로운 값 예측
new_x = np.array([1.5, 5.7, -3.0]).reshape(-1,1)
new_pred = model.predict(new_x)
print('새 값 예측값 : ', new_pred.ravel()) #  [1.5976572  6.1775813  0.43078417]
