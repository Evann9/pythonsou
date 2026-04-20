# sklearn 제공 Regressior 성능 비교
# pipeline + GridSearchCV + 교차검증 + 성능확인 + 시각화

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns

from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from xgboost import XGBRegressor

from sklearn.metrics import r2_score, mean_squared_error

data = load_diabetes()
# Pregnancies: 임신 여부, Glucose: 포도당 수치, BloodPressure: 혈압
# SkinThickness: 피부의 두께, Insulin: 인슐린 수치, BMI: 체질량 지수, 체중을 신장의 제곱으로 나눈 값
# DiabetesPedigreeFunction: 당뇨 혈통 함수, Age: 나이, Diabetes: 당뇨 여부, 예측 목표값
x = data.data
y = data.target
print(x[:2])   # [[ 0.03807591  0.05068012 ,,,
print(y[:2])   # [151.  75.]  : 연속형

x_train,x_test,y_train,y_test = train_test_split(
    x, y, test_size=0.2, random_state=42
)

# Pipeline + GridSearch
models = {
    "LinearRegression":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", LinearRegression())
        ]),
        "params":{
            "model__fit_intercept":[True, False]
        }
    },
    "RandomForest":{
        "pipeline":Pipeline([
            ("model", RandomForestRegressor(random_state=42))
        ]),
        "params":{
            "model__n_estimators":[100, 200],
            "model__max_depth":[None, 5, 10],
            "model__min_samples_split":[2, 5]
        }
    },
    "XGBoost":{
        "pipeline":Pipeline([
            ("model", XGBRegressor(random_state=42, verbosity=0))
        ]),
        "params":{
            "model__n_estimators":[100, 200],
            "model__learning_rate":[0.01, 0.05],
            "model__max_depth":[3, 5]
        }
    },
    "SVR":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", SVR())
        ]),
        "params":{
            "model__C":[0.1, 1, 10],
            "model__gamma":["scale", "auto"],
            "model__kernel":["rbf"]
        }
    },
    "KNN":{
        "pipeline":Pipeline([
            ("scaler", StandardScaler()),
            ("model", KNeighborsRegressor())
        ]),
        "params":{
            "model__n_neighbors":[3, 5, 7],
            "model__weights":["uniform", "distance"]
        }
    }
}

# GridSearchCV 실행
results = []
best_models = {}

# 각 모델을 순서대로 반복 처리 : best모델 추출, 성능 저장
for name, config in models.items():
    print(f"{name} 튜닝중 ...")
    grid = GridSearchCV(
        config["pipeline"],
        config["params"],
        cv = 5,
        scoring="r2",
        n_jobs=-1
    )
    grid.fit(x_train, y_train)

    best_model = grid.best_estimator_
    pred = best_model.predict(x_test)

    rmse = np.sqrt(mean_squared_error(y_test, pred))
    r2 = r2_score(y_test, pred)
    results.append([name, rmse, r2])
    best_models[name] = best_model
    print("best params : ", grid.best_params_)
    print("R2 : ", r2)   # 설명력

# 최종 결과 DataFrame에 저장
df_results = pd.DataFrame(results, columns=["modelname", "rmse", "r2"])
df_results = df_results.sort_values("r2", ascending=False)
print("최종 성능 비교")
print(df_results)

# 성능 비교를 위한 시각화
plt.figure(figsize=(12, 5))
# R2
plt.subplot(1, 2, 1)
sns.barplot(x="modelname", y="r2", data=df_results)
plt.title("튜닝 모델 결정계수")
plt.xticks(rotation=30)
# RMSE
plt.subplot(1, 2, 2)
sns.barplot(x="modelname", y="rmse", data=df_results)
plt.title("튜닝 모델 RMSE")
plt.xticks(rotation=30)

plt.tight_layout()
plt.show()

# Best model 예측 시각화
# 최고 모델 선택 (SVR이 1등)
best_modelname = df_results.iloc[0]["modelname"]
best_model = best_models[best_modelname]
pred = best_model.predict(x_test)

plt.figure(figsize=(6, 6))
plt.scatter(y_test, pred)
plt.plot([y_test.min(), y_test.max()],[y_test.min(), y_test.max()], 'r--')
plt.title(f'최고 모델 {best_modelname}')
plt.xlabel("실제값")
plt.xlabel("예측값")
plt.show()
