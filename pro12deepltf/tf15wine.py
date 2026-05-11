# 와인의 등급과 맛, 산도 등을 측정해 레드, 화이트 와인 분류기
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

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12, stratify=y, shuffle=True)
print(x_train[:2], x_train.shape)
print(y_train[:2], y_train.shape)

# 모델
model = Sequential()
model.add(Input(shape=(12, )))
model.add(Dense(units=24, activation='relu'))
model.add(Dense(units=12, activation='relu'))
model.add(Dense(units=8, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))
print(model.summary())

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# fit() 전에 훈련되지 않은 모델의 정확도
loss, acc = model.evaluate(x_train, y_train, verbose=0)
print(f'훈련되지 않은 모델의 정확도:{acc * 100}%')

# 조기 종료
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

# 모델 저장
MODEL_DIR = './winemodel/'
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 조건 설정
# modelpath = 'winemodel/{epochs:02d}-{val_loss:.3f}.keras'
modelpath = 'winemodel.keras'
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

mymodel = load_model(modelpath)
new_data = x_test[:5, :]
print(new_data)
new_pred = mymodel.predict(new_data)
print('예측 결과:', np.where(new_pred >= 0.5, 1, 0).ravel())
