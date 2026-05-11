# 다중선형회귀 : 자동차 연비 예측
# 조기종료 코드 추가
#
# 이 파일의 흐름
# 1) 자동차 스펙 데이터에서 연비(mpg)를 예측할 feature를 고른다.
# 2) train/test로 나누고, 학습 데이터 기준으로 표준화한다.
# 3) Keras 회귀 모델을 학습한 뒤 MAE/MSE/R2로 성능을 확인한다.
# 4) 새 자동차 스펙을 넣어 예상 mpg를 예측한다.

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler

# 데이터 읽기: 각 행은 자동차 1대, mpg는 예측해야 할 정답(label)이다.
datas = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/auto-mpg.csv")
print(datas.head(2))
print(datas.info())

# 문자열 컬럼은 신경망 입력으로 바로 쓰기 어렵고, 이 예제에서는 연비 예측에 사용하지 않는다.
del datas['car name']

# 결측치가 있으면 계산 중 오류가 나거나 학습이 불안정해질 수 있어 제거한다.
datas = datas.dropna()
print(datas.isna().sum)

# 너무 많은 feature를 한 번에 쓰기보다, 연비와 관련이 큰 수치형 feature 3개만 남긴다.
datas.drop(['cylinders', 'acceleration', 'model year', 'origin'], axis='columns', inplace=True)
print(datas.head(2))

# sns.pairplot(datas[['mpg', 'displacement', 'horsepower', 'weight']])
# plt.show()

# train / test split
# train은 모델이 학습할 데이터, test는 학습에 쓰지 않고 최종 성능 확인에만 쓰는 데이터이다.
train_dataset = datas.sample(frac=0.7, random_state=123)
print(train_dataset[:2], train_dataset.shape)   # (274, 4)
test_dataset = datas.drop(train_dataset.index)
print(train_dataset[:2], train_dataset.shape)   # (118, 4)

# 표준화 : (요소값 - 평균) / 표준편차
# displacement, horsepower, weight는 단위와 범위가 다르므로 그대로 넣으면 큰 값의 영향이 커질 수 있다.
# 반드시 train 데이터의 통계값으로만 표준화 기준을 만들고, test/new 데이터에도 같은 기준을 적용한다.
train_stat = train_dataset.describe()
train_stat.pop('mpg')
print(train_stat)
train_stat = train_stat.transpose() # 전치
print(train_stat)

def stdscale_func(x):
    # x의 각 컬럼을 train 데이터의 평균/표준편차 기준으로 같은 스케일에 맞춘다.
    return (x - train_stat['mean']) / train_stat['std']

# print(stdscale_func(train_dataset[:3]))
st_train_data = stdscale_func(train_dataset)
st_train_data = st_train_data.drop(['mpg'], axis='columns')
print(st_train_data[:3])

st_test_data = stdscale_func(test_dataset)
st_test_data = st_test_data.drop(['mpg'], axis='columns')
print(st_test_data[:3])

# label 분리: 모델 입력에는 feature만 들어가고, 정답 mpg는 y로 따로 전달한다.
train_label = train_dataset.pop('mpg')
print(train_label[:3])
test_label = test_dataset.pop('mpg')
print(test_label[:3])

# model
def build_model():
    # 회귀 모델이므로 마지막 출력은 숫자 1개이며 activation은 linear를 사용한다.
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
# val_loss가 더 좋아지지 않으면 학습을 멈춰 과적합을 줄인다.
early_stop = tf.keras.callbacks.EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True   # 학습 중 가장 성능이 좋은 epoch의 가중치를 
    # baseline=0.01
)

# validation_split=0.2는 train 데이터 중 20%를 검증용으로 떼어 학습 중 성능을 감시한다.
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
# MAE는 평균적으로 몇 mpg 정도 틀리는지 해석하기 쉽고, R2는 설명력을 보여준다.
from sklearn.metrics import r2_score
loss, mse, mae = model.evaluate(st_test_data, test_label)
print(f'loss {loss:.3f}')
print(f'mse {mse:.3f}')
print(f'mae {mae:.3f}')
print('결정 계수 : ', r2_score(test_label, model.predict(st_test_data)))

# 새로운 값으로 예측
# 새 데이터도 학습 때 사용한 컬럼명과 순서, 표준화 기준을 그대로 맞춰야 한다.
new_data = pd.DataFrame({
    'displacement':[300, 400],
    'horsepower':[120, 150],
    'weight':[2000, 4000]
})
new_st_data = stdscale_func(new_data)
new_data_pred = model.predict(new_st_data).ravel()
print('새 값 예측결과 : ', new_data_pred)

