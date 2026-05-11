import numpy as np
import pandas as pd
import joblib
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score

# ── 0. 데이터 로드 ─────────────────────────────────────────────
df_train = pd.read_csv('train_data.csv')
df_test  = pd.read_csv('test_data.csv')

# 시뮬레이션전체시간(s): 추후 추가 여부 판단 예정 (현재 제외)
FEATURES = ['풍속(m/s)', '비행고도(m)', '2D이동거리(m)', '총회전량(deg)']
TARGET   = '배터리소모율(%)'  # label: 배터리소모량

X_train = df_train[FEATURES].values
y_train = df_train[TARGET].values

X_test  = df_test[FEATURES].values
y_test  = df_test[TARGET].values

# ── 1. StandardScaler ─────────────────────────────────────────
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

# ── 2. Linear Regression 학습 ─────────────────────────────────
model = LinearRegression()
model.fit(X_train_scaled, y_train)

# ── 3. 평가 ───────────────────────────────────────────────────
y_pred_train = model.predict(X_train_scaled)
y_pred_test  = model.predict(X_test_scaled)

train_mae = mean_absolute_error(y_train, y_pred_train)
test_mae  = mean_absolute_error(y_test,  y_pred_test)
train_r2  = r2_score(y_train, y_pred_train)
test_r2   = r2_score(y_test,  y_pred_test)

print("=" * 45)
print("         Linear Regression 평가 결과")
print("=" * 45)
print(f"[Train]  MAE: {train_mae:.4f}%  |  R²: {train_r2:.4f}")
print(f"[Test]   MAE: {test_mae:.4f}%  |  R²: {test_r2:.4f}")
print("=" * 45)

# ── 4. 계수 확인 ──────────────────────────────────────────────
print("\n📌 회귀 계수 (StandardScaled 기준)")
for feat, coef in zip(FEATURES, model.coef_):
    print(f"  {feat:<22s}: {coef:+.4f}")
print(f"  {'절편':<22s}: {model.intercept_:+.4f}")

# ── 5. Test 케이스별 예측 비교 ────────────────────────────────
print("\n📋 Test 케이스 예측 vs 실제")
print(f"{'케이스ID':<12} {'실제':>8} {'예측':>8} {'오차':>8}")
print("-" * 42)
for i, row in df_test.iterrows():
    actual = y_test[i]
    pred   = y_pred_test[i]
    print(f"{row['케이스ID']:<12} {actual:>6.2f}%  {pred:>6.2f}%  {pred-actual:>+6.2f}%")

# ── 6. 모델 저장 (joblib) ─────────────────────────────────────
# joblib.dump({'model': model, 'scaler': scaler, 'features': FEATURES}, 'lr_model.pkl')
# print("\n✅ 모델 저장 완료: lr_model.pkl")