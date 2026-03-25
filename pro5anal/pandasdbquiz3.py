#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#      조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#      사번  직원명  부서명   직급  부서전화  성별
#      ...
#      인원수 : * 명
#     - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
#     - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력

import pymysql
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import seaborn as sns
import os

config = {
    'host':'127.0.0.1',
    'password':'123',
    'user':'root',
    'database' : 'test',
    'port':3306,
    'charset':'utf8'
}

try:
    conn = pymysql.connect(**config)
    cursor = conn.cursor()
    sql="""
        select 
            jikwonno, jikwonname, busername, jikwonjik, busertel, jikwongen, jikwonpay, 
            gogekno, gogekname, gogektel 
        from jikwon
        inner join buser on jikwon.busernum=buser.buserno
        left outer join gogek on jikwon.jikwonno=gogek.gogekdamsano
    """

    cursor.execute(sql)
    df_raw = pd.DataFrame(cursor.fetchall(), columns=['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉', '고객번호', '고객명', '고객전화'])
    df = df_raw.drop_duplicates(subset=['사번'])
    
except pymysql.OperationalError as e:
    print(e)

finally:
    cursor.close()
    conn.close()

# print(df)
# os._exit(0)

#  c) 키보드로 사번, 직원명을 입력받아 로그인에 성공하면 console에 아래와 같이 출력하시오.
#   조건 :  try ~ except MySQLdb.OperationalError as e:      사용
#   사번  직원명  부서명   직급  부서전화  성별
#   ...
#   인원수 : * 명
dfc = df[['사번', '이름', '부서명', '직급', '부서전화', '성별', '연봉']]
dfc = dfc.rename(columns={'이름': '직원명'})
# print(dfc)

while True:
    jikwonno = input('사번을 입력하세요. 종료:q\t')

    if jikwonno == 'q':
        break

    if not jikwonno.isdigit(): 
        print('사번은 숫자만 입력하세요\n')
        continue

    jikwonname = input('이름을 입력하세요. 종료:q\t')
    if jikwonname == 'q':
        break

    if any(dfc['사번'] == int(jikwonno)):
        name = dfc[dfc['사번'] == int(jikwonno)]['직원명'].iloc[0]
        if name == jikwonname:
            # 전직원 출력
            print(dfc.drop(columns=['연봉'], axis=1))
            print("인원수 : ", dfc['사번'].count(), "명")

            male = dfc[dfc['성별']=='남']['연봉']
            female = dfc[dfc['성별']=='여']['연봉']

            figure, ((ax1,ax2),(ax3,ax4)) = plt.subplots(nrows=2, ncols=2)
            figure.set_size_inches(15,10)

            # - 성별 연봉 분포 + 이상치 확인    <== 그래프 출력
            sns.boxplot(y=male, ax=ax1)
            sns.boxplot(y=female, ax=ax2)

            ax1.set(xlabel='남성', ylabel='연봉[원]', title='남성 연봉 분포')
            ax2.set(xlabel='여성', ylabel='연봉[원]', title='여성 연봉 분포')

            # - Histogram (분포 비교) : 남/여 연봉 분포 비교    <== 그래프 출력
            sns.histplot(data=male, bins=10, ax=ax3)
            sns.histplot(data=female, bins=10, ax=ax4)

            ax3.set(xlabel='연봉[원]', ylabel='인원수[명]', title='남성 연봉 분포 비교')
            ax4.set(xlabel='연봉[원]', ylabel='인원수[명]', title='여성 연봉 분포 비교')

            plt.show()
            break
        else:
            print("사번과 이름 정보가 일치하지 않습니다.\n")
    else: print("존재하지 않는 사번 입니다.\n")