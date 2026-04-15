from sklearn.datasets import fetch_lfw_people
import koreanize_matplotlib
import matplotlib.pyplot as plt
from sklearn.svm import SVC
from sklearn.decomposition import PCA 
from sklearn.pipeline import make_pipeline
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report
"""# SVM 분류 모델로 이미지 분류
# 세계 정치인 중 일부 얼굴 사진 데이터를 사용

faces = fetch_lfw_people(min_faces_per_person=60, color=False, resize=0.5)
# min_faces_per_person = n : 한사람 당 n장 이상의 사진이 있는 자료만 사용
# print(faces)
# print(faces.DESCR)
print(faces.data)
print(faces.data.shape) # (1348, 2914)
print(faces.target) # [1 3 3 ... 7 3 5]
print(faces.target_names) # ['Ariel Sharon' 'Colin Powell' ... 'Tony Blair']
print(faces.images.shape) # (1348, 62, 47)
print()
print(faces.images[1])
print(faces.target_names[faces.target[1]])

# 이미지 시각화
plt.imshow(faces.images[1], cmap='bone')
plt.show()

# 이미지 15개 시각화
fig, ax = plt.subplots(3, 5)
for i, axi, in enumerate(ax.flat):
    axi.imshow(faces.images[i], cmap='bone')
    axi.set(xticks=[], yticks=[], xlabel=faces.target_names[faces.target[i]])
plt.show()

# 주성분 분석으로 이미지 차원을 축소시켜 분류작업을 진행
# 설명력 95% 되는 최소 개수를 얻기
pca = PCA(n_components=0.95)
x_pca = pca.fit_transform(faces.data)
print(pca.n_components_)  # 184

n = 150
m_pca = PCA(n_components=n, whiten=True, random_state=0) # whiten=True : 주성분의 스케일이 작아지도록 조절
x_low = m_pca.fit_transform(faces.data)
print(x_low.shape) # (1348, 2914) -> (1348, n)

# 시각화
fig, ax = plt.subplots(3, 5, figsize=(10, 6))
for i, axi, in enumerate(ax.flat):
    axi.imshow(m_pca.components_[i].reshape(faces.images[0].shape), cmap='bone')
    # reshape(faces.images[0].shape) : [2914] -> (62,47)
    axi.axis('off')
    axi.set_title(f'PC {i+1}')
plt.suptitle('Eigenfaces(주성분 얼굴)', fontsize=12)
plt.tight_layout()
plt.show()  # 출력 이미지는 실제 얼굴이 아니라 특징 패턴(얼굴 윤곽, 눈 위치, 코 그림자 ...)을 보여줌
# SVM 알고리즘은 실제 얼굴이 아니라 특징 패턴으로 분류작업을 한다.

print('---설명력 확인---')
print(m_pca.explained_variance_ratio_[:10])
print('누적 설명력 : ',np.sum(m_pca.explained_variance_ratio_)) # 0.9039658
# n = 100 개로 얼마나 원본 정보를 유지했는지 확인함.

# 원본 vs. 복원 이미지 비교
x_reconst = m_pca.inverse_transform(x_low)
fig, ax = plt.subplots(2, 5, figsize=(10, 4))
for i in range(5):
    # 원본
    ax[0, i].imshow(faces.images[i], cmap='bone')
    ax[0, i].set_title('원본')
    ax[0, i].axis('off')

    # 복원
    ax[1, i].imshow(x_reconst[i].reshape(faces.images[0].shape), cmap='bone')
    ax[1, i].set_title('복원')
    ax[1, i].axis('off')
plt.suptitle('PCA 복원 이미지 비교', fontsize=15)
plt.tight_layout()
plt.show()  # 원본과 복원된 이미지의 기본 특징은 크게 차이가 없다.  (패턴이 유지됨)

print()
# 분류 모델 생성
svcmodel = SVC(C = 1, random_state = 0)
mymodel = make_pipeline(m_pca, svcmodel) # PCA와 분류기를 하나의 파이프라인으로 묶어 순차적으로 실행
print('mymodel :', mymodel)
# Pipeline(steps=[('pca', PCA(n_components=100, random_state=0, whiten=True)),
#                 ('svc', SVC(C=1, random_state=0))])
mymodel.fit(faces.data, faces.target)

# train / test split 
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix,classification_report
x_train, x_test, y_train, y_test = train_test_split(faces.data, faces.target, stratify=faces.target, random_state=0)
print(x_train.shape, x_test.shape)  # (1011, 2914) (337, 2914)

mymodel.fit(x_train, y_train)
y_pred = mymodel.predict(x_test)
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10])
# 예측값 :  [3 7 1 1 2 7 3 1 3 3]
# 실제값 :  [0 4 1 1 2 7 3 1 3 2]
print(f"총 갯수: {len(y_test)}, 오류수: {(y_test != y_pred).sum()}")
# 총 갯수: 337, 오류수: 80
print(f"accuracy: {accuracy_score(y_test, y_pred)}")
# accuracy: 0.7626112759643917
confmat = confusion_matrix(y_test, y_pred)
print(f"confusion metrix\n {confmat}")
# confusion metrix
#  [[  7   2   0  10   0   0   0   0]
#  [  0  49   0   9   0   0   0   1]
#  [  0   2  13  15   0   0   0   0]
#  [  0   2   0 130   0   0   0   1]
#  [  0   1   0  10  15   0   0   1]
#  [  0   2   0   3   1  12   0   0]
#  [  0   1   0   5   0   0   9   0]
#  [  0   1   0  13   0   0   0  22]]
print(classification_report(y_test, y_pred, target_names=faces.target_names))

#                      precision   recall   f1-score   support
#      Ariel Sharon       1.00      0.37      0.54        19
#      Colin Powell       0.82      0.83      0.82        59
#   Donald Rumsfeld       1.00      0.43      0.60        30
#     George W Bush       0.67      0.98      0.79       133
# Gerhard Schroeder       0.94      0.56      0.70        27
#       Hugo Chavez       1.00      0.67      0.80        18
# Junichiro Koizumi       1.00      0.60      0.75        15
#        Tony Blair       0.88      0.61      0.72        36

#          accuracy                           0.76       337
#         macro avg       0.91      0.63      0.72       337
#      weighted avg       0.82      0.76      0.75       337

print('\n분류결과 시각화---')
# plt.subplots(1,1)
# plt.imshow(x_test[0].reshape(62, 47), cmap='bone') # 1차원 -> 2차원으로 변환
# plt.show()

# 여러개 보기
fig, ax = plt.subplots(4, 6)
for i, ax in enumerate(ax.flat):
    ax.imshow(x_test[i].reshape(62, 47), cmap='bone')
    ax.set(xticks=[], yticks=[])
    ax.set_ylabel(faces.target_names[y_pred[i]].split()[-1], color='b' if y_pred[i] == y_test[i] else 'red', fontweight='bold')

fig.suptitle('예측 결과', size=15)
plt.tight_layout()
plt.show() 

# 오차 행렬 시각화 (heatmap)
import seaborn as sns
# cm = confusion_matrix(y_test, y_pred)
# cm_df = pd.DataFrame(cm, index=faces.target_names, columns=faces.target_names)
plt.figure(figsize=(10, 8))
sns.heatmap(confmat,annot=True, fmt='d', cmap='Blues', xticklabels=faces.target_names, yticklabels=faces.target_names)
plt.xlabel('예측값')
plt.ylabel('실제값')
plt.title('Confusion Matrix')
plt.show()

# PCA 누적 분산 그래프 (왜 n_conponents=n 인가?)
import numpy as np
plt.plot(np.cumsum(m_pca.explained_variance_ratio_))
plt.xlabel('주성분 개수')
plt.ylabel('누적 설명력')
plt.title('PCA 누적 설명력')
plt.grid(True)
plt.show()

print('새로운 이미지를 입력해 분류하기---')
# 현재 모델의 분류 accurary : 0.2377151

# 실습 1. 기존 데이터로 테스트
test_img = faces.data[0].reshape(1,-1)  # (1,2914) 형태로 변환 : 모델이 일차원 형태로 학습.
print('test_img : ', test_img)
test_pred = mymodel.predict(test_img)
print('실습1 예측 결과 : ', faces.target_names[test_pred][0], 'index : ', test_pred[0])
print('실제값 : ', faces.target_names[faces.target[0]], 'index : ', faces.target[0])
# 실습1 예측 결과 :  Colin Powell     index :  1
# 실제값 :           Colin Powell     index :  1

print()
# 실습 2. 새로운 사진 데이터로 분류하기
# 외부 이미지(bush.jpg)를 불러와 모델이 학습한 규격(62x47)으로 변환 후 예측
from PIL import Image

img = Image.open("col.jpg").convert('L') # convert('L') : 흑백 변환
img = img.resize((47, 62)) # 모델 학습 사이즈 (width, height)
# numpy 이미지는 (height, width) - 세로, 가로
# PIL 이미지는 (width, height) - 가로, 세로
img_np = np.array(img)
img_np = img_np.astype('float32')

# [수정] 데이터 스케일링 맞춤 (LFW 데이터셋의 평균과 표준편차에 가깝게 조정)
# 특정 인물(George W Bush)로 편향되는 현상을 막기 위해 입력 이미지의 분포를 학습 데이터와 유사하게 정규화
img_np = (img_np - img_np.mean()) / img_np.std() # 로컬 정규화
img_np = img_np * 65 + 120 # LFW 데이터셋의 대략적인 분포로 복원

# 하이퍼파라미터 튜닝 (GridSearchCV) 적용 권장
# class_weight='balanced'를 추가하여 데이터 불균형(부시 대통령 사진이 압도적으로 많음) 문제를 해결
from sklearn.model_selection import GridSearchCV
param_grid = {'svc__C': [1, 5, 10, 50], 'svc__gamma': [0.0001, 0.0005, 0.001, 0.005], 'svc__class_weight': ['balanced']}
grid = GridSearchCV(mymodel, param_grid, cv=5)
grid.fit(x_train, y_train)
final_model = grid.best_estimator_

img_flat = img_np.reshape(1, -1)  # 1차원으로 변환
new_pred = final_model.predict(img_flat)
print('실습2 예측 결과 : ', faces.target_names[new_pred][0])

# 시각화 + 예측
plt.imshow(img_np, cmap='bone')
plt.title(f"예측 : {faces.target_names[new_pred][0]}")
plt.axis('off')
plt.show()

# 참고 : 정확도를 높이려면 밝기/위치 정렬 등의 작업 필요


"""
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.datasets import fetch_lfw_people
from sklearn.svm import SVC
from sklearn.decomposition import PCA 
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
from PIL import Image

