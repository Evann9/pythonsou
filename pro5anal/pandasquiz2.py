import pandas as pd
import numpy as np

df=pd.read_csv('titanic_data.csv')

bins=[1,20,35,60,150]
labels=["소년","청년","장년","노년"]
df['나이대']=pd.cut(df['Age'],bins=bins,labels=labels)
result=df.groupby('나이대',observed=True)['Survived'].sum()
result=result.reset_index()
result.columns=['나이대','생존자수']
print(result)
print()

# 2)

# 나이대 컬럼 생성
bins = [1, 20, 35, 60, 150]
labels = ["소년", "청년", "장년", "노년"]
df['나이대'] = pd.cut(df['Age'], bins=bins, labels=labels)

# 샘플1 
pivot1 = df.pivot_table(
    values='Survived',
    index='Sex',
    columns='Pclass',
    aggfunc='mean'
)
print(pivot1)
print()

# 샘플2 
pivot2 = df.pivot_table(
    values='Survived',
    index=['Sex', '나이대'],
    columns='Pclass',
    aggfunc='mean'
)
pivot2 = (pivot2 * 100).round(2)
print(pivot2)

# 문제 6번 

# 1)
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/human.csv",skipinitialspace=True)
print(df)

df.columns = df.columns.str.strip()

# Group이 NA인 행은 삭제
print(df.dropna(subset=["Group"]))
df1 = df.dropna(subset=["Group"])

# Career, Score 칼럼을 추출하여 데이터프레임을 작성
print(df1[['Career', 'Score']])

# Career, Score 칼럼의 평균계산
print(df1[['Career', 'Score']].mean())

# 2)
df3 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/tips.csv")

# 파일 정보 확인
print(df3.info())

# 앞에서 3개의 행만 출력
print(df3.head(3))

# 요약 통계량 보기
print(df3.describe())

# 흡연자, 비흡연자 수를 계산  : value_counts()
print(df3["smoker"].value_counts())

# 요일을 가진 칼럼의 유일한 값 출력  : unique()
print(df3["day"].unique())