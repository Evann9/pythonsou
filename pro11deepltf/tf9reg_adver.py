# 다중선형회귀 : tv,radio,newspaper가 sales에 얼마나 영향을 주는지 파악

import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras import optimizers
import numpy as np
import pandas as pd

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/Advertising.csv")
print(data.head(2))
del data['no']
print(data.head(2))

fdata = data[['tv', 'radio', 'newspaper']]
# ldata = data[['sales']]
ldata = data.iloc[:, [3]]
print(fdata.head(2))
print(ldata[:2])

# feature 간 단위의 차이가 클 경우 정규화/표준화 작업이 모델 성능에 도움
from sklearn.preprocessing import MinMaxScaler, minmax_scale, StandardScaler

# 정규화
# scaler = MinMaxScaler(feature_range=(0, 1))
# fedata = scaler.fit_transform(data)
# print(fedata[:3])
fedata = minmax_scale(fdata, axis=0, copy=True)     # 행 기준, 원본자료 보존
print(fedata[:3])

# train / test 분리
from sklearn.model_selection import train_test_split
x_train, x_test, y_train, y_test = train_test_split(fedata, ldata, shuffle=True, test_size=0.3, random_state=123)   # stratify는 회귀에서는 안줌
print(x_train[:2], x_train.shape)   # (140, 3)
print(x_test[:2], x_test.shape)     # (60, 3)

print()
# 전처리가 모두 끝난 경우 모델 설계 및 실행
model = Sequential()
model.add(Input(shape=(3, )))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='linear'))      # activation 생략 가능
print(model.summary())
# Model: "sequential"
# ┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
# ┃ Layer (type)                         ┃ Output Shape                ┃         Param # ┃
# ┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
# │ dense (Dense)                        │ (None, 16)                  │              64 │
# ├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
# │ dense_1 (Dense)                      │ (None, 8)                   │             136 │
# ├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
# │ dense_2 (Dense)                      │ (None, 1)                   │               9 │
# └──────────────────────────────────────┴─────────────────────────────┴─────────────────┘
#  Total params: 209 (836.00 B)
#  Trainable params: 209 (836.00 B)
#  Non-trainable params: 0 (0.00 B)
# None


# pip install pydot
# 케라스 모델 구조를 이미지 파일로 저장
tf.keras.utils.plot_model(
    model, 
    to_file = 'aaa.png',
    show_shapes=True,               # 각 layer의 입력/출력 shape 표시
    show_layer_names=True,          # layer 이름 표시
    show_dtype=True,                # 데이터 타입 표시
    show_layer_activations=True,    # activation 함수 표시
    dpi=96                          # 이미지 해상도
    )

model.compile(optimizer='adam', loss='mse', metrics=['mse'])

history = model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2)   # train data중 20%를 학습 중 검증용 사용

ev_loss = model.evaluate(x_test, y_test, verbose=0)
print('ev_loss : ', ev_loss)

# history 값 확인
# print('history : ', history.history)
print('history val_loss : ', history.history['val_loss'])   # valid
print('history val_mse : ', history.history['val_mse'])
print('history loss : ', history.history['loss'])
print('history mse : ', history.history['mse'])

# loss 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['val_loss'], label='val_loss')
plt.plot(history.history['loss'], label='loss')
plt.legend()
plt.show()

from sklearn.metrics import r2_score
print('설명력:', r2_score(y_test, model.predict(x_test)))

# predict
pred = model.predict(x_test[:5])
print('예측값 : ', pred.ravel())
print('실제값 : ', y_test[:5].values.ravel())
# 예측값 :  [13.116314  8.639378 16.042656 11.372726 13.549072]
# 실제값 :  [11.4  8.8 14.7 10.1 14.6]

print('\n\nFunctional api를 사용한 방법 -------------')
from tensorflow.keras.models import Model
# 입력층 정의
inputs = Input(shape=(3, ), name='input_layer') # name은 텐서보드 등에 사용
# 은닉층 정의
x = Dense(units=16, activation='relu', name='hidden_layer1')(inputs)
x = Dense(units=16, activation='relu', name='hidden_layer2')(x)
# 출력층 정의
outputs = Dense(units=1, activation='linear', name='output_layer')(x)
# 모델 생성 (입력과 출력을 연결)
func_model = Model(inputs, outputs)

func_model.compile(optimizer='adam', loss='mse', metrics=['mse'])

history = func_model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=2, validation_split=0.2)   # train data중 20%를 학습 중 검증용 사용

ev_loss = func_model.evaluate(x_test, y_test, verbose=0)
print('func_model ev_loss : ', ev_loss)


# ============================================================
# TensorBoard 설정
# ============================================================
import datetime
from tensorflow.keras.callbacks import TensorBoard

# 실행할 때마다 타임스탬프 폴더 생성 → 여러 실행 비교 가능
log_dir = "logs/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")

tb_callback = TensorBoard(
    log_dir=log_dir,
    histogram_freq=1,   # 에포크마다 가중치 히스토그램 기록
    write_graph=True,   # 모델 그래프 기록
)

print(f'TensorBoard 로그 저장 경로: {log_dir}')

# ============================================================
# Functional API 모델 평가 및 예측
# ============================================================
from sklearn.metrics import r2_score
import matplotlib.pyplot as plt

# func_model에 TensorBoard 콜백 적용하여 재학습
history2 = func_model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=2,
    validation_split=0.2,
    callbacks=[tb_callback]   # TensorBoard 콜백 추가
)

ev_loss2 = func_model.evaluate(x_test, y_test, verbose=0)
print('func_model ev_loss:', ev_loss2)

# loss 시각화
plt.figure(figsize=(8, 4))
plt.plot(history2.history['loss'], label='train loss')
plt.plot(history2.history['val_loss'], label='val loss')
plt.title('Functional API - Training Loss')
plt.xlabel('Epoch')
plt.ylabel('Loss (MSE)')
plt.legend()
plt.tight_layout()
plt.show()

# 설명력
pred2 = func_model.predict(x_test)
print('func_model 설명력(R²):', r2_score(y_test, pred2))

# 예측값 vs 실제값
print('예측값:', pred2[:5].ravel())
print('실제값:', y_test[:5].values.ravel())

# ============================================================
# Sequential 모델도 TensorBoard 적용 비교용
# ============================================================
log_dir_seq = "logs/sequential_" + datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
tb_seq = TensorBoard(log_dir=log_dir_seq, histogram_freq=1)

history_seq = model.fit(
    x_train, y_train,
    epochs=100,
    batch_size=32,
    verbose=0,
    validation_split=0.2,
    callbacks=[tb_seq]
)

# ============================================================
# TensorBoard 실행 안내
# ============================================================
print('\n===== TensorBoard 실행 방법 =====')
print('터미널에서 아래 명령어 실행:')
print('  tensorboard --logdir=logs')
print('브라우저에서 접속: http://localhost:6006')
print('=================================')