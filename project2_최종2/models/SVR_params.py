# =========================
# SVR + Optuna + GroupKFold + Full Evaluation
# =========================

import pandas as pd
import numpy as np
import joblib

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score, GroupKFold
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.inspection import permutation_importance

import optuna

np.random.seed(4)

# =========================
# 1. Load data
# =========================
df_train = pd.read_csv("train_data.csv")
df_test = pd.read_csv("test_data.csv")

features = ['풍속(m/s)','비행고도(m)','2D이동거리(m)', "총회전량(deg)"]

X = df_train[features]
y = df_train["배터리소모율(%)"]

X_test = df_test[features]
y_test = df_test["배터리소모율(%)"]

groups = df_train["케이스ID"]

# =========================
# 2. Objective
# =========================
def objective(trial):

    C = trial.suggest_float("C", 1, 1e4, log=True)
    epsilon = trial.suggest_float("epsilon", 1e-3, 1.0, log=True)
    gamma = trial.suggest_float("gamma", 1e-4, 1e-2, log=True)

    model = make_pipeline(
        StandardScaler(),
        SVR(
            kernel="rbf",
            C=C,
            epsilon=epsilon,
            gamma=gamma
        )
    )

    cv = GroupKFold(n_splits=5)

    score = cross_val_score(
        model,
        X,
        y,
        cv=cv,
        groups=groups,
        scoring="neg_mean_absolute_error"
    ).mean()

    return -score

# =========================
# 3. Optuna
# =========================
study = optuna.create_study(
    direction="minimize",
    sampler=optuna.samplers.TPESampler(n_startup_trials=10),
    pruner=optuna.pruners.MedianPruner(n_warmup_steps=5)
)

study.optimize(objective, n_trials=1e3)

# =========================
# 4. Train FINAL MODEL
# =========================
best_params = study.best_params

best_model = make_pipeline(
    StandardScaler(),
    SVR(
        kernel="rbf",
        C=best_params["C"],
        epsilon=best_params["epsilon"],
        gamma=best_params["gamma"]
    )
)

best_model.fit(X, y)

# =========================
# 5. TEST EVALUATION
# =========================
y_pred = best_model.predict(X_test)

mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n========== TEST RESULT ==========")
print("MAE:", mae)
print("R2 :", r2)

# =========================
# 6. CASE 분석
# =========================
df_result = df_test.copy()

df_result["y_true"] = y_test.values
df_result["y_pred"] = y_pred
df_result["abs_error"] = abs(df_result["y_true"] - df_result["y_pred"])
df_result["bias"] = df_result["y_pred"] - df_result["y_true"]

print("\nTest case 개수:", df_result["케이스ID"].nunique())

# CASE별 MAE
case_mae = df_result.groupby("케이스ID")["abs_error"].mean()
print("\n=== CASE별 MAE ===")
print(case_mae)

# CASE별 실제 vs 예측
case_compare = df_result.groupby("케이스ID")[["y_true", "y_pred"]].mean()
print("\n=== CASE별 실제 vs 예측 평균 ===")
print(case_compare)

# CASE별 Bias
case_bias = df_result.groupby("케이스ID")["bias"].mean()
print("\n=== CASE별 Bias ===")
print(case_bias)

# Worst Case
worst_case = case_mae.sort_values(ascending=False)
print("\n=== WORST CASE TOP 5 ===")
print(worst_case.head())

# =========================
# 7. Feature Importance : 성능 감소량, 큰 값일 수록 모델이 해당 feature에 의존적.
# =========================
result = permutation_importance(
    best_model,
    X_test,
    y_test,
    n_repeats=30,
    random_state=4,
    scoring="neg_mean_absolute_error"
)

importance_mean = pd.Series(result.importances_mean, index=features)
importance_std = pd.Series(result.importances_std, index=features)

importance_mean = importance_mean.sort_values(ascending=False)

print("\n=== Feature Importance (성능 감소량) ===")
for f in importance_mean.index:
    print(f"{f}: {importance_mean[f]:.4f} ± {importance_std[f]:.4f}")

# =========================
# 8. CV vs TEST 비교
# =========================
print("\n========== CV vs TEST ==========")
print("Best CV MAE:", study.best_value)
print("TEST MAE   :", mae)

if mae > study.best_value:
    print("→ 과적합 가능성 있음")
else:
    print("→ 일반화 성능 양호")

# =========================
# 9. SAVE
# =========================
joblib.dump(best_model, "best_svr_model.pkl")
joblib.dump(best_params, "best_svr_model_params.pkl")

print("\nSaved model and params.")
print("Best params:", best_params)