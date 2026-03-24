# iris dataset : 150 행, 3가지 종류, 4개의 특성
import pandas as pd
import matplotlib.pyplot as plt

# %matplotlib inline  # jupyter notebook에서 실습 시 show() 생략

iris_data = pd.read_csv('https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/iris.csv')
print(iris_data.info())
print(iris_data.head(3))
print(iris_data.tail(3))

# 산점도
plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'])
plt.xlabel('Sepal_Length')
plt.ylabel('Petal.Length')
plt.title('iris data')
plt.show()

print()
print(iris_data['Species'].unique())
# print(set(iris_data['Species']))
cols = []  # 꽃의 종류에 따라 다른색 기억
for s in iris_data['Species']:
    choice = 0
    if s == 'setosa':
        choice = 1
    elif s == 'versicolor':
        choice = 2
    elif s == 'virginica':
        choice = 3
    cols.append(choice)

plt.scatter(iris_data['Sepal.Length'], iris_data['Petal.Length'], c=cols)
plt.xlabel('Sepal_Length')
plt.ylabel('Petal.Length')
plt.title('iris data')
plt.show()

# pandas의 시각화 기능
from pandas.plotting import scatter_matrix
iris_col = iris_data.loc[:, 'Sepal.Length':'Petal.Width']
scatter_matrix(iris_col, diagonal='kde')
plt.show()

# seaborn 
import seaborn as sns
sns.pairplot(iris_data, hue='Species',  height=2)
plt.show()
