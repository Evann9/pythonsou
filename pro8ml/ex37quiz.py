import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder

# 1. 데이터 로드
url = "https://raw.githubusercontent.com/pykwon/python/master/testdata_utf8/Heart.csv"
df = pd.read_csv(url)

# 2. 데이터 전처리
# 'Unnamed: 0' 컬럼(인덱스용)은 삭제
df = df.drop(['Unnamed: 0'], axis=1)

# [중요] 문제 조건: 문자 데이터 컬럼 제외
# 데이터프레임에서 수치형(int, float) 컬럼만 자동으로 골라냅니다.
df_numeric = df.select_dtypes(include=[np.number])

# 결측치(NaN) 처리: SVM은 결측치가 있으면 에러가 발생합니다.
df_numeric = df_numeric.dropna()

# 독립변수(X)와 종속변수(y) 설정
# y는 'AHD' 컬럼인데 문자열("Yes"/"No")이므로 수치화가 필요합니다.
X = df_numeric 
y = df.loc[df_numeric.index, 'AHD'] # X의 인덱스와 맞춤

# LabelEncoder로 AHD(Yes/No)를 0과 1로 변환
le = LabelEncoder()
y = le.fit_transform(y) 

# 3. 데이터 분할 (random_state 고정으로 재현성 확보)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 4. SVM 모델 생성 및 학습
# 정확한 확률 확인을 위해 probability=True 설정 필수!
model = svm.SVC(kernel='linear', C=1.0, probability=True, random_state=42)
model.fit(X_train, y_train)

# 5. 성능 평가
y_pred = model.predict(X_test)
print('예측값 : ', y_pred[:10])
print('실제값 : ', y_test[:10])
# 예측값 :  [0 1 1 0 0 1 0 0 0 1]
# 실제값 :  [0 1 0 1 0 1 0 1 0 1]
print(f"전체 정확도 : {accuracy_score(y_test, y_pred):.4f}")  # 0.7667
