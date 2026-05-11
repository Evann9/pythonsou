# animal_name: Unique for each instance
# hair Boolean
# feathers Boolean
# eggs Boolean
# milk Boolean
# airborne Boolean
# aquatic Boolean
# predator Boolean
# toothed Boolean
# backbone Boolean
# breathes Boolean
# venomous Boolean
# fins Boolean
# legs Numeric (set of values: {0,2,4,5,6,8})
# tail Boolean
# domestic Boolean
# catsize Boolean
# class_type Numeric (integer values in range [1,7])
# 1:포유류, 2번:조류 ~~

import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout
from sklearn.model_selection import train_test_split

datas = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/zoo.csv')
print(datas.head(3))
print(datas.info())

x_data = datas.iloc[:, :-1].astype("float32").values
y_data = datas.iloc[:, -1].astype("int32").values
print(x_data[0], x_data.shape)
print(y_data[0], sorted(set(map(int, y_data))))

np.random.seed(42)
# tf.keras.utils.set_random


x_train, x_test, y_train, y_test = train_test_split(
    x_data, y_data, test_size=0.2, random_state=42, stratify=y_data
)

print(x_train.shape, x_test.shape)

nb_classes = len(set(y_data))

model = Sequential([
    Input(shape=(x_train.shape[1], )),
    Dense(units=64, activation='relu'),
    Dropout(rate=0.3),
    Dense(units=32, activation='relu'),
    Dropout(rate=0.3),
    Dense(units=7, activation='softmax'),
])
print(model.summary())

# 레이블을 원핫 처리 안 한 경우
model.compile(optimizer='adam', 
            loss='sparse_categorical_crossentropy',     # 레이블 원핫 내부적으로 처리
            # loss='categorical_crossentropy',          # 레이블 원핫되어 있어야 함
            metrics=['accuracy'])

history = model.fit(x_train, y_train, epochs=50, batch_size=32, validation_split=0.2, verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print(f'loss:{loss:.4f}, acc:{acc:.4f}')

# 시각화
import matplotlib.pyplot as plt
plt.plot(history.history['loss'], label='train loss')
plt.plot(history.history['val_loss'], label='val loss')
plt.legend()
plt.show()

plt.plot(history.history['accuracy'], label='train accuracy')
plt.plot(history.history['val_accuracy'], label='val accuracy')
plt.legend()
plt.show()

# 혼동행렬 출력
from sklearn.metrics import classification_report, confusion_matrix
import seaborn as sns
y_pred = np.argmax(model.predict(x_test), axis=1)
print('classification_report : \n', classification_report(y_test, y_pred))

cm = confusion_matrix(y_test, y_pred)
print(cm)
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.xlabel('predicted')
plt.ylabel('true')
plt.show()

print('\n새로운 값으로 분류 예측')
new_data = np.array([[1,0,0,1,1,0,0,1,1,1,1,0,0,4,1,0]], dtype='float32')
probs = model.predict(new_data)
print('예측 확률 : ', probs)
print('예측 클래스 : ', np.argmax(probs) + 1)  # +1로 원래 1~7 복원