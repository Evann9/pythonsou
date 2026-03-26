# Flask, Pandas, PyMySQL을 활용한 데이터베이스 연동 및 데이터 분석 웹 애플리케이션
from flask import Flask, render_template, request
import pymysql
import pandas as pd
import numpy as np
from markupsafe import escape

app = Flask(__name__)

# MariaDB 연결 설정 정보
db_config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': '123',
    'database': 'test',
    'port': 3306,
    'charset': 'utf8mb4'
}

# 데이터베이스 연결 객체 생성을 위한 함수
def get_connection():
    return pymysql.connect(**db_config)

@app.route('/')
def index():
    # 메인 페이지(검색 폼이 있는 index.html) 렌더링
    return render_template('index.html')

@app.route('/dbshow')
def dbshow():
    # 클라이언트로부터 전달받은 부서명 검색어 가져오기
    dept = request.args.get('dept',"").strip()

    # 직원(jikwon)과 부서(buser) 테이블 조인을 위한 기본 SQL 쿼리
    sql = """
        select j.jikwonno as 직원번호, j.jikwonname as 직원명, b.busername as 부서명,
        b.busertel as 부서전화, j.jikwonpay as 연봉, j.jikwonjik as 직급, j.jikwongen as 성별
        from jikwon j
        inner join buser b on j.busernum = b.buserno
    """
    
    params = []
    if dept:
        # 부서명 검색 조건이 있는 경우 WHERE 절 추가
        sql += " where b.busername like %s"
        params.append(f"%{dept}%")

    # 직원번호 기준 오름차순 정렬
    sql += " order by j.jikwonno asc"    

    # DB 연결 및 데이터 조회 실행
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()
            cols = [c[0] for c in cur.description]  # 결과 셋의 컬럼명 추출

    # 조회된 데이터를 Pandas DataFrame으로 변환
    df = pd.DataFrame(rows, columns=cols)

    # 1) 직원 목록 데이터 처리: 특정 컬럼만 선택하여 HTML 테이블로 변환
    if not df.empty:
        jikwondata = df[['직원번호', '직원명', '부서명', '부서전화', '연봉']].to_html(index=False)
    else:
        jikwondata = '직원 정보가 없어요'

    # 2) 직급별 연봉 통계 분석 (Pandas GroupBy 활용)
    if not df.empty:
        stats_df = (
            df.groupby('직급')['연봉']
            .agg(
                평균 = "mean", 
                표준편차= lambda x:x.std(ddof=0),
                인원수 = 'count'
            )
            .round(2)
            .reset_index()
            .sort_values('평균', ascending=False)
        )
        stats_df['표준편차'] = stats_df['표준편차'].fillna(0) # 데이터가 1개일 경우 NaN 방지
        statsdata = stats_df.to_html(index=False)

    else:
        statsdata = '직급별 연봉 통계가 없어요'

    # 결과 데이터를 템플릿(dbshow.html)으로 전달
    return render_template('dbshow.html', 
                            dept=escape(dept),    # xss 방지 
                            jikwondata=jikwondata,
                            statsdata=statsdata)


if __name__ == '__main__':
    app.run(debug=True)
