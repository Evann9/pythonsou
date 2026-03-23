import pandas as pd

items = {'apple':{'count':10, 'price':1500},
        'orange':{'count':5, 'price':800},
}

df = pd.DataFrame(items)
print(df)

# DataFrame 저장
# to_clipboard: 데이터를 클립보드로 복사 (엑셀이나 메모장에 붙여넣기 가능)
df.to_clipboard()   
print(df.to_html())  # to_html: HTML 테이블 태그 형태로 변환
print(df.to_json())  # to_json: JSON 문자열 형태로 변환

# to_csv: CSV 파일로 저장
df.to_csv('reslult1.csv', sep=',')  
df.to_csv('reslult2.csv', sep=',', index=False) # index=False: 행 인덱스 제외
df.to_csv('reslult3.csv', sep=',', index=False, header=False)  # header=False: 컬럼명 제외
print()
df2 = df.T  # T: 전치 (행과 열을 바꿈)
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

# to_excel: DataFrame 객체를 엑셀 파일로 저장
df3.to_excel('result.xlsx', index=False, sheet_name='work1')

# ExcelFile: 엑셀 파일을 읽기 위한 객체 생성 (여러 시트 접근 시 유용)
exdf = pd.ExcelFile("result.xlsx")
print(exdf.sheet_names)  # sheet_names: 엑셀 파일 내의 모든 시트 이름 확인
print()

df4 = exdf.parse('work1')  # parse: 특정 시트의 데이터를 DataFrame으로 읽기
print(df4)
print()
