#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#      조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#      사번  직원명  부서명   직급  부서전화  성별
#      ...
#      인원수 : * 명
#     - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
#     - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력

import MySQLdb
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
    conn = MySQLdb.connect(**config)
    cursor = conn.cursor() 
    sql = """
        select jikwonno, jikwonname, busername, jikwonjik, jikwonpay, jikwongen, busertel from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        """  
    cursor.execute(sql) 

    rows = cursor.fetchall()

    df1 = pd.DataFrame(rows,
                    columns= ['jikwonno', 'jikwonname', 'busername', 'jikwonjik', 'jikwonpay', 'jikwongen', 'busertel'])

    with open('pandasdbquiz3.csv', mode='w', encoding='utf-8') as f:
        writer = csv.writer(f)
        for row in rows:
            writer.writerow(row)

    df2 = pd.read_csv('pandasdbquiz3.csv', header=None, names=['사번', '직원명', '부서명', '직급', '연봉', '성별', '부서전화'])

    df = pd.read_sql(sql, conn) 
    df.columns = ['사번', '직원명', '부서명', '직급', '연봉', '성별', '부서전화']

     



except MySQLdb.OperationalError as e:
    print('처리오류 : ' , e)
finally:
    cursor.close()
    conn.close()