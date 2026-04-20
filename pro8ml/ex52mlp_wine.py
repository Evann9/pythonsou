# MLP - wine dataset으로 다항 분리 (3등급)

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score,confusion_matrix,classification_report

data = load_wine()
x = data.data
y = data.target
print(x[:2], ' ', x.shape)       # (178, 13)
print(y[:2], ' ', np.unique(y))  # [0 1 2]

x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=42, stratify=y
)

# 스케일링 (MLP는 얘를 권장)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# 모델 생성
model = MLPClassifier( 
    hidden_layer_sizes=(20, 10),   # 은닉층 2개
    activation='relu',      # 활성화 함수
    solver='adam',          # 손실 최소화 함수 지정
    learning_rate_init=0.001,  # 학습율
    max_iter=150,     # 학습 횟수
    random_state=42,
    verbose=1        # 학습 도중 로그 출력 여부
)
model.fit(x_train_scaled, y_train)
pred = model.predict(x_test_scaled)
print('accuracy_score : ', accuracy_score(y_test, pred))  #  1.0
print('classification_report\n', classification_report(y_test, pred))

# 혼동행렬 시각화
cm = confusion_matrix(y_test, pred)
plt.figure(figsize=(5, 4))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues')
plt.title('confusion_matrix')
plt.xlabel('predicted')
plt.ylabel('actual')
plt.show()

# train loss curve 시각화
plt.plot(model.loss_curve_)
plt.title('train loss curve')
plt.xlabel('iteration(epoch)')
plt.ylabel('loss')  # 예측값과 실제값의 차이
plt.show()

# 참고 : 미분이 MLP(Deep Learning의 옛이름)에서 어떻게 쓰이는가? 미분으로 오차를 줄여나감
# MLP 구조 : 입력 -> 신경망(뉴런) -> 출력 후 오차를 확인
# 예) 입력(x) -> 모델 -> 예측값(y^) - 실제값(y) -> 오차(loss) 발생
#     오차함수(loss function)는 L = (y - y^)   예측이 틀릴수록 값이 커짐
# 그럼 미분은 왜 쓰나? 오차를 어떻게 줄일지 즉, 오차가 줄어드는 방향으로 w(가중치)를 갱신
# 전체 학습 과정을 보면
# 1.모델이 예측 -> 2.오차 계산 -> 3.미분(기울기 계산) 
#              -> 4. 가중치W를 갱신 -> 5. 반복(1 ~ 4) - 역전파(back propergation)
# 이것이 MLP 학습!!!
