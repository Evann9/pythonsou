# 최근접 이웃(K-Nearest Neighbors) - breast_cancer dataset 사용

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

data = load_breast_cancer()
x = data.data 
y = data.target  # (0 : malignant(악성), 1 : benign)
print(x[:1], ' ', x.shape)
print(y[:1], ' ', np.unique(y))

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42, stratify=y)
print(x_train.shape, x_test.shape) # (455, 30) (114, 30)

# 표준화(∵거리기반 모델이므로 크기가 영향을 미침) 
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)

# 분류 모델 생성
# KNN은 
train_acc = []
test_acc = []
k_range = range(3, 12)
for k in k_range:
    model = KNeighborsClassifier(n_neighbors=k)
    model.fit(x_train_scaled, y_train)
    y_train_pred = model.predict(x_train_scaled)
    y_test_pred = model.predict(x_test_scaled)
    train_acc.append(accuracy_score(y_train, y_train_pred))
    test_acc.append(accuracy_score(y_test, y_test_pred))

# 시각화
import matplotlib.pyplot as plt
plt.figure()
plt.plot(k_range, train_acc,marker='o', label='train acc')
plt.plot(k_range, test_acc,marker='s', label='test acc')
plt.xlabel('k value')
plt.ylabel('accuracy')
plt.title('knn accuracy comp')
plt.grid(True)
plt.legend()
plt.show()
# 그래프 기준으로 최적은 3

best_k = k_range[np.argmax(test_acc)]
print('최적의 k : ', best_k)
# 최적의 k :  3
# test acc가 가장 높은 지점이 3 (과적합 의심)
# 4는 불안, 7 ~ 9는 안정적

best_k = 9
final_model = KNeighborsClassifier(n_neighbors=best_k)
final_model.fit(x_train_scaled, y_train)
y_pred = final_model.predict(x_test_scaled)
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10])
print(f"총 갯수: {len(y_test)}, 오류수: {(y_test != y_pred).sum()}")
# 총 갯수: 114, 오류수: 4
print(f"분류 정확도: {accuracy_score(y_test, y_pred)}") #  0.9736842105263158
print(f"분류 리포트: \n{classification_report(y_test, y_pred)}")
print(f"분류 혼동행렬: \n{confusion_matrix(y_test, y_pred)}")
# [[39  3]
#  [ 0 72]]

# 새로운 자료로 예측  (기존 자료 수정 사용)
new_data = x[0].copy()
new_data = new_data + np.random.normal(0,0.1, size=new_data.shape)
new_data_scaled = scaler.transform([new_data])
new_pred = final_model.predict(new_data_scaled)
new_pred_prob = final_model.predict_proba(new_data_scaled)
print('새로운 데이터 예측 결과 : ', new_pred)
print('새로운 데이터 예측 확률 : ', new_pred_prob)