# 다항분류는 출력층에 softmax를 사용
#
# 이 파일의 흐름
# 1) softmax가 실수 점수를 클래스별 확률로 바꾸는 원리를 확인한다.
# 2) 5개 클래스 분류 모델을 만들고 one-hot label과 categorical_crossentropy를 사용한다.
# 3) 예측 확률에서 가장 큰 위치(argmax)를 실제 클래스 번호로 해석한다.

# 참고 : softmax 함수 보기
# 소프트맥스함수는 입력받은 실수 벡터를 0~1 사이의 확률값으로 정규화하여, 
# 모든 출력의 합이 1이 되도록 만드는 함수 (지수함수 / 지수함수 합)
import numpy as np
def softmaxFunc(a):
    # c를 빼면 exp 계산 시 너무 큰 값이 생기는 것을 줄일 수 있다.
    c = np.max(a)
    exp_a = np.exp(a - c)
    sum_exp_a = np.sum(exp_a)
    return exp_a / sum_exp_a

data = np.array([0.3, 2.8, 4.0])
print(softmaxFunc(data))

# 다항분류 모델 - 출력은 softmax로 인해
# 이 때 가장 큰 인덱스를 분류 결과로 취함
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.utils import to_categorical   # 원핫 지원
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(1)

xdata = np.random.random((1000, 12))            # feature   시험점수
ydata = np.random.randint(5, size=(1000, 1))    # label     다섯 과목
print(xdata[:2])
print(ydata[:2])
# softmax 출력이 5개 확률이므로 정답도 [0,0,1,0,0] 같은 one-hot 형태로 맞춘다.
ydata = to_categorical(ydata, num_classes = 5)
print(ydata[:2])

model = Sequential()
model.add(Input(shape=(12, )))
model.add(Dense(units=32, activation='relu'))
model.add(Dense(units=16, activation='relu'))
model.add(Dense(units=5, activation='softmax')) # 5개 클래스 각각의 확률을 출력
print(model.summary())

model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

history = model.fit(xdata, ydata, epochs=1000, batch_size=32, verbose=2, shuffle=True)
model_eval = model.evaluate(xdata, ydata, verbose=0)
print('모델 평가 결과 : ', model_eval)

# 시각화
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
ax1.plot(history.history['loss'])
ax1.set_title('Loss')
ax1.set_xlabel('epoch')
ax1.set_ylabel('loss')

ax2.plot(history.history['accuracy'])
ax2.set_title('Accuracy')
ax2.set_xlabel('epoch')
ax2.set_ylabel('accuracy')
plt.show()


# 기존 값으로 분류 예측
print('예측값 : ', model.predict(xdata[:5]))
# argmax는 가장 큰 확률을 가진 클래스 번호를 반환한다.
print('예측값 : ', np.argmax((model.predict(xdata[:5])), axis=1))
print('실제값 : ', ydata[:5])
print('실제값 : ', [int(i) for i in np.argmax(ydata[:5], axis=1)])

print()
# 새로운 값으로 예측
x_new = np.random.random([1, 12])
print(x_new)
new_pred = model.predict(x_new)
print('분류 결과 : ', new_pred)
print('분류 결과합 : ', np.sum(new_pred))
print('분류 결과 : ', np.argmax(new_pred))
classes = np.array(['국어', '영어', '수학', '과학', '체육'])
# 예측 결과를 과목명으로 출력하기
# 숫자 class id를 사람이 읽을 수 있는 이름으로 매핑한다.
print('예측값 : ', classes[np.argmax(new_pred, axis=1)[0]])


