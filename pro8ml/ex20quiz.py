# [로지스틱 분류분석 문제2] 

# 게임, TV 시청 데이터로 안경 착용 유무를 분류하시오.
# 안경 : 값0(착용X), 값1(착용O)
# 예제 파일 : https://github.com/pykwon  ==>  bodycheck.csv
# 새로운 데이터(키보드로 입력)로 분류 확인. 스케일링X

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler  # 표준화
from sklearn.linear_model import LogisticRegression
from sklearn import datasets

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/bodycheck.csv")
print(data.head(3), data.shape) 
# 컬럼 확인: ['신장', '체중', '안경유무', '성별', '머리둘레', '좌우시력']
# 문제에서 요구하는 독립변수: 게임, TV 시청 데이터가 없으므로 
# 데이터셋 내의 '게임', 'TV시청' 컬럼이 있는지 확인이 필요하나, 
# 제공된 bodycheck.csv의 일반적인 구성에 따라 '게임', 'TV시청' 컬럼을 사용함.

x = data[['게임', 'TV시청']]
y = data['안경유무']

print('\n데이터 분리 ----')
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.3, random_state=12)

print('\n분류 모델 생성 ----')
model = LogisticRegression(C=0.06, solver='lbfgs', random_state=0)
model.fit(x_train, y_train)

y_pred = model.predict(x_test)
print(f"분류 정확도: {accuracy_score(y_test, y_pred)}")

print('\n새로운 데이터로 분류 확인 (키보드 입력) ----')
try:
    input_game = float(input("게임 시간을 입력하세요: "))
    input_tv = float(input("TV 시청 시간을 입력하세요: "))
    
    new_data = pd.DataFrame({'게임': [input_game], 'TV시청': [input_tv]})
    new_pred = model.predict(new_data)
    new_prob = model.predict_proba(new_data)
    
    if new_pred[0] == 1:
        print(f"예측 결과: 안경 착용 (확률: {new_prob[0][1]:.2f})")
    else:
        print(f"예측 결과: 안경 미착용 (확률: {new_prob[0][0]:.2f})")
except Exception as e:
    print("입력 에러:", e)

import joblib
joblib.dump(model, 'bodycheck_model.pkl')