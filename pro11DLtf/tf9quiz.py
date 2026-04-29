# data를 이용해 아버지 키로 아들의 키를 예측하는 회귀분석 모델을 작성하시오.
#  - train / test 분리
#  - Sequential api와 function api 를 사용해 모델을 만들어 보시오.
#  - train과 test의 mse를 시각화 하시오
#  - 새로운 아버지 키에 대한 자료로 아들의 키를 예측하시오.

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

data = pd.read_csv('https://raw.githubusercontent.com/data-8/materials-fa17/refs/heads/master/lec/galton.csv')
print(data.head(10), data.shape)

# 남자아이 데이터만 사용
data = data[data['gender'] == 'male'].copy()
print(data.head(10), data.shape)

#   family  father  mother  midparentHeight  children  childNum  gender  childHeight
# 0      1    78.5    67.0            75.43         4         1    male         73.2
# 1      1    78.5    67.0            75.43         4         2  female         69.2
# 2      1    78.5    67.0            75.43         4         3  female         69.0
# 3      1    78.5    67.0            75.43         4         4  female         69.0
# 4      2    75.5    66.5            73.66         4         1    male         73.5
# 5      2    75.5    66.5            73.66         4         2    male         72.5
# 6      2    75.5    66.5            73.66         4         3  female         65.5
# 7      2    75.5    66.5            73.66         4         4  female         65.5
# 8      3    75.0    64.0            72.06         2         1    male         71.0
# 9      3    75.0    64.0            72.06         2         2  female         68.0 (934, 8)

# father 키로 남자아이의 childHeight 예측
xdata = data[['father']].values
ydata = data['childHeight'].values.reshape(-1,1)

print(xdata.shape, ydata.shape)
# (934, 1) (934, 1)
# x, y 정규화하기
# x만 정규화하거나, 둘 다 정규화를 하지 않으면 설명력이 음수로 나옴
from sklearn.preprocessing import MinMaxScaler

# 객체 생성
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

# 학습 데이터로 기준 잡기 (fit) 및 변환 (transform)
x_scaled = scaler_x.fit_transform(xdata)
y_scaled = scaler_y.fit_transform(ydata)
print(x_scaled[:5])
# [[1.        ]
#  [1.        ]
#  [1.        ]
#  [1.        ]
#  [0.81818182]]
print(y_scaled[:5])
# [[0.74782609]
#  [0.57391304]
#  [0.56521739]
#  [0.56521739]
#  [0.76086957]]

from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y_scaled, shuffle=True, test_size=0.3, random_state=123) #stratify는 회귀에서는 안줌.
print(x_train.shape, x_test.shape, y_train.shape, y_test.shape)
# (653, 1) (281, 1) (653, 1) (281, 1)

# Sequential api를 사용한 모델
model_seq = Sequential()
model_seq.add(Input(shape=(1,)))
model_seq.add(Dense(16, activation='relu'))
model_seq.add(Dense(8, activation='relu'))
model_seq.add(Dense(1, activation='linear'))

print(model_seq.summary())

model_seq.compile(optimizer='adam', loss='mse', metrics=['mse'])

history_seq = model_seq.fit(x_train, y_train, batch_size=32, epochs=100, verbose=2, validation_split=0.2) 
# validation_split=0.2 : train data 중 20%를 학습 중 검증용으로 사용
ev_loss = model_seq.evaluate(x_test, y_test, verbose=0)
print('evaluation loss:', ev_loss)

# history값 확인
print('history : ', history_seq.history)
print('history loss : ', history_seq.history['loss'])
print('history mse : ', history_seq.history['mse'])
print('history val loss : ', history_seq.history['val_loss'])
print('history val mse : ', history_seq.history['val_mse'])

# mse 시각화
plt.figure(figsize=(10, 6))
plt.plot(history_seq.history['mse'], label='train_mse')
plt.plot(history_seq.history['val_mse'], label='val_mse')
plt.title('Model mse')
plt.ylabel('mse')
plt.xlabel('Epoch')
plt.legend()
plt.grid()
plt.show()

