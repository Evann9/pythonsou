import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

# 1) 데이터 수집 및 가공
x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[1]]) # XOR 게이트

model = Sequential()
model.add(Input(shape=(2, )))       # 입력층(input layer)
# model.add(Dense(units=1))
# model.add(Activation('sigmoid'))
model.add(Dense(units=5, activation='relu'))        # 은닉층(hidden layer)
model.add(Dense(units=5, activation='relu'))        # 은닉층(hidden layer)
model.add(Dense(units=1, activation='sigmoid'))     # 출력층(output layer)
print(model.summary())  # 설계된 모델의 Layer, Parameter 수 확인
# Parameter 수 : (입력수 + 1) * 출력수
# Model: "sequential"
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
# ┃ Layer (type)                         ┃ Output Shape                ┃         Param # ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
# │ dense (Dense)                        │ (None, 5)                   │              15 │
# ├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
# │ dense_1 (Dense)                      │ (None, 5)                   │              30 │
# ├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
# │ dense_2 (Dense)                      │ (None, 1)                   │               6 │
# └──────────────────────────────────────┴─────────────────────────────┴─────────────────┘
#  Total params: 51 (204.00 B)
#  Trainable params: 51 (204.00 B)
#  Non-trainable params: 0 (0.00 B)
# None

model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
history = model.fit(x=x, y=y, epochs=200, batch_size=1, verbose=1)
loss_metrics = model.evaluate(x=x, y=y)
print('loss_metrics : ', loss_metrics)
print(history.history)

proba = model.predict(x=x, verbose=0)
pred = (proba > 0.5).astype('int32')
print('pred : ', pred)

import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['accuracy'], label='accuracy')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend(loc='best')
plt.show()

