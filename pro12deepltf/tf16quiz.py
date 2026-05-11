# 문제2) 21세 이상의 피마 인디언 여성의 당뇨병 발병 여부에 대한 dataset을 이용하여 당뇨 판정을 위한 분류 모델을 작성한다.
# 피마 인디언 당뇨병 데이터는 아래와 같이 구성되어 있다.
#   Pregnancies: 임신 횟수
#   Glucose: 포도당 부하 검사 수치
#   BloodPressure: 혈압(mm Hg)
#   SkinThickness: 팔 삼두근 뒤쪽의 피하지방 측정값(mm)
#   Insulin: 혈청 인슐린(mu U/ml)
#   BMI: 체질량지수(체중(kg)/키(m))^2
#   DiabetesPedigreeFunction: 당뇨 내력 가중치 값
#   Age: 나이
#   Outcome: 5년 이내 당뇨병 발생여부 - 클래스 결정 값(0 또는 1)
# 당뇨 판정 칼럼은 outcome 이다.   1 이면 당뇨 환자로 판정
# train / test 분류 실시
# 모델 작성은 Sequential API, Function API 두 가지를 사용한다.
# ModelCheckPoint, EarlyStopping 사용
# loss, accuracy에 대한 시각화를 실시한다.

# https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/pima-indians-diabetes.data.csv

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
import os

# 데이터 읽기, 컬럼명이 없어서 직접 지정
url = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/pima-indians-diabetes.data.csv"
names = ['Pregnancies', 'Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI', 'DiabetesPedigreeFunction', 'Age', 'Outcome']
df = pd.read_csv(url, names=names)

# 전처리 (독립변수, 종속변수 분리)
dataset = df.values
x = dataset[:, 0:8]
y = dataset[:, 8]

# 스케일링 실시 (값 범위 맞춰줌)
scaler = StandardScaler()
x_scaled = scaler.fit_transform(x)

# 7:3 분리, stratify=y로 클래스 비율 유지
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.3, random_state=12, stratify=y)

# 모델 저장 폴더 준비
MODEL_DIR = './pimamodel/'
if not os.path.exists(MODEL_DIR):
    os.mkdir(MODEL_DIR)

print('--- 1. Sequential API 모델 ---')
seq_model = Sequential()
seq_model.add(Input(shape=(8, )))
seq_model.add(Dense(units=24, activation='relu'))
seq_model.add(Dense(units=12, activation='relu'))
seq_model.add(Dense(units=1, activation='sigmoid'))

seq_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 체크포인트, 얼리스탑 적용
seq_chkpoint = ModelCheckpoint(filepath='pimamodel/seq_best.keras', monitor='val_loss', save_best_only=True)
seq_early = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)

# 모델 학습
seq_hist = seq_model.fit(x_train, y_train, epochs=200, validation_split=0.2, batch_size=32, 
                        callbacks=[seq_early, seq_chkpoint], verbose=0)
seq_eval = seq_model.evaluate(x_test, y_test, verbose=0)
print(f'Sequential 모델 평가 - 손실: {seq_eval[0]:.4f}, 정확도: {seq_eval[1]:.4f}')
# Sequential 모델 평가 - 손실: 0.4673, 정확도: 0.7706

print('\n--- 2. Functional API 모델 ---')
inputs = Input(shape=(8, ))
h1 = Dense(units=24, activation='relu')(inputs)
h2 = Dense(units=12, activation='relu')(h1)
outputs = Dense(units=1, activation='sigmoid')(h2)
func_model = Model(inputs=inputs, outputs=outputs)

func_model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# 체크포인트, 얼리스탑 적용
func_chkpoint = ModelCheckpoint(filepath='pimamodel/func_best.keras', monitor='val_loss', save_best_only=True)
func_early = EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True)

# 모델 학습
func_hist = func_model.fit(x_train, y_train, epochs=200, validation_split=0.2, batch_size=32, 
                        callbacks=[func_early, func_chkpoint], verbose=0)
func_eval = func_model.evaluate(x_test, y_test, verbose=0)
print(f'Functional 모델 평가 - 손실: {func_eval[0]:.4f}, 정확도: {func_eval[1]:.4f}')
# Functional 모델 평가 - 손실: 0.4839, 정확도: 0.7662

# 시각화 처리
# Seq Loss
plt.figure()
plt.plot(seq_hist.epoch, seq_hist.history['loss'], label='train loss')
plt.plot(seq_hist.epoch, seq_hist.history['val_loss'], label='val loss')
plt.title('Sequential API - Loss')
plt.legend()
plt.show()

# Seq Acc
plt.figure()
plt.plot(seq_hist.epoch, seq_hist.history['accuracy'], label='train acc')
plt.plot(seq_hist.epoch, seq_hist.history['val_accuracy'], label='val acc')
plt.title('Sequential API - Accuracy')
plt.legend()
plt.show()

# Func Loss
plt.figure()
plt.plot(func_hist.epoch, func_hist.history['loss'], label='train loss')
plt.plot(func_hist.epoch, func_hist.history['val_loss'], label='val loss')
plt.title('Functional API - Loss')
plt.legend()
plt.show()

# Func Acc
plt.figure()
plt.plot(func_hist.epoch, func_hist.history['accuracy'], label='train acc')
plt.plot(func_hist.epoch, func_hist.history['val_accuracy'], label='val acc')
plt.title('Functional API - Accuracy')
plt.legend()
plt.show()

# 예측
new_data = x_test[:5]

print('\n--- Sequential API 모델 예측 ---')
seq_pred = seq_model.predict(new_data, verbose=0)
print('예측 결과 : ', np.where(seq_pred >= 0.5, 1, 0).ravel())
# 예측 결과 :  [1 1 0 0 1]

print('\n--- Functional API 모델 예측 ---')
func_pred = func_model.predict(new_data, verbose=0)
print('예측 결과 : ', np.where(func_pred >= 0.5, 1, 0).ravel())
# 예측 결과 :  [1 1 0 0 1]

print('\n실제 정답 : ', y_test[:5].astype(int))
# 실제 정답 :  [1 0 0 0 1]