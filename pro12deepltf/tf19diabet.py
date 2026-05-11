# 이항분류(sigmoid)는 다항분류(softmax)로 처리 가능
#
# 이 파일의 목적
# - 같은 당뇨병 0/1 분류 문제를 두 방식으로 풀어본다.
# - 방식 1: 출력 1개 + sigmoid + binary_crossentropy
# - 방식 2: 출력 2개 + softmax + categorical_crossentropy

import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from sklearn.model_selection import train_test_split

datas = np.loadtxt('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/diabetes.csv', delimiter=',')
print(datas.shape)
print(datas[:1])
print(set(datas[:, -1]))

# 앞 8개 컬럼은 feature, 마지막 컬럼은 당뇨 여부 label이다.
x_train, x_test, y_train, y_test = train_test_split(datas[:, 0:8], datas[:, -1], test_size=0.3, shuffle=True, random_state=123)
print(x_train.shape, x_test.shape)  # (531, 8) (228, 8)

print('\n이항분류(sigmoid)')
# sigmoid 방식에서는 정답 y가 0 또는 1인 1차원 값 그대로 들어간다.
model = Sequential()
model.add(Input(shape=(8, )))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['acc'])
model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=0)
scores = model.evaluate(x_test, y_test, verbose=0)
print('sigmoid scores : ', scores)

print('\n다항분류(softmax)')
from tensorflow.keras.utils import to_categorical

# softmax 방식에서는 정답 y를 [1,0] 또는 [0,1] 형태의 one-hot 벡터로 바꾼다.
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)
print(y_train[:3])

model = Sequential()
model.add(Input(shape=(8, )))
model.add(Dense(units=64, activation='relu'))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=2, activation='softmax'))

# 출력 노드가 2개라서 각 클래스(0/1)의 확률이 따로 나온다.
model.compile(optimizer='adam', loss='categorical_crossentropy')
model.fit(x_train, y_train, epochs=100, batch_size=32, verbose=0)
scores = model.evaluate(x_test, y_test, verbose=0)
print('softmax scores : ', scores)

