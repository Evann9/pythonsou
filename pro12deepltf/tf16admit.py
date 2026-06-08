import pandas as pd
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np
import os
from sklearn.preprocessing import StandardScaler

# 대학원 합격 여부 예측 예제
# - 입력: gre, gpa, rank
# - 출력: admit(0/1)
# - rank는 숫자로 적혀 있지만 등급을 뜻하는 범주형 변수라 원핫 인코딩한다.

df = pd.read_csv('binary.csv')
print(df.head(3))
print(df.info())

# 전처리 : rank는 연속형이 아니라 범주형 자료이므로 원핫 처리
df = pd.get_dummies(df, columns=['rank'], dtype=int)
print(df.head(3))

# feature, label로 구분
x = df.drop('admit', axis=1)
y = df['admit']
print(x.head(3))
print(y.head(3))

scaler = StandardScaler()
# gre와 gpa처럼 값의 단위가 다른 feature를 평균 0, 표준편차 1 근처로 맞춘다.
x_scaled = scaler.fit_transform(x)

# train / test split
x_train, x_test, y_train, y_test = train_test_split(x_scaled, y, test_size=0.2, random_state=42)

# model
# sigmoid 출력값은 합격할 확률로 해석한다.
model = Sequential([
    Input(shape=(x_train.shape[1],)),
    Dense(units=16, activation='relu'),
    Dense(units=8, activation='relu'),
    Dense(units=1, activation='sigmoid'),
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
print(model.summary())

history = model.fit(x_train, y_train, validation_data = (x_test, y_test), epochs=100, batch_size=32, verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'테스트 결과 손실:{loss:.4f}, 정확도:{acc:.4f}')

plt.figure(figsize=(12, 5))
# loss
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()

# accuracy
plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')

plt.legend()
plt.show()

# 사용자 입력 결과 예측
# 사용자가 입력한 값도 학습 데이터와 같은 컬럼 순서로 만들고, 같은 scaler로 변환해야 한다.
gre = float(input('gre 점수 입력:'))
gpa = float(input('gpa 점수 입력:'))
rank = int(input('rank 입력(1 ~ 4):'))
rank_encoded = [0,0,0,0]    # 입력된 rank 원핫처리
# rank=1이면 [1,0,0,0], rank=4이면 [0,0,0,1]이 된다.
rank_encoded[rank - 1] = 1

user_input = np.array([[gre, gpa] + rank_encoded])
print('user_input : ', user_input)

user_scaled = scaler.transform(user_input)
new_pred = model.predict(user_scaled)
# new_pred는 0~1 사이 확률이므로 0.5를 기준으로 합격/불합격을 나눈다.
prob = new_pred[0][0]
print('합격 확률 : ', prob)
if prob >= 0.5:
    print('합격 가능성이 높아요')
else:
    print('불합격 할 것 같아요')
