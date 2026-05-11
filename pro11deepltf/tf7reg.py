# 단순선형회쉬 모델 작성
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam
import numpy as np

xdata = np.array([1,2,3,4,5], dtype='float32').reshape(-1, 1)
ydata = np.array([1.2, 2.0, 3.0, 3.5, 5.5])
print('상관 계수 : ', np.corrcoef(xdata.ravel(), ydata.ravel()))    # 0.97494708

model = Sequential()
model.add(Input((1, )))
model.add(Dense(units=5, activation='relu'))    
model.add(Dense(units=1, activation='linear'))  # 'linear' : 계산된 값을 그대로 출력
print(model.summary())
# Model: "sequential"
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
# ┃ Layer (type)                         ┃ Output Shape                ┃         Param # ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
# │ dense (Dense)                        │ (None, 5)                   │              10 │
# ├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
# │ dense_1 (Dense)                      │ (None, 1)                   │               6 │
# └──────────────────────────────────────┴─────────────────────────────┴─────────────────┘
#  Total params: 16 (64.00 B)
#  Trainable params: 16 (64.00 B)
#  Non-trainable params: 0 (0.00 B)
# None

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])
# loss='mse' : 회귀분석 모델에서는 mean_squared_error 사용

model.fit(x=xdata, y=ydata, epochs=100, batch_size=1, verbose=1, shuffle=True)
# shuffle=True : default

loss_eval = model.evaluate(x=xdata, y=ydata)
print('loss_eval : ', loss_eval)

pred = model.predict(xdata)
print('pred : ', pred.ravel())  # [1.0760864 2.1811159 3.286145  4.391174  5.496203 ]
print('real : ', ydata.ravel()) # [1.2 2.  3.  3.5 5.5]

print('결정계수(R2, 설명력)')
from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, pred))   # 0.9138798256184778

import matplotlib.pyplot as plt
plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, pred, 'b--', label='pred')
plt.show()

# 새로운 값으로 예측
new_x = np.array([1.5, 5.7, -3.0]).reshape(-1, 1)
new_pred = model.predict(new_x)
print('새값 예측 결과 : ', new_pred.ravel())
# [ 1.6286011  6.269723  -1.1058154]
