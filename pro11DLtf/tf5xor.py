import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

# 1) 데이터 수집 및 가공
x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])  # XOR 게이트

model = Sequential()
model.add(Input(shape=(2,)))  # 입력층(Input layer)
# model.add(Dense(units=1))
# model.add(Activation('sigmoid'))
model.add(Dense(units=5, activation='relu')) # 은닉층(Hidden layer)
model.add(Dense(units=5, activation='relu')) # 은닉층(Hidden layer)
model.add(Dense(units=1, activation='sigmoid')) # 출력층(Output layer)
print(model.summary())  # 설계된 모델의 Layer, Parameter 수 확인 가능
# parameter = (입력 수 + 1) * 출력 수 

model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
history = model.fit(x, y, epochs=200, batch_size=1, verbose=2)
loss_metrics = model.evaluate(x, y)
print('loss_metrics : ', loss_metrics)   # loss_metrics :  [0.07437311112880707, 1.0]
# print(history.history)

pred = (model.predict(x=x) > 0.5).astype("int32")
print('예측 확률:\n', pred)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['accuracy'], label='accuracy')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend(loc='best')
plt.show()