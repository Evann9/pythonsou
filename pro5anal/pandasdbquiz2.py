#  b) MariaDB에 저장된 jikwon 테이블을 이용하여 아래의 문제에 답하시오.
#      - pivot_table을 사용하여 성별 연봉의 평균을 출력
#      - 성별(남, 여) 연봉의 평균으로 시각화 - 세로 막대 그래프
#      - 부서명, 성별로 교차 테이블을 작성 (crosstab(부서, 성별))

import pymysql
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
    conn   = pymysql.connect(**config)
    cursor = conn.cursor()

    sql = """
        SELECT j.jikwonno   AS 사번,
               j.jikwonname AS 직원명,
               b.busername  AS 부서명,
               j.jikwongen  AS 성별,
               j.jikwonpay  AS 연봉
        FROM   jikwon j
        INNER JOIN buser b ON j.busernum = b.buserno
    """
    from sqlalchemy import create_engine
    engine = create_engine("mysql+pymysql://root:123@127.0.0.1:3306/test")
    df = pd.read_sql(sql, engine)
    print(df.head(3))


    pt = pd.pivot_table(df, index='성별', values='연봉', aggfunc='mean')
    print('성별 연봉 평균 (pivot_table)')
    print(pt)
    print()


    pt.plot(kind='bar', legend=False, color=['steelblue', 'coral'], rot=0)
    plt.title('성별 평균 연봉')
    plt.xlabel('성별')
    plt.ylabel('연봉')
    plt.tight_layout()
    plt.show()


    ct = pd.crosstab(df['부서명'], df['성별'])
    print('부서명 성별 교차 테이블')
    print(ct)

except pymysql.OperationalError as e:
    print('DB 오류 :', e)
except Exception as e:
    print('처리 오류 :', e)
finally:
    try:
        cursor.close()
        conn.close()
    except:
        pass