# 모델 생성 방법 3가지 수행

import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras import optimizers
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

np.random.seed(1)
tf.random.set_seed(1)

# 공부 시간에 따른 성적 결과 예측
xdata = np.array([1,2,3,4,5], dtype=np.float32).reshape(-1,1)
ydata = np.array([15, 32, 39, 55, 60], dtype=np.float32).reshape(-1,1)

print('모델 생성 방법 1 - Sequential API')
model = Sequential()
model.add(Input(shape=(1,)))
model.add(Dense(
    units=1,
    activation='linear',
    kernel_initializer='zeros',
    bias_initializer='zeros'
))
# 단순선형회귀이므로 은닉층 없이 y = wx + b 형태로 학습한다.
# ReLU 은닉층을 쓰면 작은 데이터에서는 모든 예측값이 같은 값으로 수렴할 수 있다.
# model = Sequential([
#     Input(shape=(1,)),
#     Dense(units=1, activation='linear')
# ])
print(model.summary())
opti = optimizers.Adam(learning_rate=0.05)
model.compile(loss='mse', optimizer=opti, metrics=['mse'])
history = model.fit(xdata, ydata, epochs=500, batch_size=1, verbose=1, shuffle=False)
loss_metrics = model.evaluate(xdata, ydata)
print('loss_metrics : ', loss_metrics)
ypred = model.predict(xdata, verbose=0)

print('설명력 : ', r2_score(ydata, ypred))
print('예측값 : ', ypred)
print('실제값 : ', ydata)

plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, ypred, 'b--', label='pred')
plt.legend(loc='best')
plt.show()

# mse 변화량 시각화
plt.plot(history.history['mse'], label='mse')
plt.xlabel('epoch')
plt.ylabel('mse')
plt.legend(loc='best')
plt.show()


print('\n모델 생성 방법 2 - Functional API')
# 유연한 구조 : 입력 자료로 여러 층을 공유하거나 다양한 종류의 입출력 모델 생성 가능
# 다중입력값 모델, 다중출력값 모델, 공유층 활용 모델, 데이터 흐름이 비순차적인 경우에도 효과적
inputs = Input(shape=(1,))
outputs = Dense(
    units=1,
    activation='linear',
    kernel_initializer='zeros',
    bias_initializer='zeros'
)(inputs)  # 단순선형회귀 : y = wx + b

model2 = Model(inputs=inputs, outputs=outputs, name='functional_linear_model')
print(model2.summary())
opti2 = optimizers.Adam(learning_rate=0.05)
model2.compile(loss='mse', optimizer=opti2, metrics=['mse'])
history2 = model2.fit(xdata, ydata, epochs=500, batch_size=1, verbose=1, shuffle=False)
loss_metrics2 = model2.evaluate(xdata, ydata)
print('loss_metrics : ', loss_metrics2)
ypred2 = model2.predict(xdata, verbose=0)

print('설명력 : ', r2_score(ydata, ypred2))
print('예측값 : ', ypred2)
print('실제값 : ', ydata)

plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, ypred2, 'g--', label='pred2')
plt.legend(loc='best')
plt.show()

plt.plot(history2.history['mse'], label='mse')
plt.xlabel('epoch')
plt.ylabel('mse')
plt.legend(loc='best')
plt.show()


print('\n모델 생성 방법 3 - Subclassing API')


class LinearModel(Model):
    def __init__(self):
        super().__init__()
        self.dense = Dense(
            units=1,
            activation='linear',
            kernel_initializer='zeros',
            bias_initializer='zeros'
        )

    def call(self, inputs):
        return self.dense(inputs)


model3 = LinearModel()
model3.build(input_shape=(None, 1))
print(model3.summary())
opti3 = optimizers.Adam(learning_rate=0.05)
model3.compile(loss='mse', optimizer=opti3, metrics=['mse'])
history3 = model3.fit(xdata, ydata, epochs=500, batch_size=1, verbose=1, shuffle=False)
loss_metrics3 = model3.evaluate(xdata, ydata)
print('loss_metrics : ', loss_metrics3)
ypred3 = model3.predict(xdata, verbose=0)

print('설명력 : ', r2_score(ydata, ypred3))
print('예측값 : ', ypred3)
print('실제값 : ', ydata)

plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, ypred3, 'm--', label='pred3')
plt.legend(loc='best')
plt.show()

plt.plot(history3.history['mse'], label='mse')
plt.xlabel('epoch')
plt.ylabel('mse')
plt.legend(loc='best')
plt.show()
