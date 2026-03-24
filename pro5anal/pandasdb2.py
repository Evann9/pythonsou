# 원격 DB 연동  - jikwon 자료를 읽어 dataFrame에 저장
import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import csv

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8'
}
try:
    # 1. DB 연결 및 데이터 조회
    conn = pymysql.connect(**config)
    cursor = conn.cursor()  # 커서 객체 생성
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        """  # 직원 정보와 부서명을 조인하는 쿼리
    cursor.execute(sql)  # SQL 실행
    
    # fetchall(): 모든 데이터를 튜플 형태로 가져옴 (변수에 저장해야 재사용 가능)
    rows = cursor.fetchall() 

    # 2. 조회된 데이터를 DataFrame으로 변환
    df1 = pd.DataFrame(rows,
                    columns= ['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwongen', 'jikwonpay'])
    print(df1.head(3))  # 상위 3개 행 출력
    print('연봉의 총합 : ', df1['jikwonpay'].sum())  # 수치 데이터 합계 계산

    print()
    # 3. CSV 파일 저장 및 읽기 (표준 csv 모듈 활용)
    with open('pandasdb2.csv', mode='w', encoding='utf-8') as fobj:
        writer = csv.writer(fobj)
        for row in rows:
            writer.writerow(row)  # 행 단위로 파일 기록
    
    # header=None: 파일에 컬럼명이 없을 때 사용, names: 새 컬럼명 지정
    df2 = pd.read_csv('pandasdb2.csv', header=None, names=['번호', '이름', '부서', '직급', '성별', '연봉'])
    print(df2.head(3))
    
    # 4. Pandas의 read_sql 함수 사용 (가장 권장되는 방식)
    print('\npandas의 read_sql 함수 사용')
    df = pd.read_sql(sql, conn)  # SQL 결과를 즉시 DataFrame으로 로드
    df.columns = ['번호', '이름', '부서', '직급', '성별', '연봉']  # 컬럼명 한글화
    
    # 데이터 슬라이싱 및 필터링
    print(df.head(2))  # 상위 2개
    print(df[:2])      # 인덱스 슬라이싱
    print(df[:-28])    # 뒤에서 28개 제외
    print(df['이름'].count(), ' ', len(df))  # 데이터 개수 확인
    
    # 통계 및 분석
    print('부서별 인원수 : ', df['부서'].value_counts())  # 범주별 빈도수
    print('연봉 7000이상 : ', df[df['연봉'] >= 7000])    # 불리언 인덱싱(조건 필터)
    
    # crosstab: 성별과 직급 간의 빈도 교차표 생성
    ctab = pd.crosstab(df['성별'], df['직급']) 
    print('교차표\n' ,ctab)

    # 5. 데이터 시각화 (직급별 평균 연봉)
    jik_ypay = df.groupby(['직급'])['연봉'].mean()  # 직급별 연봉
    print('jik_ypay : ', jik_ypay)

    # 파이 차트 생성
    plt.pie(jik_ypay, explode=(0.2,0,0,0.3,0),
            labels=jik_ypay.index,
            shadow=True, counterclock=False)  # explode: 조각 돌출, shadow: 그림자
    plt.show()
    
except Exception as e:
    print('처리오류 : ' , e)  # 예외 발생 시 메시지 출력
finally:
    cursor.close()  # 커서 닫기
    conn.close()    # DB 연결 종료