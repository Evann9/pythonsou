# Support Vector Regression(SVR)

# kernel : 데이터를 어떤 방식으로 변환해서 직선으로 만들지 
# linear : 직선 회귀 
# rbf : 기본 비선형 

# # C : 규제 강도 (50~200) 
# 1 : 강한 규제 
# 10 : 기본 100 : 복잡 데이터 대응 

# epsilon : 오차 무시 2% 설정했으니까 0.05~2 정도 
# 0.01 : 매우 민감 0.1 : 기본 0.2 : 스무스

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.model_selection import cross_val_score

np.random.seed(4)

# =========================
# 1. Load data
# =========================
df_train = pd.read_csv("train_data.csv")
# features = ['풍속(m/s)','비행고도(m)','2D이동거리(m)', '총회전량(deg)', '시뮬레이션전체시간(s)']
features = ['풍속(m/s)','비행고도(m)','2D이동거리(m)', '총회전량(deg)']

X = df_train[features]
y = df_train["배터리소모율(%)"]

# =========================
# 2. Scaling
# =========================
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# =========================
# 3. Kernel evaluation function
# =========================
def evaluate_kernel(kernel_name):

    best_score = float("inf")

    # GridSearch
    C_list = np.logspace(0, 2.48, 10)   # 10^0 ~ 10^2.48
    epsilon_list = np.linspace(0.01, 0.3, 15)

    for C in C_list:
        for eps in epsilon_list:

            if kernel_name == "rbf":
                model = SVR(kernel="rbf", C=C, gamma="scale", epsilon=eps)
            else:
                model = SVR(kernel="linear", C=C, epsilon=eps)

            score = cross_val_score(
                model,
                X_scaled,
                y,
                cv=5,
                scoring="neg_mean_absolute_error"
            ).mean()

            mae = -score

            if mae < best_score:
                best_score = mae

    return best_score

# =========================
# 4. Evaluate both kernels
# =========================
linear_mae = evaluate_kernel("linear")
rbf_mae = evaluate_kernel("rbf")

print("Linear best MAE:", linear_mae)
print("RBF best MAE:", rbf_mae)

# =========================
# 5. Decision
# =========================
if rbf_mae < linear_mae:
    print("Best kernel: RBF")
else:
    print("Best kernel: Linear")

# Linear best MAE: 8.971178730651356
# RBF best MAE: 6.282351547561782
# Best kernel: RBF
