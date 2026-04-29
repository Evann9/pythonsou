# 다중선형회귀 (tv  radio  newspaper)가 sales에 얼마나 영향을 주는지 파악

import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head())
del data['no']
print(data.head())

# Check for and drop any NaN values to prevent Input contains NaN error
data = data.dropna()

fdata = data[['tv', 'radio', 'newspaper']]
ldata = data[['sales']]
print(fdata.head())
print(ldata.head())

from sklearn.preprocessing import MinMaxScaler, minmax_scale, StandardScaler

# 정규화
# scaler = MinMaxScaler()
# fedata = scaler.fit_transform(fdata)
# print(fedata[:3])
fedata = minmax_scale(fdata, axis=0, copy=True)
print(fedata[:3])

# train / test 분리
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(fedata, ldata, test_size=0.3, random_state=123) # stratify는 회귀에선 안줌
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape) # (140, 3) (60, 3) (140, 1) (60, 1)

# 전처리가 모두 끝난 경우 모델 설계 및 실행
model = Sequential()
model.add(Input(shape=(3,)))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='linear'))  # activation='linear' 생략 가능
print(model.summary())

# 1. pip install pydot
# 2. Install Graphviz software (https://graphviz.org/download/)
# 3. Add Graphviz bin folder to System PATH
# 케라스 모델 구조를 이미지 파일로 저장
tf.keras.utils.plot_model(model, to_file='aaa.png', show_shapes=True, show_layer_names=True, show_dtype=True, show_layer_activations=True, rankdir='TB',dpi=96)

model.compile(optimizer='adam', loss='mse', metrics=['mse'])
history = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2)
ev_loss = model.evaluate(x_test, y_test, verbose=0)
print('ev_loss : ', ev_loss) # [5.8914103507995605, 5.8914103507995605]

# history 값 확인
print('history : ', history.history)
print('history loss : ', history.history['loss'])
print('history val_loss : ', history.history['val_loss'])
print('history mse : ', history.history['mse'])
print('history val_mse : ', history.history['val_mse'])

# loss 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.legend()
plt.show()

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_test, model.predict(x_test))) # 0.7812

# predict
pred = model.predict(x_test[:5])
print('예측값 : ', pred.ravel())
print('실제값 : ', y_test.values[:5].ravel())
# 예측값 :  [13.574885  8.743219 15.022896 10.826119 13.665731]
# 실제값 :  [11.4  8.8 14.7 10.1 14.6]

print('\n\nFunctional API')
# 다중입출력, 분기구조, 병합구조 등 복잡한 신경망 모델 작성시 효과적
from tensorflow.keras.models import Model
# 입력층
inputs = Input(shape=(3,), name="input_layer")
# 은닉층
x = Dense(units=16, activation='relu', name="hidden_layer1")(inputs)
x = Dense(units=8, activation='relu', name="hidden_layer2")(x)
# 출력층
outputs = Dense(units=1, activation='linear', name="output_layer")(x)
# 모델 생성 (입력과 출력을 연결)
func_model = Model(inputs=inputs, outputs=outputs)
print(func_model.summary())

func_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

history = func_model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2)

ev_loss = func_model.evaluate(x_test, y_test, verbose=0)
print('ev_loss : ', ev_loss) 

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_test, func_model.predict(x_test))) # 0.8308