# 1. 데이터 로드 (최소 60장 이상의 사진이 있는 인물만 선택)
faces = fetch_lfw_people(min_faces_per_person=60, color=False, resize=0.5)
X = faces.data
y = faces.target
target_names = faces.target_names

# 2. 학습/테스트 데이터 분리 (계층적 분할로 비율 유지)
x_train, x_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, stratify=y, random_state=0
)

# 3. 모델 파이프라인 구축
# - StandardScaler: 조명/밝기 정규화
# - PCA: 핵심 특징(Eigenfaces) 150개 추출
# - SVC: class_weight='balanced'를 통해 데이터 불균형(부시 쏠림) 해결
pca = PCA(n_components=150, whiten=True, random_state=0)
svc = SVC(kernel='rbf', class_weight='balanced', probability=True, random_state=0)
model_pipe = make_pipeline(StandardScaler(), pca, svc)

# 4. 하이퍼파라미터 튜닝 (GridSearchCV)
param_grid = {
    'svc__C': [1, 5, 10, 50],
    'svc__gamma': [0.0001, 0.0005, 0.001, 0.005]
}
grid = GridSearchCV(model_pipe, param_grid, cv=3)
grid.fit(x_train, y_train)

# 최적의 모델 추출
final_model = grid.best_estimator_
print(f"최적의 파라미터: {grid.best_params_}")

