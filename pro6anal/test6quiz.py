# * 카이제곱 검정

# 카이제곱 문제1) 부모학력 수준이 자녀의 진학여부와 관련이 있는가?를 가설검정하시오
#   예제파일 : cleanDescriptive.csv
#   칼럼 중 level - 부모의 학력수준, pass - 자녀의 대학 진학여부
#   조건 :  level, pass에 대해 NA가 있는 행은 제외한다.
import pandas as pd
import scipy.stats as stats

df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/cleanDescriptive.csv")

data = df.dropna(subset=['level', 'pass'])

# 귀무(H0): 부모의 학력수준과 자녀의 대학 진학여부는 관련이 없다.
# 대립(H1): 부모의 학력수준과 자녀의 대학 진학여부는 관련이 있다.

ctab = pd.crosstab(index=data['level'], columns=data['pass'])
ctab.columns = ['미진학', '진학']
ctab.index = ['고졸', '대졸', '대학원졸']
print(ctab)

chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f"카이제곱 통계량: {chi2:.4f}")
print(f"p-value: {p:.7f}")
# [판정] p-value(0.2507057) > 0.05 이므로 대립가설 기각. 
# 부모의 학력수준과 자녀의 대학 진학여부는 관련이 없다.



# 카이제곱 문제2) 지금껏 A회사의 직급과 연봉은 관련이 없다. 
# 그렇다면 jikwon_jik과 jikwon_pay 간의 관련성 여부를 통계적으로 가설검정하시오.
#   예제파일 : MariaDB의 jikwon table 
#   jikwon_jik   (이사:1, 부장:2, 과장:3, 대리:4, 사원:5)
#   jikwon_pay (1000 ~2999 :1, 3000 ~4999 :2, 5000 ~6999 :3, 7000 ~ :4)
#   조건 : NA가 있는 행은 제외한다.

import pymysql
import pandas as pd
import scipy.stats as stats
import csv

# 1. 데이터베이스 접속 설정
config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8'
}

try:
    # 2. DB 연결 및 데이터 로드
    conn = pymysql.connect(**config)
    sql = "SELECT jikwonjik, jikwonpay FROM jikwon"
    
    # pandas의 read_sql을 사용하여 직접 DataFrame으로 읽기
    df = pd.read_sql(sql, conn)
    df.columns = ['직급', '연봉']

    # 3. 데이터 전처리 (결측치 제거)
    df = df.dropna(subset=['직급', '연봉'])

    # 4. 직급 넘버링 (Mapping)
    # 문제 조건: 이사:1, 부장:2, 과장:3, 대리:4, 사원:5
    jik_map = {'이사': 1, '부장': 2, '과장': 3, '대리': 4, '사원': 5}
    df['직급_번호'] = df['직급'].map(jik_map)

    # 5. 연봉 범주화 (Binning)
    # 조건: 1000~2999:1, 3000~4999:2, 5000~6999:3, 7000~:4
    bins = [1000, 3000, 5000, 7000, 100000]
    labels = ['1', '2', '3', '4']
    df['연봉_범주'] = pd.cut(df['연봉'], bins=bins, labels=labels, right=False)

    # 6. 넘버링 정보가 포함된 CSV 파일 저장
    df.to_csv('testquiz.csv', index=False, encoding='utf-8-sig')
    print("파일 저장 완료: testquiz.csv (직급_번호 포함)")

    # 7. 가설 검정 준비 (교차표 생성)
    
    # 귀무(H0): 직급과 연봉은 관련이 없다.
    # 대립(H1): 직급과 연봉은 관련이 있다.

    # 1. 직급 번호를 이름으로 미리 매핑
    df['직급_라벨'] = df['직급_번호'].map({
        1: '1.이사', 2: '2.부장', 3: '3.과장', 4: '4.대리', 5: '5.사원'
    })

    # 2. 교차표 생성 (라벨링된 컬럼 사용)
    ctab = pd.crosstab(index=df['직급_라벨'], columns=df['연봉_범주'])

    # 3. 컬럼명도 직관적으로 변경
    ctab.columns = ['1단계(1000-)', '2단계(3000-)', '3단계(5000-)', '4단계(7000-)']

    print(ctab)

    # 8. 카이제곱 검정 실행
    chi2, p, dof, expected = stats.chi2_contingency(ctab)
    
    print("-" * 40)
    print(f"카이제곱 통계량 : {chi2:.4f}")
    print(f"p-value : {p:.7f}")
    print(f"자유도 : {dof}")
    print("-" * 40)

    # 9. 최종 판정
    if p < 0.05:
        print("결과: p < 0.05 이므로 귀무가설 기각.")
        print("=> [결론] 직급과 연봉은 통계적으로 유의미한 관련성이 있습니다.")
    else:
        print("결과: p >= 0.05 이므로 귀무가설 채택.")
        print("=> [결론] 직급과 연봉은 관련이 없습니다.")

except Exception as e:
    print(f"처리 중 오류 발생: {e}")
finally:
    if 'conn' in locals():
        conn.close()