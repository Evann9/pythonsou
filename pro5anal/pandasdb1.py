# SQLite 로컬 데이터베이스 연동 및 Pandas DataFrame 활용 예제
import sqlite3
import pandas as pd

# 1. 데이터베이스 연결 및 테이블 생성
# :memory:를 사용하여 메모리 상에 임시 DB 생성
conn = sqlite3.connect(':memory:')
sql = "create table if not exists extab(product varchar(10), maker varchar(10), weight real, price integer)"
conn.execute(sql)
conn.commit()

# 2. 데이터 삽입 (DML)
data = [('mouse', 'samsung', 12.5, 5000),
        ('keyboard', 'LG', 52.5, 35000)]
isql = "insert into extab values(?,?,?,?)"
conn.executemany(isql, data)      # 여러 개의 데이터를 리스트 형태로 한 번에 삽입
data1 = ('pen', 'abc', 5.0, 1200)
conn.execute(isql, data1)         # 단일 데이터 삽입
conn.commit()                     # 변경 사항 반영

# 3. 데이터 조회 (Cursor 활용)
cursor = conn.execute("select * from extab")
rows = cursor.fetchall()
for a in rows:
    print(a)

# 4. 조회 결과를 DataFrame으로 변환 (방법 1: 리스트 활용)
print('\n1. fetchall() 결과를 DataFrame으로 변환 ----')
df1 = pd.DataFrame(rows, columns=['product', 'maker', 'weight', 'price'])
print(df1)
print(df1.describe())             # 수치형 데이터 요약 통계량

# 5. SQL 쿼리를 직접 DataFrame으로 읽기 (방법 2: read_sql 활용)
print('\n2. pd.read_sql()을 사용하여 직접 읽기 ----')
df2 = pd.read_sql("select * from extab", conn)
print()
print(df2)
print()
print(pd.read_sql("select count(*) from extab", conn))

# 6. DataFrame 데이터를 DB 테이블에 저장 (Insert)
data = {
    'product':['연필','볼펜','지우개'],
    'maker':['모나미','모나미','모나미'],
    'weight':[2.3,3.0,5.0],
    'price':(1000, 2000, 500)
}
frame = pd.DataFrame(data)

# to_sql: DataFrame을 SQL 테이블로 저장
# if_exists='append': 기존 테이블이 있으면 데이터를 추가 (replace: 교체, fail: 중단)
frame.to_sql('extab', conn, if_exists='append', index=False)

# 7. 최종 데이터 확인
df3 = pd.read_sql("select * from extab", conn)
print('\n3. 데이터 추가 후 전체 테이블 조회 ----')
print(df3)

cursor.close()                    # 커서 닫기
conn.close()                      # DB 연결 종료