# 앙상블 학습 : 여러 개의 분류기를 생성하고, 그 예측을 결합함으로써 보다 정확한 예측결과를 얻을 수 있음.
# 강력한 모델 하나보다는 약한 모델 여러개를 조합하여 더 정확한 예측결과를 도출.

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline

from sklearn.ensemble import VotingClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from sklearn.metrics import accuracy_score
from collections import Counter
import numpy as np

cancer = load_breast_cancer()
print(cancer.keys())
x, y = cancer.data, cancer.target
print(x[:2])
print(y[:2])
print('diagnosis(y) : ', np.unique(y))  # [0(악성), 1(양성)]
# 0과 1의 비율
counter = Counter(y)
total = sum(counter.values())
for cls, cnt in counter.items():
    print(f"class {cls}:{cnt}개 ({cnt/total*100:.2f}%)")
# class 0:212개 (37.26%)
# class 1:357개 (62.74%)

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=12, stratify=y)
# stratify=y : train, test 비율 유지 (불균형 데이터 모델 평가시 왜곡 방지)
y_il = y.tolist()
ytr_li = y_train.tolist()
yte_li = y_test.tolist()

print('전체 분포 : ', Counter(y_il))  # Counter({1: 357, 0: 212})
print('train 분포 : ', Counter(ytr_li)) # Counter({1: 285, 0: 170})
print('test 분포 : ', Counter(yte_li)) #  Counter({1: 72, 0: 42})


print('\n분류 모델 생성 ----')
# make_pipeline : 전처리와 모델을 일체형 객체로 관리
logi = make_pipeline(StandardScaler(), LogisticRegression(max_iter=1000, solver='lbfgs',random_state=12))
knn = make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5))
tree = DecisionTreeClassifier(max_depth=3, random_state=12)

# 앙상블 모델
voting = VotingClassifier(estimators=[('LR', logi), ('KNN', knn), ('DT', tree)], voting='soft')

# 개별 모델 성능 확인
named_models = [('LR', logi), ('KNN', knn), ('DT', tree)]
for name, clf in named_models:
    clf.fit(x_train, y_train)
    pred = clf.predict(x_test)
    print(f"{name} 정확도 : {accuracy_score(y_test, pred):.4f}")

# 분류 모델 생성 ----
# LR 정확도 : 0.9912
# KNN 정확도 : 0.9737
# DT 정확도 : 0.8860

# Votiong 성능
voting.fit(x_train, y_train)
vpred = voting.predict(x_test)
print(f"Voting 정확도 : {accuracy_score(y_test, vpred):.4f}") # Voting 정확도 : 0.9561

# 선택 : 교차검증으로 안정성 확인
cvfold = StratifiedKFold(n_splits=5, shuffle=True, random_state=12)
cv_score = cross_val_score(voting, x, y, cv=cvfold, scoring='accuracy')
print(f'voting 5차례 cv 정확도 평균 : {cv_score.mean():.4f} (표준편차 : +- {np.std(cv_score):.4f})')
# voting 5차례 cv 정확도 평균 : 0.9719 (표준편차 : +- 0.0140)

print('\n모델 성능 확인')
# 모델 성능 지표
from sklearn.metrics import classification_report, confusion_matrix, roc_curve, roc_auc_score
print('\nvoting 모델 성능 평가')
print(classification_report(y_test, vpred))
#               precision    recall  f1-score   support

#            0       0.93      0.95      0.94        42
#            1       0.97      0.96      0.97        72

#     accuracy                           0.96       114
#    macro avg       0.95      0.96      0.95       114
# weighted avg       0.96      0.96      0.96       114
print(confusion_matrix(y_test, vpred))
# [[40  2]
#  [ 3 69]]
print(roc_auc_score(y_test, voting.predict_proba(x_test)[:,1]))
# 0.9930555555555555
