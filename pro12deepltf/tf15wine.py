# 와인의 등급과 맛, 산도 등을 측정해 레드, 화이트 와인 분류기
#
# 이 파일의 흐름
# 1) 와인 성분 데이터 12개 feature로 와인 종류(0/1)를 분류한다.
# 2) validation loss 기준으로 조기 종료하고, 가장 좋은 모델을 파일로 저장한다.
# 3) 저장된 모델을 다시 불러와 예측까지 수행한다.
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

# 마지막 컬럼이 정답 label이고, 나머지 12개 컬럼이 입력 feature이다.
wdf = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/wine.csv")
print(wdf.head(2))
print(wdf.info())
print(wdf.iloc[:, 12].unique())     # [1 0]
print(len(wdf[wdf.iloc[:, 12]==0])) # 4898
print(len(wdf[wdf.iloc[:, 12]==1])) # 1599

# array로 변환
dataset = wdf.values
x = dataset[:, 0:12]
y = dataset[:, -1]
print(x[:2])
print(y[:2])

# stratify=y는 train/test에 0과 1의 비율이 비슷하게 들어가도록 유지한다.
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y, shuffle=True)
print(x_train[:2], x_train.shape)
print(y_train[:2], y_train.shape)

# 모델
# 이진분류이므로 마지막 노드는 1개, activation은 sigmoid를 사용한다.
model = Sequential()
model.add(Input(shape=(12, )))
model.add(Dense(units=24, activation='relu'))
model.add(Dense(units=12, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit() 전에 훈련되지 않은 모델의 정확도
# 학습 전 성능을 확인하면 학습 후 성능 향상을 비교하기 쉽다.
loss, acc = model.evaluate(x_train, y_train, verbose=0)
print(f'훈련되지 않은 모델의 정확도:{acc * 100}%')

# 조기 종료
# 검증 손실이 5번 연속 개선되지 않으면 멈추고, 가장 좋았던 가중치로 되돌린다.
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# 모델 저장
MODEL_DIR = './winemodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 조건 설정
# modelpath = 'winemodel/{epochs:02d}-{val_loss:.3f}.keras'
modelpath = 'winemodel.keras'
# save_best_only=True라서 validation loss가 가장 낮은 모델만 파일로 남는다.
chkpoint = ModelCheckpoint(filepath=modelpath, monitor='val_loss', mode='auto', save_best_only=True)

# 학습 모델
history = model.fit(x_train, y_train, epochs=1000, validation_split=0.2, batch_size=64, callbacks=[early_stop, chkpoint])

loss, acc = model.evaluate(x_test, y_test, verbose = 0)
print(f'훈련된 모델의 정확도:{acc * 100}%')

# 시각화
epoch_len = np.arange(len(history.epoch))
plt.plot(epoch_len, history.history['val_loss'], c='red', label='val_loss')
plt.plot(epoch_len, history.history['loss'], c='blue', label='loss')
plt.xlabel('epochs')
plt.ylabel('loss')
plt.legend()
plt.show()

plt.plot(epoch_len, history.history['val_accuracy'], c='red', label='val_accuracy')
plt.plot(epoch_len, history.history['accuracy'], c='blue', label='accuracy')
plt.xlabel('epochs')
plt.ylabel('accuracy')
plt.legend()
plt.show()


# 저장된 모델로 예측
from tensorflow.keras.models import load_model

# 학습한 모델 파일을 불러와도 같은 구조와 가중치로 바로 예측할 수 있다.
mymodel = load_model(modelpath)
new_data = x_test[:5, :]
print(new_data)
new_pred = mymodel.predict(new_data)
print('예측 결과:', np.where(new_pred >= 0.5, 1, 0).ravel())
