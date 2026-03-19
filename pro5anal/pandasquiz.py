import numpy as np
import pandas as pd
from pandas import Series, DataFrame
# # 1)
# #   a) 표준정규분포를 따르는 9 X 4 형태의 DataFrame을 생성하시오. 
# data = pd.DataFrame(np.random.randn(9,4))
# print(data)

# #   b) a에서 생성한 DataFrame의 칼럼 이름을 - No1, No2, No3, No4로 지정하시오
# data.columns = ['No1','No2','No3','No4']
# print(data)

# #   c) 각 컬럼의 평균을 구하시오. mean() 함수와 axis 속성 사용
# print(data.mean(axis=0))

# print()
# # 2)
# # a) DataFrame으로 위와 같은 자료를 만드시오. colume(열) name은 numbers, row(행) name은 a~d이고 값은 10~40.
# numbers = pd.DataFrame(np.arange(10,50,10), columns=['numbers'], index=['a','b','c','d'])
# print(numbers)
# # b) c row의 값을 가져오시오.
# print(numbers.loc["c"])
# # c) a, d row들의 값을 가져오시오.
# print(numbers.iloc[0:4:3])
# # d) numbers의 합을 구하시오.
# print()
# print(numbers.sum())
# # e) numbers의 값들을 각각 제곱하시오. 아래 결과가 나와야 함.
# print(numbers ** 2)
# print()
# # f) floats 라는 이름의 칼럼을 추가하시오. 값은 1.5, 2.5, 3.5, 4.5    아래 결과가 나와야 함.
# floats = [1.5, 2.5, 3.5, 4.5]
# numbers['floats'] = floats
# print(numbers)
# # g) names라는 이름의 다음과 같은 칼럼을 위의 결과에 또 추가하시오. Series 클래스 사용.
# names = pd.Series(['길동','오정','팔계','오공'], index=['d','a','b','c'])
# print(names)
# print()
# numbers['names'] = names
# print(numbers)

# pandas 문제 3)

# 1) 5 x 3 형태의 랜덤 정수형 DataFrame을 생성하시오. (범위: 1 이상 20 이하, 난수)
data = DataFrame(np.random.choice(range(1,21),15).reshape(5,3))
print(data)
# 2) 생성된 DataFrame의 컬럼 이름을 A, B, C로 설정하고, 행 인덱스를 r1, r2, r3, r4, r5로 설정하시오.
col = ["A","B","c"]
row = ['r1','r2','r3','r4','r5']
data.columns = col
data.index = row
print(data)
# 3) A 컬럼의 값이 10보다 큰 행만 출력하시오.
print(data[data['A'] > 10])
# 4) 새로 D라는 컬럼을 추가하여, A와 B의 합을 저장하시오.
data.insert(3,'D',data['A'] + data['B'])
print(data)
# 5) 행 인덱스가 r3인 행을 제거하되, 원본 DataFrame이 실제로 바뀌도록 하시오.
print()
print(data.drop('r3', inplace=True))
print(data)
# 6) 아래와 같은 정보를 가진 새로운 행(r6)을 DataFrame 끝에 추가하시오.
data.loc['r6'] = [15, 10, 2, 15 + 10]
print(data)

# pandas 문제 4)
# 다음과 같은 재고 정보를 가지고 있는 딕셔너리 data가 있다고 하자.
data = {
    'product': ['Mouse', 'Keyboard', 'Monitor', 'Laptop'],
    'price':   [12000,     25000,      150000,    900000],
    'stock':   [  10,         5,          2,          3 ]
}
# 1) 위 딕셔너리로부터 DataFrame을 생성하시오. 단, 행 인덱스는 p1, p2, p3, p4가 되도록 하시오.
da = pd.DataFrame(data, index=['p1','p2','p3','p4'])
print(da)
# 2) price와 stock을 이용하여 'total'이라는 새로운 컬럼을 추가하고, 값은 'price x stock'이 되도록 하시오.
da.insert(3,'total',da['price'] * da['stock'])
print(da)
# 3) 컬럼 이름을 다음과 같이 변경하시오. 원본 갱신
#    product → 상품명,  price → 가격,  stock → 재고,  total → 총가격
col = ['상품명', '가격','재고','총가격']
da.columns = col
print(da)
# 4) 재고(재고 컬럼)가 3 이하인 행의 정보를 추출하시오.
print(da[da['재고'] <= 3])
# 5) 인덱스가 p2인 행을 추출하는 두 가지 방법(loc, iloc)을 코드로 작성하시오.
print('---' * 10)
print(da.loc[['p2']])
print('---' * 10)
print(da.iloc[:1])
# 6) 인덱스가 p3인 행을 삭제한 뒤, 그 결과를 확인하시오. (원본이 실제로 바뀌지 않도록, 즉 drop()의 기본 동작으로)
imsi = da.drop(['p3'])
print(imsi)
print(da)
# 7) 위 DataFrame에 아래와 같은 행(p5)을 추가하시오.
#             상품명             가격     재고    총가격
#  p5       USB메모리    15000     10    가격*재고

da.loc['p5'] = ['USB메모리', 15000, 10, 15000 * 10]
print(da)