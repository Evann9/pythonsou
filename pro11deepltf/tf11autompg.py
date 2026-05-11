# 다중선형회귀 : 자동차 연비 예측
# 조기종료 코드 추가

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv")
print(datas.head(2))
print(datas.info())
del datas['car name']
datas = datas.dropna()
print(datas.isna().sum)

datas.drop(['cylinders', 'acceleration', 'model year', 'origin'], axis='columns', inplace=True)
print(datas.head(2))

# sns.pairplot(datas[['mpg', 'displacement', 'horsepower', 'weight']])
# plt.show()

# train / test split
train_dataset = datas.sample(frac=0.7, random_state=123)
print(train_dataset[:2], train_dataset.shape)   # (274, 4)
test_dataset = datas.drop(train_dataset.index)
print(train_dataset[:2], train_dataset.shape)   # (118, 4)

# 표준화 : (요소값 - 평균) / 표준편차
train_stat = train_dataset.describe()
train_stat.pop('mpg')
print(train_stat)
train_stat = train_stat.transpose() # 전치
print(train_stat)

def stdscale_func(x):
    return (x - train_stat['mean']) / train_stat['std']

# print(stdscale_func(train_dataset[:3]))
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop(['mpg'], axis='columns')
print(st_train_data[:3])

st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop(['mpg'], axis='columns')
print(st_test_data[:3])

train_label = train_dataset.pop('mpg')
print(train_label[:3])
test_label = test_dataset.pop('mpg')
print(test_label[:3])

# model
def build_model():
    network = Sequential([
        Input(shape=(3, )),
        Dense(units=32, activation='relu'),
        Dense(units=16, activation='relu'),
        Dense(units=1, activation='linear'),
    ])
    opti = tf.keras.optimizers.Adam(learning_rate=0.01)
    network.compile(optimizer=opti, loss='mean_squared_error', metrics=['mean_squared_error', 'mean_absolute_error'])
    
    return network

model = build_model()
print(model.summary())

EPOCHS = 5000

# 조기종료
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True   # 학습 중 가장 성능이 좋은 epoch의 가중치를 
    # baseline=0.01
)

history = model.fit(x=st_train_data, y=train_label, batch_size=32, epochs=EPOCHS, verbose=2, validation_split=0.2, callbacks = [early_stop])

df = pd.DataFrame(history.history)
print(df.head(3))
print(df.columns)

# 모델 학습 정보 시각화
def plt_history(df):
    hist = df
    hist['epoch'] = history.epoch
    # print(hist.head())
    plt.figure(figsize=(8, 14))
    plt.subplot(2, 1, 1)
    plt.xlabel('epoch')
    plt.ylabel('mae [mpg]')
    plt.plot(hist['epoch'], hist['mean_absolute_error'], label='train err')
    plt.plot(hist['epoch'], hist['val_mean_squared_error'], label='validation err')
    plt.legend()
    plt.show()


plt_history(df)

# 모델 평가
from sklearn.metrics import r2_score
loss, mse, mae = model.evaluate(st_test_data, test_label)
print(f'loss {loss:.3f}')
print(f'mse {mse:.3f}')
print(f'mae {mae:.3f}')
print('결정 계수 : ', r2_score(test_label, model.predict(st_test_data)))

# 새로운 값으로 예측
new_data = pd.DataFrame({
    'displacement':[300, 400],
    'horsepower':[120, 150],
    'weight':[2000, 4000]
})
new_st_data = stdscale_func(new_data)
new_data_pred = model.predict(new_st_data).ravel()
print('새 값 예측결과 : ', new_data_pred)

