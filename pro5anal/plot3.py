# seaborn lib : matplotlib를 더 편하게 사용할 수 있도록 만든 라이브러리
# matplotlib 기반의 고수준 인터페이스를 제공하여 통계 그래픽을 시각화하는 데 최적화됨

import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib
import pandas as pd

# 한글 폰트 설정 (koreanize_matplotlib가 설치된 경우 자동으로 처리되나 명시적 설정 가능)
plt.rc('font', family='Malgun Gothic') 
# plt.rcParams['axes.unicode_minus'] = False 
# sns.load_dataset: seaborn에서 제공하는 연습용 데이터셋(titanic) 로드
titanic = sns.load_dataset('titanic')
# print(titanic.info())
print(titanic.info(max_cols=None))

# sns.displot: 데이터의 분포를 시각화 (히스토그램 + 밀도 함수 등)
sns.displot(titanic['age'])
plt.title('나이 차트')
plt.show()

# sns.boxplot: 박스 플롯 생성 (데이터의 사분위수 및 이상치 확인)
sns.boxplot(y='age', data=titanic, palette='Paired')
plt.show()

# sns.relplot: 두 변수 간의 관계를 나타내는 산점도(기본값) 생성
sns.relplot(x='sex', y='age', data=titanic)
plt.show()

# pivot_table: 데이터를 재구조화하여 행(class)과 열(sex)에 따른 데이터 개수(size) 집계
titanic_pivot = titanic.pivot_table(index='class', columns='sex', aggfunc='size')
print(titanic_pivot)
# sns.heatmap: 수치 데이터를 색상으로 표현하는 열지도 생성 (annot=True: 수치 표시)
sns.heatmap(titanic_pivot, cmap=sns.light_palette('gray'), annot=True, fmt='d')
plt.show()

# ---------------------------------------------------------
# Boxplot 기준 이상치(outlier) 확인

# 1. 데이터 정의
data = [10, 12, 13, 15, 14, 12, 11, 100]  
df = pd.DataFrame({'score': data})

# 2. IQR 기반 이상치 탐지
Q1 = df['score'].quantile(0.25) # 1사분위수 (25%)
Q3 = df['score'].quantile(0.75) # 3사분위수 (75%)
IQR = Q3 - Q1                   # 사분위간 범위 (Interquartile Range)

lower_bound = Q1 - 1.5 * IQR    # 하한선
upper_bound = Q3 + 1.5 * IQR    # 상한선

# 3. 이상치, 정상치 분리 
# IQR(사분위간 범위)의 1.5배를 기준으로 하한선 미만 또는 상한선 초과인 값을 이상치(Outlier)로 판별
outliers = df[(df['score'] < lower_bound) | (df['score'] > upper_bound)]
# 불리언 인덱싱을 활용하여 하한선과 상한선 사이에 포함되는 정상 범위의 데이터만 필터링하여 추출
filtered_df = df[(df['score'] >= lower_bound) & (df['score'] <= upper_bound)]

# 4. 탐지된 이상치 데이터 출력 (인덱스와 값 확인)
print("이상치 값:")
print(outliers)

# 5. 박스플롯 시각화: 제거 전/후 비교
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

# 이상치 포함
sns.boxplot(y=df['score'], ax=axes[0], color='salmon')
axes[0].set_title('이상치 포함 데이터')
axes[0].set_ylabel('Score')
axes[0].grid(True)

# 이상치 제거 후
sns.boxplot(y=filtered_df['score'], ax=axes[1], color='lightblue')
axes[1].set_title('이상치 제거 후')
axes[1].set_ylabel('Score')
axes[1].grid(True)

plt.tight_layout() # 서브플롯 간의 간격을 자동으로 조절
plt.show()