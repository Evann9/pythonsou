"""
ROC(Receiver Operating Characteristic) Curve는 모든 분류 임계값에서 분류 모델의 성능을 보여주는 
그래프로 x축이 FPR(1-특이도), y축이 TPR(민감도)인 그래프이다. 
즉 민감도와 특이도의 관계를 표현한 그래프이다. 
ROC Curve는 AUC(Area Under Curve : 그래프 아래의 면적)를 이용해 모델의 성능을 평가한다. 
AUC가 클수록 정확히 분류함을 뜻한다.
fpr(1 - 특이도 : 위양성률)이 변할 때 tpr(민감도)이 어떻게 변하는지 알려주는 곡선
"""

from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, random_state=123)
# n_redundant : 독립변수 중 다른 독립변수의 선형조합으로 나타내는 성분 수
print(x[:3], x.shape) # (100, 2)
print(y[:3], y.shape) # (100,)

# 산포도
# plt.scatter(x[:,0], x[:,1])
# plt.show()

model = LogisticRegression().fit(x,y) # 모델 학습
y_hat = model.predict(x) # 예측값 생성
print('y_hat : ', y_hat[:5])
print('real : ', y[:5])

# Roc curve의 판별경계선 설정용 결정함수(Decision Function) 사용
# 샘플이 특정 클래스에 속하는지 판단하는 신뢰 점수(거리)를 반환
f_value = model.decision_function(x)
print('f_value : ', f_value[:10])
print()
df = pd.DataFrame(np.vstack([f_value, y_hat, y]).T, columns=['f','y_hat','y'])
print(df.head())

# 모델 성능 파악
# 혼동 행렬(Confusion Matrix) 생성
from sklearn.metrics import confusion_matrix
con_mat = confusion_matrix(y, y_hat)
print(con_mat)
# [[44  4]
#  [ 8 44]]

# 정확도: 전체 중 맞춘 비율
acc = (con_mat[0, 0] + con_mat[1, 1]) / len(y) 

# 재현율(Recall/TPR): 실제 Positive 중 맞춘 비율 (민감도)
recall = con_mat[1, 1] / (con_mat[1, 0] + con_mat[1, 1]) 

# 정밀도(Precision): Positive로 예측한 것 중 실제 Positive 비율
precision = con_mat[1, 1] / (con_mat[0, 1] + con_mat[1, 1]) 

# 특이도(Specificity): 실제 Negative 중 맞춘 비율
specificity = con_mat[0, 0] / (con_mat[0, 0] + con_mat[0, 1])

# 위양성률(Fallout/FPR): 실제 Negative 중 틀린 비율 (1-특이도)
fallout = con_mat[0, 1] / (con_mat[0, 0] + con_mat[0, 1]) 

print(f'정확도(Accuracy): {acc}')
print(f'재현율(Recall): {recall}')
print(f'정밀도(Precision): {precision}')
print(f'특이도(Specificity): {specificity}')
print(f'위양성률(Fallout): {fallout}')

print()
from sklearn import metrics
scc_score = metrics.accuracy_score(y, y_hat)
print(f'정확도(Accuracy): {scc_score}') # 0.88

# 주요 분류 지표(Precision, Recall, F1-score 등)를 한눈에 확인
cl_rep = metrics.classification_report(y, y_hat)
print(cl_rep)
#               precision    recall  f1-score   support

#            0       0.85      0.92      0.88        48
#            1       0.92      0.85      0.88        52

#     accuracy                           0.88       100
#    macro avg       0.88      0.88      0.88       100
# weighted avg       0.88      0.88      0.88       100

print()
# Roc curve 시각화
import matplotlib.pyplot as plt

fpr, tpr, thresholds = metrics.roc_curve(y, model.decision_function(x))
print('fpr : ', fpr)
print('tpr : ', tpr)
print('thresholds : ', thresholds)

plt.plot(fpr, tpr, 'o-', label="Logistic Regression")
plt.plot([0, 1], [0, 1], 'k--', label="random classifier line(AUC=0.5)")
plt.plot([fallout], [recall], 'ro', ms=6)  # 위양성률, 재현율 출력
plt.xlabel('위양성률(FPR)')
plt.ylabel('재현율(TPR)')
plt.title('ROC Curve')
plt.legend()
plt.show()

print('AUC(Area Under Curve) : ', metrics.auc(fpr, tpr)) # 0.9547 -> 매우 성능이 우수한 모델