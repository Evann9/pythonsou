# BMI는 체질량지수로, 몸무게(kg)를 키의 제곱으로 나눈 값. 
# 키와 몸무게로 체지방량을 추정하여 비만도를 간편하게 측정하는 지표
# 공식 : 체중(kg) / 키(m)^2
# ex) 키: 170, 몸무게: 68 => 68 / (1.7)^2 
"""
파일 생성
print(68 / ((1.7) * (1.7))) # 23.529 -> 과체중

import random
random.seed(12)

def cald_bmiFunc(height, weight):
    bmi = weight / (height / 100) ** 2
    if bmi < 18.5:
        return "thin"
    elif bmi < 25.0:
        return "normal"
    else:
        return "fat"
    
print(cald_bmiFunc(170, 68))

fp = open("bmi.csv", "w")
fp.write("height,weight,label\n")

cnt = {"thin":0, "normal":0, "fat":0}

for i in range(50000):
    h = random.randint(150, 200)
    w = random.randint(35, 100)
    label = cald_bmiFunc(h, w)
    cnt[label] += 1
    fp.write(f"{h},{w},{label}\n")
fp.close()
"""

# bmi data를 SVM으로 분류
from sklearn import svm, metrics
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv("bmi.csv")
print(df.head(3))
print(df.shape) # (50000, 3)
print(df.info())

label = df['label']
print(label[:2])

w = df['weight']
h = df['height']
print(w[:2], h[:2])
wh = pd.concat([w, h], axis=1)
print(wh[:2])

print()
# label은 dummy화
label = label.map({'thin':0, 'normal':1, 'fat':2})

x_train, x_test, y_train, y_test = train_test_split(wh, label, test_size=0.3, random_state=42)
print(x_train.shape, x_test.shape) # (35000, 2) (15000, 2)

model = svm.SVC(C=0.01, kernel='rbf')
model.fit(x_train, y_train)

pred = model.predict(x_test)
print('예측값 : ', pred[:10])
print('실제값 : ', y_test[:10].values)
# 예측값 :  [0 1 2 2 1 0 1 0 0 2]
# 실제값 :  [0 1 2 2 1 0 1 0 0 2]
acc = metrics.accuracy_score(y_test, pred)
print('정확도 : ', acc)   # 0.9735

# 교차 검증 모델
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, wh, label, cv=3)
print('3회 각 정확도 : ',scores)  # [0.97078058 0.96838063 0.96885875]
print('평균 정확도 : ', scores.mean()) # 0.9693399903752794

# 새로운 값으로 예측
new_data = pd.DataFrame({'weight':[66,88], 'height':[188,160]})
new_data['weight'] = new_data['weight'] / 100
new_data['height'] = new_data['height'] / 200
new_pred = model.predict(new_data)
print('새로운 값 예측 결과 : ', new_pred)

# 시각화 
df2 = pd.read_csv("bmi.csv", index_col=2)

def scatter_func(lbl, color):
    b = df2.loc[lbl]
    plt.scatter(b['weight'], b['height'], c=color, label=lbl)
    plt.legend()

scatter_func('fat', 'red')
scatter_func('normal', 'yellow')
scatter_func('thin', 'blue')
plt.legend()
plt.show()