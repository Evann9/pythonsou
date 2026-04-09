# Decision Tree (의사결정나무) 분류 모델
# 데이터 균일도에 따른 규칙기반의 결정트리
# 트리는 데이터를 직각(수직, 수평) 기준으로 나누면서 영역을 만든다.

from sklearn.datasets import make_classification
from sklearn.tree import DecisionTreeClassifier, plot_tree
import matplotlib.pyplot as plt
import numpy as np

x, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_informative=2, random_state=42)

model = DecisionTreeClassifier(criterion='gini', max_depth=3)  # 최대 깊이 : 3
model.fit(x, y)   # 입력데이터, 정답데이터 <-_ supervised learning

# 트리구조 시각화
plt.figure(figsize=(10, 6))
plot_tree(model, feature_names=['x1', 'x2'], class_names=['0', '1'], filled=True)
plt.show()

# 결정경계 시각화
xx, yy = np.meshgrid(
    # x1 범위를 100개 구간으로 나눔.
    np.linspace(x[:, 0].min() , x[:, 0].max(), 100),
    # x2 범위 
    np.linspace(x[:, 1].min() , x[:, 1].max(), 100)
)
# 모든 좌표에 대해 예측값 계산
z = model.predict(np.c_[xx.ravel(), yy.ravel()])
z = z.reshape(xx.shape)  # 예측 결과를 원래 grid로 변환
print(z)

# 시각화
plt.contourf(xx, yy, z, alpha=0.3)  # 영역을 색으로 채워 결정경계 표현
plt.scatter(x[:, 0], x[:, 1], c=y)
plt.title("Decision Boundary")
plt.xlabel("x1")
plt.ylabel("x2")
plt.show()