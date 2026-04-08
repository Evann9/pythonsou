"""
[로지스틱 분류분석 문제3]
'testdata/advertisement.csv' 
참여 칼럼 : 
- Daily Time Spent on Site : 사이트 이용 시간 (분)
- Age : 나이,
- Area Income : 지역 소득,
- Daily Internet Usage : 일별 인터넷 사용량(분),
- Clicked Ad : 광고 클릭 여부 ( 0 : 클릭x , 1 : 클릭o )
광고를 클릭('Clicked on Ad')할 가능성이 높은 사용자 분류.
데이터 간 단위가 큰 경우 표준화 작업을 시도한다.
모델 성능 출력 : 정확도, 정밀도, 재현율, ROC 커브와 AUC 출력
새로운 데이터로 분류 작업을 진행해 본다.
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn import metrics

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/advertisement.csv")

x = data[['Daily Time Spent on Site', 'Age', 'Area Income', 'Daily Internet Usage']]
y = data['Clicked on Ad']

# 데이터 표준화
sc = StandardScaler()
x_scaled = sc.fit_transform(x)

model = LogisticRegression().fit(x_scaled, y) 
y_hat = model.predict(x_scaled) 
f_value = model.decision_function(x_scaled)

# 성능 지표 출력
print(metrics.classification_report(y, y_hat))
print('AUC:', metrics.roc_auc_score(y, f_value))

# ROC Curve 시각화
fpr, tpr, thresholds = metrics.roc_curve(y, f_value)
plt.plot(fpr, tpr, label="Logistic Regression")
plt.plot([0, 1], [0, 1], 'k--')
plt.xlabel('FPR')
plt.ylabel('TPR')
plt.title('ROC Curve')
plt.show()

# 새로운 데이터 예측
print('\n--- 새로운 데이터 예측 ---')
new_data = np.array([[40, 50, 20000, 100]])
new_data_scaled = sc.transform(new_data)
new_pred = model.predict(new_data_scaled)
new_prob = model.predict_proba(new_data_scaled)
print(f'결과: {"클릭함" if new_pred[0] == 1 else "클릭안함"}, 확률: {new_prob[0]}')