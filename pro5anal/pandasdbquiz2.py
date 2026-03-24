#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.

import pymysql
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

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
        select jikwonno, jikwonname, busername, jikwonjik, jikwongen, jikwonpay from jikwon
        inner join buser on jikwon.busernum = buser.buserno
        """  
    cursor.execute(sql) 

    rows = cursor.fetchall()

    #   - pivot_table을 사용하여 성별 연봉의 평균을 출력
    df3 = pd.DataFrame(rows, columns=['jikwonno', 'jikwonname', 'busername', 'jikwonjik','jikwongen', 'jikwonpay'])
    gen_pay_pivot = df3.pivot_table(values='jikwonpay' , columns='jikwongen', aggfunc='mean')
    print(gen_pay_pivot)
    
    #   - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
    print()
    gen_pay_m = df3.groupby(['jikwongen'])['jikwonpay'].mean()  # 직급별 연봉
    print(gen_pay_m)

    plt.bar(gen_pay_m.index, gen_pay_m.values)
    plt.show()

    #   - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서명, 성별))
    print()
    ktab = pd.crosstab(df3['busername'], df3['jikwongen']) 
    print('교차표\n' ,ktab)

except Exception as e:
    print('처리오류 : ' , e)
finally:
    cursor.close()
    conn.close()
