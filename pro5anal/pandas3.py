# 연산
from pandas import Series, DataFrame
import numpy as np

s1 = Series([1,2,3], index=['a','b','c'])
s2 = Series([4,5,6,7], index=['a','b','d','c'])
print(s1)
print(s2)
print(s1 + s2)  # 같은 인덱스끼리 연산, 불일치 시 NaN을 반환
print(s1.add(s2)) # numpy 함수를 계승

print(s1.mul(s2))  # sub, div

print()
df1 = DataFrame(np.arange(9).reshape(3,3), columns=list('kbs'), index=['서울','대전','부산'])
df2 = DataFrame(np.arange(12).reshape(4,3), columns=list('kbs'), index=['서울','대전','제주','광주'])

print(df1)
print(df2)
print(df1 + df2)  # 같은 인덱스끼리 연산
print(df1.add(df2, fill_value=0))  # NaN은 0으로 채운 후 연산에 참여
# sub, mul, div 도 가능

print('NaN(결측값 처리) ------------------')
df = DataFrame([[1.4, np.nan], [7, -4.5], [np.nan, np.nan], [0.5, -1]], columns=['one','two'])
print(df)

print()
print(df.isnull())   # null 값 탐지
print(df.notnull())

print()
print(df.dropna())
print(df.dropna(how='any'))  # 하나라도 NaN값이 있으면 삭제
print()
print(df.dropna(how='all'))  # 모든 값이 NaN이면 삭제
print()
print(df.dropna(subset=['one'])) # 특정 열에 NaN이 있는 행 삭제
print()
print(df.dropna(subset=['two'])) 
print()
print(df.dropna(axis='rows'))     
print(df.dropna(axis='columns'))  # NaN이 있는 행/열 삭제

print()
print(df)
imsi = df.drop(1)  # 원본 삭제 안됨. 삭제된 결과가 새로운 dataFrame으로 생성됨.
print(imsi)
print(df)
print()
# imsi = df.drop(1, inplace=True)  # 원본 삭제
# print(df)

print()
# 계산 관련 메소드
print(df.sum())        # 열의 합 - NaN은 연산에서 제외
print(df.sum(axis=0, skipna=True))   # 생략 가능

print(df.sum(axis=1))  # 행의 합 

print()
print(df.describe())  # 요약 통계량 출력
print(df.info())  # 구조 출력

print()
words = Series(['봄','여름','가을','봄'])
print(words.describe())


