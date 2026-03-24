# pandas 문제 7)

#  a) MariaDB에 저장된 jikwon, buser, gogek 테이블을 이용하여 아래의 문제에 답하시오.

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
    conn = pymysql.connect(**config)
    cursor = conn.cursor() 
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        """  
    cursor.execute(sql) 

    rows = cursor.fetchall()

#      - 사번, 이름, 부서명, 연봉, 직급을 읽어 DataFrame을 작성
    df1 = pd.DataFrame(rows,
                    columns= ['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwonpay'])

#      - DataFrame의 자료를 파일로 저장
    with open('pandasdbquiz1.csv', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    df2 = pd.read_csv('pandasdbquiz1.csv', header=None, names=['번호', '이름', '부서명', '직급', '연봉'])

    df = pd.read_sql(sql, conn) 
    df.columns = ['번호', '이름', '부서명', '직급', '연봉']

#      - 부서명별 연봉의 합, 연봉의 최대/최소값을 출력
    print()
    print('연봉 최대값 : ', df['연봉'].max()) 
    print('연봉 최소값 : ', df['연봉'].min()) 

#      - 부서명, 직급으로 교차 테이블(빈도표)을 작성(crosstab(부서명, 직급))
    print()
    ctab = pd.crosstab(df['부서명'], df['직급']) 
    print('교차표\n' ,ctab)

#      - [문제] 직원별 담당 고객자료(고객번호, 고객명, 고객전화)를 출력하세요. (담당 고객이 없으면 "담당 고객 X"라고 표시)
    print(
    pd.read_sql("""
                select jikwonname as 직원, ifnull(gogekno, "담당 고객 X") as 고객번호, 
                gogekname as 고객명, gogektel as 고객전화 from gogek 
                right outer join jikwon on jikwon.jikwonno = gogek.gogekdamsano 
                group by jikwonname;
                """, conn))

#      - [문제] quantile() 함수를 사용하여 연봉이 상위 20%에 속하는 직원들을 출력하세요.
    print()
    st1 = df['연봉'].quantile(0.8)
    ru1 = df['연봉'] >= st1
    print("연봉 상위 20% 직원 : " , df[ru1]['이름'].to_list())

#      - [문제] 연봉 중앙값(median)을 기준으로 상위 50%인 데이터만 필터링한 후, 직급별 평균 연봉을 구하세요.
    print()
    st2 = df['연봉'].median()
    ru2 = df['연봉'] >= st2
    print(df[ru2].groupby(['직급'])['연봉'].mean())

#      - [문제] 부서별 연봉 평균을 계산하여 가로 막대 그래프(barh)로 시각화하세요.
    pay_mean = df.groupby(['부서명'])['연봉'].mean()  
    # print(pay_mean)
    plt.barh(pay_mean.index, pay_mean.values)  # explode: 조각 돌출, shadow: 그림자
    plt.show()

except Exception as e:
    print('처리오류 : ' , e)
finally:
    cursor.close()
    conn.close()

#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
#      - pivot_table을 사용하여 성별 연봉의 평균을 출력
#      - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
#      - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서명, 성별))


#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#       조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#      사번  직원명  부서명   직급  부서명전화  성별
#      ...
#      인원수 : * 명
#     - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
#     - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력



# pandas 문제 8)

# MariaDB에 저장된 jikwon, buser 테이블을 이용하여 아래의 문제에 답하시오.

# Django(Flask) 모듈을 사용하여 결과를 클라이언트 브라우저로 출력하시오.



#    1) 사번, 직원명, 부서명, 직급, 연봉, 근무년수를 DataFrame에 기억 후 출력하시오. (join)

#        : 부서명번호, 직원명 순으로 오름 차순 정렬 

#    2) 부서명, 직급 자료를 이용하여  각각 연봉합, 연봉평균을 구하시오.

#    3) 부서명별 연봉합, 평균을 이용하여 세로막대 그래프를 출력하시오.

#    4) 성별, 직급별 빈도표를 출력하시오.