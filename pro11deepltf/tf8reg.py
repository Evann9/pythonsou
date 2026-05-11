# 모델 생성 방법 3가지 수행
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np

# 공부 시간에 따른 성적 결과
xdata = np.array([1,2,3,4,5], dtype=np.float32).reshape(-1,1)
ydata = np.array([15,32,39,55,60], dtype=np.float32).reshape(-1, 1)

print('모델 생성 방법1 - Sequential API')
model = Sequential()
model.add(Input((1, )))
model.add(Dense(units=4, activation='relu'))
model.add(Dense(units=1, activation='linear'))
# model = Sequential([
#     model.add(Input((1, )),
#     model.add(Dense(units=4, activation='relu')),
#     model.add(Dense(units=1, activation='linear'))
# ])

print(model.summary())
opti = optimizers.SGD(learning_rate=0.001)
model.compile(loss='mse', optimizer=opti, metrics=['mse'])
history = model.fit(x=xdata, y=ydata, batch_size=1, epochs=100, verbose=2)
loss_metrics = model.evaluate(x=xdata, y=ydata)
print('loss_metrics : ', loss_metrics)
ypred = model.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred))
print('실제값 : ', ydata.ravel())
print('예측값 : ', ypred.ravel())

import matplotlib.pyplot as plt
plt.scatter(xdata, ydata, color='r', marker='o', label='real')
plt.plot(xdata, ypred, 'b--', label='pred')
plt.show()


# mse 변화량 시각화
plt.plot(history.history['mse'], label='mse')
plt.xlabel('epochs')
plt.legend()
plt.show()


print('\n 모델 생성 방법2 - Functional API')
# 유연한 구조 : 입력 자료로 여러 층을 공유하거나 다양한 종류의 입출력 모델 생성 가능
# 다중입력값 모델, 다중출력값 모델, 공유층 활용 모델, 데이터 흐름이 비순차적인 경우에도 효과적
from tensorflow.keras.models import Model
inputs = Input(shape=(1, ))
output1 = Dense(units=4, activation='relu')(inputs)
outputs = Dense(units=1, activation='linear')(output1)

model2 = Model(inputs, outputs)

opti2 = optimizers.SGD(learning_rate=0.001)
model2.compile(loss='mse', optimizer=opti2, metrics=['mse'])
history2 = model2.fit(x=xdata, y=ydata, batch_size=1, epochs=100, verbose=2)
loss_metrics2 = model2.evaluate(x=xdata, y=ydata)
print('loss_metrics2 : ', loss_metrics2)
ypred2 = model2.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred2))
print('실제값 : ', ydata.ravel())
print('예측값 : ', ypred2.ravel())

print('\n모델 생성 방법3 - Sub classing : Model을 상속 받아 직접 모델 생성')
class MyModel(Model):
    def __init__(self):
        super(MyModel, self).__init__()
        self.d1 = Dense(units=4, activation='relu')
        self.d2 = Dense(units=1, activation='linear')

    # x : input 매개변수
    def call(self, x):  # Input 클래스를 사용하지 않고 call 메소드의 input 매개변수 이용
        x = self.d1(x)
        return self.d2(x)
    
model3 = MyModel()
    
opti3 = optimizers.SGD(learning_rate=0.001)
model3.compile(loss='mse', optimizer=opti3, metrics=['mse'])
history3 = model3.fit(x=xdata, y=ydata, batch_size=1, epochs=100, verbose=2)
loss_metrics3 = model3.evaluate(x=xdata, y=ydata)
print('loss_metrics3 : ', loss_metrics3)
ypred3 = model3.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred3))
print('실제값 : ', ydata.ravel())
print('예측값 : ', ypred3.ravel())

print('\n모델 생성 방법3 - 1 : Custom Layer 층 사용')
from tensorflow.keras.layers import Layer

class MyLayer(Layer):
    def __init__(self, units=1, **kwargs):
        super(MyLayer, self).__init__(**kwargs)
        self.units = units

    def build(self, input_shape):   # 내부적으로 call() 호출
        print(f'build:input_shape={input_shape}')
        self.w = self.add_weight(shape=(input_shape[-1], self.units), initializer='random_normal', trainable=True)
        self.b = self.add_weight(shape=(self.units, ), initializer='zeros', trainable=True)

    def call(self, inputs):
        return tf.matmul(inputs, self.w) + self.b   # y = wx + b

class MLP(Model):
    def __init__(self, **kwargs):
        super(MLP, self).__init__(**kwargs)
        self.linear1 = MyLayer(2)
        self.linear2 = MyLayer(1)

    def call(self, inputs):
        net = self.linear1(inputs)
        net = tf.nn.relu(net)
        return self.linear2(net)
    
model4 = MLP()

opti4 = optimizers.SGD(learning_rate=0.001)
model4.compile(loss='mse', optimizer=opti4, metrics=['mse'])
history4 = model4.fit(x=xdata, y=ydata, batch_size=1, epochs=100, verbose=0)
loss_metrics4 = model4.evaluate(x=xdata, y=ydata)
print('loss_metrics4 : ', loss_metrics4)
ypred4 = model4.predict(xdata, verbose=0)

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(ydata, ypred4))
print('실제값 : ', ydata.ravel())
print('예측값 : ', ypred4.ravel())
    


