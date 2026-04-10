# [XGBoost 문제] 
# 유리 식별 데이터베이스(glass.csv)를 읽어 7가지 label(Type) 분류 작업을 수행하시오.

import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
import warnings ; warnings.filterwarnings('ignore')

# 데이터 로드
df = pd.read_csv("glass.csv")
print(df.head(3), df.shape) # (214, 10)

# 독립변수(X)와 종속변수(y) 분리
x = df.drop('Type', axis=1)
y = df['Type']

# XGBoost 레이블 0부터 시작하도록 인코딩 (XGBoost 인식 유리)
encoding = LabelEncoder()
y_enc = encoding.fit_transform(y)

# 데이터 분할
X_train, X_test, y_train, y_test = train_test_split(x, y_enc, test_size=0.3, random_state=42, stratify=y_enc)

# 모델 생성 및 학습
xgb_model = xgb.XGBClassifier(
    n_estimators=200,
    max_depth=6,
    random_state=42,
    eval_metric='logloss'
)
xgb_model.fit(X_train, y_train)

# 예측 및 평가
y_pred = xgb_model.predict(X_test)
print(f"분류 정확도 : {accuracy_score(y_test, y_pred):.4f}")  # 분류 정확도 : 0.7846
print("\n[상세 분류 보고서]")
print(classification_report(y_test, y_pred, target_names=[str(c) for c in encoding.classes_]))