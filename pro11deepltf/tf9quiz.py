'''
문제1)
https://github.com/data-8/materials-fa17/blob/master/lec/galton.csv
data를 이용해 아버지 키로 아들의 키를 예측하는 회귀분석 모델을 작성하시오.
 - train / test 분리
 - Sequential api와 function api 를 사용해 모델을 만들어 보시오.
 - train과 test의 mse를 시각화 하시오
 - 새로운 아버지 키에 대한 자료로 아들의 키를 예측하시오.
'''

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
from sklearn.model_selection import train_test_split
import numpy as np
import pandas as pd

data = pd.read_csv('https://raw.githubusercontent.com/data-8/materials-fa17/refs/heads/master/lec/galton.csv')

print(data.head(2))
#   family  father  mother  midparentHeight  children  childNum  gender  childHeight
# 0      1    78.5    67.0            75.43         4         1    male         73.2
# 1      1    78.5    67.0            75.43         4         2  female         69.2

xdata = data['father']
ydata = data['childHeight']

x_train, x_test, y_train, y_test = train_test_split(xdata, ydata, test_size=0.3, random_state=42)

print('train:', x_train.shape, 'test:', x_test.shape)

print('Sequential API')
# Sequential API
model = Sequential()
model.add(Input((1, )))
model.add(Dense(units=4, activation='relu'))
model.add(Dense(units=1, activation='linear'))

print(model.summary())
opti = optimizers.SGD(learning_rate=0.001)
model.compile(loss='mse', optimizer=opti, metrics=['mse'])
history = model.fit(x=x_train, y=y_train, batch_size=1, epochs=30, verbose=2,  validation_data=(x_test, y_test))
loss_metrics = model.evaluate(x=x_test, y=y_test)
print('loss_metrics : ', loss_metrics)
ypred = model.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred))
print('실제값 : ', ydata[:5].ravel())
print('예측값 : ', ypred[:5].ravel())

import matplotlib.pyplot as plt

# mse 변화량 시각화
plt.plot(history.history['mse'], label='train mse')
plt.plot(history.history['val_mse'], label='test mse')
plt.xlabel('epochs')
plt.legend()
plt.show()



# ------------------------------------------
print()
print('Functional API')

# Functional API
from tensorflow.keras.models import Model
inputs = Input(shape=(1, ))
output1 = Dense(units=4, activation='relu')(inputs)
outputs = Dense(units=1, activation='linear')(output1)

model2 = Model(inputs, outputs)

opti2 = optimizers.SGD(learning_rate=0.001)
model2.compile(loss='mse', optimizer=opti2, metrics=['mse'])
history2 = model2.fit(x=x_train, y=y_train, batch_size=1, epochs=30, verbose=2,  validation_data=(x_test, y_test))
loss_metrics2 = model2.evaluate(x=x_test, y=y_test)
print('loss_metrics2 : ', loss_metrics2)
ypred2 = model2.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred2))
print('실제값 : ', ydata[:5].ravel())
print('예측값 : ', ypred2[:5].ravel())

# mse 변화량 시각화
plt.plot(history2.history['mse'], label='train mse')
plt.plot(history2.history['val_mse'], label='test mse')
plt.xlabel('epochs')
plt.legend()
plt.show()



new_x = np.array([165, 170, 175, 180, 185]).reshape(-1, 1)

print('\n----- 새로운 아버지 키 예측 -----')
new_pred1 = model.predict(new_x, verbose=0)
new_pred2 = model2.predict(new_x, verbose=0)

for i, h in enumerate(new_x.ravel()):
    print(f'아버지 키 {h}cm → Sequential: {new_pred1[i][0]:.2f}cm / Functional: {new_pred2[i][0]:.2f}cm')

