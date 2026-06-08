# 다층 신경망 구성 : keras(Deep Learning lib) 모듈 사용
# : 일관성 있게 API를 제공 받을 수 있다.
# : 머신러닝 모델을 쉽게 작성이 가능

# 실습 : 논리회로 처리를 위한 분류 간단한 모델 작성

import numpy as np
from tensorflow import keras
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Activation
from tensorflow.keras.optimizers import SGD, RMSprop, Adam

# 1) 데이터 수집 및 가공
x = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[1]]) # OR 게이트
# y = np.array([0,1,1,1])     # 얘도 가능(sklearn에 비해 유연한 구조)

# 2) 모델 설정
model = Sequential([
    Input(shape=(2, )),
    Dense(units=1),
    Activation('sigmoid')
])

# 풀어 적으면 아래와 같이 할 수 도 있다.
# model = Sequential()
# model.add(Input(shape=(2, )))
# model.add(Dense(units=1))
# model.add(Activation('sigmoid'))

# 3) 모델 학습 과정 설정
# model.compile(loss='binary_crossentropy', optimizer='sgd', metrics=['accuracy'])
    # loss(손실함수): 훈련데이터에서 신경망의 성능을 측정하는 방법으로 모델이 정확히 학습할 수 있도록 함
    # optimizer: 입력데이터와 손실함수를 기반으로 모델을 갱신함
    # metrics: 훈련단계와 검정단계를 모니터링 하기 위해 사용 (모델 성능 지표)
# model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.compile(loss='binary_crossentropy', optimizer=SGD(learning_rate=0.1), metrics=['accuracy'])
# model.compile(loss='binary_crossentropy', optimizer=RMSprop(learning_rate=0.1), metrics=['accuracy'])
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.1), metrics=['accuracy'])

# 4) 모델 학습(더 나은 결과를 찾는 자동화된 과정) : train data 사용
model.fit(x=x, y=y, epochs=30, batch_size=1, verbose=2)

# 5) 모델 평가 : test data 사용
loss_metrics = model.evaluate(x=x, y=y)
print('loss_metrics : ', loss_metrics)  # [0.6271371841430664, 0.5]

# 6) 학습결과 확인 (예측)
pred = model.predict(x=x)
print('예측 확률 : ', pred)
# [[0.563117  ]
#  [0.3462985 ]
#  [0.8217862 ]
#  [0.65460086]]

proba = model.predict(x=x, verbose=0)
pred = (proba > 0.5).astype('int32')
print('예측 값 : ', pred.ravel())
print('실제 값 : ', y.ravel())

# 7) 학습된 모델 저장
model.save('tf4model.keras')

# 8) 모델 읽기
from tensorflow.keras.models import load_model
mymodel = load_model('tf4model.keras')
new_proba = mymodel.predict(x=x, verbose=0)
new_pred = (new_proba > 0.5).astype('int32')
print('예측 값 : ', new_pred.ravel())


# epochs=2 이상이면 역전파 알고리즘이 적용된다.
# 순전파 → 손실계산 → 역전파 → 가중치 업데이트
# 역전파 Backpropagation
# 모델의 예측값이 정답과 얼마나 다른지 계산한 뒤, 그 오차를 거꾸로 거슬러 올라가며
# 각 가중치가 오차에 얼마나 영향을 줬는지 계산하는 과정이다.
# 예측이 틀림 → 손실값 loss 계산
#            → 어느 가중치가 얼마나 책임이 있는지 계산 → 그 가중치를 조금씩 수정
# 순전파 : 입력 x → 은닉층 → 출력 y_pred → 손실 loss
# 역전파 반대 방향으로 진행 : 손실 loss → 출력층 → 은닉층 → 입력층 방향
# 한마디로 역전파는 손실값을 기준으로 각 가중치의 책임 정도를 계산하고, 그 결과를 이용해
# 모델의 가중치를 수정하는 딥러닝 학습의 핵심 알고리즘이다.





