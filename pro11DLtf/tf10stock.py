# 주식 데이터로 다중선형회귀모델 작성
# 전날 데이터로 다음날 종가 예측
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/stockdaily.csv")
print(datas.head(2), datas.shape)  # 732
#          Open        High         Low   Volume       Close
# 0  828.659973  833.450012  828.349976  1247700  831.659973
# 1  823.020020  828.070007  821.655029  1597800  828.070007

# feature
x_data = datas.iloc[:, 0:-1] 
print(x_data.shape) # (732, 4)
scaler = MinMaxScaler(feature_range=(0,1)) # 정규화
x_data = scaler.fit_transform(x_data)
print(x_data[:2])
# print(scaler.inverse_transform(x_data[:2]))

# label
y_data = datas.iloc[:, -1]  # 종가
print(y_data[:2]) 
print()
print(x_data[0], y_data[0])
print(x_data[1], y_data[1])

# x_data와 y_data를 한칸 씩 어긋나게 맞추기 위한 전처리
x_data = np.delete(x_data, -1, axis=0)
y_data = np.delete(y_data, 0)
print(x_data[0], y_data[0])

print('train / test split 없이 모델 작성')
model = Sequential()
model.add(Input(shape=(4,)))
model.add(Dense(units=1, activation='linear'))
print(model.summary())

model.compile(loss='mse', optimizer='sgd', metrics=['mse'])  # optimizer을 종류 별로 돌려보면서 성능이 우수한 것을 찾아야 함.
model.fit(x_data, y_data, epochs=200, verbose=0)
ev_loss = model.evaluate(x_data, y_data, verbose=0)
print('evaluate result : ', model.evaluate(x_data, y_data, verbose=0))
# evaluate result :  [62.96637725830078, 62.96637725830078]

# R2 score (train test 없이)
from sklearn.metrics import r2_score
pred = model.predict(x_data)
print("train test 없이 설명력 보기 : " , r2_score(y_data, pred)) 
# 0.9938598651500494 -> 오버피팅(과적합이 매우 의심스러움)

# 시각화
plt.plot(y_data, 'b', label='real')
plt.plot(pred, 'r--', label='pred')
plt.legend(loc='best')
plt.show()

print()
print('train / test split 후 모델 작성')
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(x_data, y_data, test_size=0.3, random_state=123, shuffle=False) 
# 주의 : 시계열 데이터는 shuffle=False
print(x_train.shape, x_test.shape) # (511, 4) (220, 4)

model2 = Sequential()
model2.add(Input(shape=(4,)))
model2.add(Dense(units=1, activation='linear'))
print(model2.summary())

model2.compile(loss='mse', optimizer='sgd', metrics=['mse'])  # optimizer을 종류 별로 돌려보면서 성능이 우수한 것을 찾아야 함.
model2.fit(x_train, y_train, epochs=200, verbose=0, validation_split=0.15)
print('evaluate result : ', model2.evaluate(x_test, y_test, verbose=0))

# R2 score (train test 없이)
from sklearn.metrics import r2_score
pred2 = model2.predict(x_test)
print("train test R2 score : " , r2_score(y_test, pred2))  
#  0.9483737043232252 : train / test split
#  0.8393947594319192 : train / test split + validation_split

# 시각화
plt.plot(y_test, 'b', label='real')
plt.plot(pred2, 'r--', label='pred')
plt.legend(loc='best')
plt.show()

# 딥러닝의 이슈 : 최적화와 일반화
