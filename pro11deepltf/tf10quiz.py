'''
문제2)
https://github.com/pykwon/python/tree/master/data
자전거 공유 시스템 분석용 데이터 train.csv를 이용하여 대여횟수에 영향을 주는 변수들을 골라 다중선형회귀분석 모델을 작성하시오.
모델 학습시에 발생하는 loss를 시각화하고 설명력을 출력하시오.
새로운 데이터를 input 함수를 사용해 키보드로 입력하여 대여횟수 예측결과를 콘솔로 출력하시오.
'''

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv")

print(data.head(5), data.shape)
#               datetime  season  holiday  workingday  weather  temp   atemp  humidity  windspeed  casual  registered  count
# 0  2011-01-01 00:00:00       1        0           0        1  9.84  14.395        81        0.0       3          13     16
# 1  2011-01-01 01:00:00       1        0           0        1  9.02  13.635        80        0.0       8          32     40
# 2  2011-01-01 02:00:00       1        0           0        1  9.02  13.635        80        0.0       5          27     32
# 3  2011-01-01 03:00:00       1        0           0        1  9.84  14.395        75        0.0       3          10     13
# 4  2011-01-01 04:00:00       1        0           0        1  9.84  14.395        75        0.0       0           1      1
# (10886, 12)

# 대여횟수(count)에 영향을 주는 변수 선택
# casual, registered는 count의 구성 요소(데이터 누수)이므로 제외, datetime은 문자열이므로 제외
feature_cols = ['season', 'holiday', 'workingday', 'weather', 'temp', 'atemp', 'humidity', 'windspeed']
xdata = data[feature_cols].values
ydata = data['count'].values.reshape(-1, 1)

print('xdata shape:', xdata.shape, 'ydata shape:', ydata.shape)

# 정규화
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()

x_scaled = scaler_x.fit_transform(xdata)
y_scaled = scaler_y.fit_transform(ydata)

# 모델 구성
model = Sequential()
model.add(Input((len(feature_cols),)))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=1, activation='linear'))

print(model.summary())

opti = optimizers.Adam(learning_rate=0.001)
model.compile(loss='mse', optimizer=opti, metrics=['mse'])

history = model.fit(x=x_scaled, y=y_scaled, batch_size=32, epochs=100, verbose=2,
                    validation_split=0.2)

# loss 시각화
plt.figure(figsize=(8, 4))
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.title('Training Loss')
plt.xlabel('epochs')
plt.ylabel('loss (mse)')
plt.legend()
plt.tight_layout()
plt.show()

# 설명력(R²) 출력
from sklearn.metrics import r2_score

ypred_scaled = model.predict(x_scaled, verbose=0)
ypred = scaler_y.inverse_transform(ypred_scaled)

print('설명력(R²):', r2_score(ydata, ypred))
print('실제값 샘플:', ydata[:5].ravel())
print('예측값 샘플:', ypred[:5].ravel().astype(int))

# 새로운 데이터 입력 및 예측
print('\n----- 새로운 데이터 예측 -----')
print('입력 항목: season, holiday, workingday, weather, temp, atemp, humidity, windspeed')
print('  season: 1=봄 2=여름 3=가을 4=겨울')
print('  holiday/workingday: 0 또는 1')
print('  weather: 1=맑음 2=흐림 3=눈/비')
print('  예시: 2, 0, 1, 1, 25.0, 28.0, 50, 10.0')
vals = input('값을 쉼표로 구분하여 입력하세요: ')
new_data = np.array([float(v.strip()) for v in vals.split(',')]).reshape(1, -1)
new_scaled = scaler_x.transform(new_data)
new_pred_scaled = model.predict(new_scaled, verbose=0)
new_pred = scaler_y.inverse_transform(new_pred_scaled)
print(f'예측 대여횟수: {new_pred[0][0]:.0f}회')



