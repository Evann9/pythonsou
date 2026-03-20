import pandas as pd

items = {'apple':{'count':10, 'price':1500},
        'orange':{'count':5, 'price':800},
}

df = pd.DataFrame(items)
print(df)

# DataFrame 저장
# 클립보드로 저장
df.to_clipboard()   # 메모장 등으로 확인
print(df.to_html())
print(df.to_json())

df.to_csv('reslult1.csv', sep=',')  # 그대로 출력
df.to_csv('reslult2.csv', sep=',', index=False) # 인덱스 제외하고 출력
df.to_csv('reslult3.csv', sep=',', index=False, header=False)  # 순수 데이터만 출력
print()
df2 = df.T
print(df2)
df2.to_csv('reslult4.csv', sep=',', index=False, encoding='utf-8-sig')   # encoding='utf-8-sig' : 엑셀에서 읽을때 깨지는 것을 방지
redata = pd.read_csv('reslult4.csv')
print(redata)

print('\n엑셀 관련 ----------')
df3 = pd.DataFrame({
    'name':['Alice', 'Bob', 'oscar'],
    'age':[24,22,29],
    'city':['Seoul', 'suwon', 'incheon']
})
print(df3)

# 엑셀 파일 i/o

# 저장
df3.to_excel('result.xlsx', index=False, sheet_name='work1')

# 읽기
exdf = pd.ExcelFile("result.xlsx")
print(exdf.sheet_names)
print()

df4 = exdf.parse('work1')
print(df4)
print()
