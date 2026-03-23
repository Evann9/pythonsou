# DataFrame 재구 조화 (열을 행으로, 행을 열로 이동)
import pandas as pd
import numpy as np

df = pd.DataFrame(1000 + np.arange(6).reshape(2,3), index=['대전','서울'], columns=['2020','2021','2022'])
print(df)


# stack, unstack
print()
df_row = df.stack()   # stack: 열 인덱스를 행 인덱스의 하위 레벨로 변경 (Pivotting)
print(df_row)  
print()
df_col = df_row.unstack()  # unstack: 행 인덱스를 열 인덱스로 변경 (stack의 반대)
print(df_col)


print('\n범주화 ---------')
price = [10.3, 5.5, 7.8, 3.6]
cut = [3, 7, 9, 11]  # 구간 기준값
result_cut = pd.cut(price, cut)  # 연속형 -> 범주화
print(result_cut) # cut: 지정한 경계값을 기준으로 구간을 나눔. ( : 초과  ] : 이하   => (a,b] : a < x <= b
print(pd.Series(result_cut).value_counts())
# (3, 7]     2
# (7, 9]     1
# (9, 11]    1

print()
datas = pd.Series(np.arange(1,1001))
print(datas.head(3))  # head(n) :  데이터의 앞에 n개만 봄
print(datas.head(2))
result_cut2 = pd.qcut(datas, 3)  # qcut: 데이터를 동일한 개수를 갖는 n개의 구간으로 나눔
print(result_cut2)
print(pd.Series(result_cut2).value_counts())


print('\nnagg함수 : 범주의 그룹별 연산 ---------')
group_col = datas.groupby(result_cut2, observed=True) # groupby: 특정 기준에 따라 데이터를 그룹화
# print(group_col)
print(group_col.agg(['count','mean','std','min'])) # agg: 여러 개의 집계 연산을 한 번에 수행


# agg 대신 사용자 함수를 작성
def summaryFunc(gr):
    return {
        'count': gr.count(),
        'mean': gr.mean(),
        'std': gr.std(),
        'min': gr.min()
        }
print(group_col.apply(summaryFunc))  # apply: 사용자 정의 함수를 그룹별로 적용
print()
print(group_col.apply(summaryFunc).unstack())  


# merge
print('\nmerge : 데이터 프레임 객체 병합')
df1 = pd.DataFrame({'data1':range(7), 'key':['b','b','a','c','a','a','b']})
print(df1)
df2 = pd.DataFrame({'key':['a','b','d'],'data2':range(3)})
print(df2)
print()
print(pd.merge(df1, df2, on='key'))  # merge: 공통 열(key)을 기준으로 데이터 병합
print()
print(pd.merge(df1, df2, on='key', how='inner'))  # 교집합(inner join) 
print(pd.merge(df1, df2, on='key', how='outer'))  # 합집합(outer join)
print(pd.merge(df1, df2, on='key', how='left'))  # 왼쪽(df1) 기준 병합
print(pd.merge(df1, df2, on='key', how='right'))  # 오른쪽 기준

print()
# 공통 칼럼명이 없는 경우 df1 vs df3
df3 = pd.DataFrame({'key2':['a','b','d'],'data2':range(3)})
print(pd.merge(df1, df3, left_on='key', right_on='key2'))  # inner join

print('-----concat----')
print(pd.concat([df1, df3], axis=0))   # concat: 물리적으로 데이터를 이어 붙임 (axis=0: 위아래)
print(pd.concat([df1, df3], axis=1))   # axis=1: 좌우로 붙임


print('\n\n피벗 테이블(pivot table) : pivot과 groupby 명령의 중간적 성격')
# pivot : 데이터 열 중에서 두개의 열(key)을 사용해 데이터의 행렬을 재구성 (수치 데이터 꼭 필요함.)
data = {'city':['강남','강북','강남','강북'],
        'year':[2000,2001,2002,2002],
        'pop':[3.3,2.5,3.0,2.0]}
df = pd.DataFrame(data)
print(df)
print()
print(df.pivot(index='city', columns='year', values='pop')) # pivot: 데이터 재구조화 (단순 형태)
print(df.pivot(index='year', columns='city', values='pop'))
print()
print(df.set_index(['city','year']))  # set_index : 기존 행 인덱스를 제거하고 첫번째 열 인덱스 설정
print(df.set_index(['city','year']).unstack()) # unstack : 행 인덱스를 열 인덱스로 변경
print()
print(df['pop'].describe())
print()
print(df)
print(df.pivot_table(index=['city'], aggfunc='mean'))         # pivot_table: 집계(aggfunc) 기능을 포함한 피벗
print(df.pivot_table(index=['city', 'year'], aggfunc=[len,'sum']))
print(df.pivot_table(values='pop', index='city', aggfunc=len))
print()
print(df.pivot_table(values='pop', index='year', columns='city'))
print(df.pivot_table(values='pop', index='year', columns='city', margins=True)) # margins=True : 행/열 합계(All) 추가
print(df.pivot_table(values='pop', index='year', columns='city', margins=True, fill_value=0)) # fill_value = n : NaN 값 n으로 대체
print()
hap = df.groupby(['city'])
print(hap)
print(hap.sum())
print(df.groupby(['city']).sum())
print(df.groupby(['city']).mean())

# [pandas4.py 주요 함수 및 기능 정리]
# 1. stack() / unstack(): 데이터프레임의 구조 변경 (열 <-> 행 인덱스 레벨 이동)
# 2. pd.cut() / pd.qcut(): 연속형 데이터를 특정 구간(범주)으로 나누는 이산화 작업
# 3. groupby(): 특정 열을 기준으로 데이터를 그룹화하여 집계 준비
# 4. agg(): 그룹화된 데이터에 대해 여러 개의 통계 함수(count, mean 등)를 동시 적용
# 5. apply(): 사용자 정의 함수를 그룹별 또는 행/열별로 일괄 적용
# 6. pd.merge(): 공통 열(Key)을 기준으로 두 데이터프레임을 병합 (SQL Join 방식)
# 7. pd.concat(): 데이터를 축(axis)을 기준으로 물리적으로 이어 붙임
# 8. pivot(): 데이터의 열을 행과 열 인덱스로 재구성하여 형태 변경
# 9. pivot_table(): pivot 기능에 집계 연산(aggfunc) 및 합계(margins) 기능이 추가된 형태
# 10. set_index(): 특정 열을 데이터프레임의 행 인덱스로 설정