# 5. 테스트 데이터 평가
y_pred = final_model.predict(x_test)
print(f"테스트 데이터 정확도: {accuracy_score(y_test, y_pred):.4f}")
print("\n[상세 분류 보고서]")
print(classification_report(y_test, y_pred, target_names=target_names))

# 6. [실습] 외부 이미지(col.jpg) 분류하기
try:
    # 이미지 로드 및 전처리
    img = Image.open("bush.jpg").convert('L')
    img = img.resize((faces.images.shape[2], faces.images.shape[1])) # (47, 62)
    img_np = np.array(img).astype('float32').reshape(1, -1) # 1차원 변환

    # 예측 및 확률 포착
    new_pred = final_model.predict(img_np)
    new_pred_proba = final_model.predict_proba(img_np)[0]
    
    # 결과 시각화
    plt.figure(figsize=(5, 5))
    plt.imshow(np.array(img), cmap='bone')
    plt.title(f"예측: {target_names[new_pred[0]]}\n확률: {new_pred_proba[new_pred[0]]*100:.2f}%")
    plt.axis('off')
    plt.show()
    
    # 상위 3명 확률 출력
    print("\n--- 상위 3명 예측 확률 ---")
    top3_idx = np.argsort(new_pred_proba)[-3:][::-1]
    for i in top3_idx:
        print(f"{target_names[i]}: {new_pred_proba[i]*100:.2f}%")

except Exception as e:
    print(f"외부 이미지 처리 중 오류 발생: {e}")