from sklearn.metrics import r2_score
print('설명력 : ', r2_score(y_test, model_seq.predict(x_test)))
# 설명력 :  -0.0018943632018406653 -> ???

# predict
pred = model_seq.predict(x_test[:5])
print('실제값 : ', y_test[:5].ravel())
print('예측값 : ', pred.ravel())
# 실제값 :  [0.52173913 0.32608696 0.39130435 0.45652174 0.5       ]
# 예측값 :  [0.46847308 0.46847308 0.46847308 0.46847308 0.46847308]

print('\n\nFunctional api를 사용한 방법 --------------')
from tensorflow.keras.models import Model

# 입력층 정의
inputs = Input(shape=(1,), name='input_layer')

# 은닉층 1
x = Dense(units=16, activation='relu', name='hidden_layer1')(inputs)

# 은닉층 2
x = Dense(units=8, activation='relu', name='hidden_layer2')(x)

# 출력층
outputs = Dense(units=1, activation='linear', name='output_layer')(x)

# 모델 생성(입력, 출력을 연결)
model_func = Model(inputs=inputs, outputs=outputs)
print(model_func.summary())

# 모델 컴파일
model_func.compile(optimizer='adam', loss='mse', metrics=['mse'])

# 모델 학습
history_func = model_func.fit(x_train, y_train, batch_size=32, epochs=100, verbose=2, validation_split=0.2)

# evaluation
func_ev_loss = model_func.evaluate(x_test, y_test, verbose=0)
print('evaluation loss:', func_ev_loss)

# 설명력 확인
print('설명력 : ', r2_score(y_test, model_func.predict(x_test)))
# 설명력 :  0.08034843307652939

# predict
pred = model_func.predict(x_test[:5])
print('실제값 : ', y_test[:5].ravel())
print('예측값 : ', pred.ravel())
# 실제값 :  [0.52173913 0.32608696 0.39130435 0.45652174 0.5       ]
# 예측값 :  [0.47385493 0.49304354 0.5026379  0.4162889  0.49304354]

# mse 시각화
plt.figure(figsize=(10, 6))
plt.plot(history_func.history['mse'], label='train_mse')
plt.plot(history_func.history['val_mse'], label='val_mse')
plt.title('Model mse')
plt.ylabel('mse')
plt.xlabel('Epoch')
plt.legend()
plt.grid()
plt.show()

# 새아빠 키로 예측하기
# 새로운 아버지 키 데이터 준비 (2차원 배열 형태 유지)
new_father = np.array([[70.0], [67.0], [78.0]]) 

# 기존 학습 시 사용했던 'scaler'를 그대로 사용하여 변환
new_father_scaled = scaler_x.transform(new_father)

print(f"새로운 아버지 키: {new_father}")
print(f"새로운 아버지 키(정규화): {new_father_scaled}")
# 새로운 아버지 키: [[70.]]
# 새로운 아버지 키(정규화): [[0.48484848]]

# 각 모델로 예측
pred_seq_scaled = model_seq.predict(new_father_scaled)
pred_func_scaled = model_func.predict(new_father_scaled)

print(f'Sequential 모델 예측 자식 키(정규화): {pred_seq_scaled}')
print(f'Functional 모델 예측 자식 키(정규화): {pred_func_scaled}')
# Sequential 모델 예측 자식 키(정규화): [[0.46847308]]
# Functional 모델 예측 자식 키(정규화): [[0.47294834]]

# 예측된 키를 원래 키로 돌리기(inverse_transform)
pred_seq_original = scaler_y.inverse_transform(pred_seq_scaled)
pred_func_original = scaler_y.inverse_transform(pred_func_scaled)


print(f"Sequential 모델 예측 아들 키: {pred_seq_original}")
print(f"Functional 모델 예측 아들 키: {pred_func_original}")
# Sequential 모델 예측 아들 키: [[66.77488]]
# Functional 모델 예측 아들 키: [[66.877815]]
