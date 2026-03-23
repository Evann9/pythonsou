import requests
import pandas as pd
from bs4 import BeautifulSoup

# 크롤링할 페이지 URL 리스트 (네이버 증권 시가총액 상위 종목)
urls = [
    "https://finance.naver.com/sise/sise_market_sum.naver?&page=1",
    "https://finance.naver.com/sise/sise_market_sum.naver?&page=2"
]

# HTTP 요청 시 브라우저로 인식시키기 위한 헤더 설정
headers = {"User-Agent": "Mozilla/5.0"}
file_name = "market_cap.csv"

# CSV 파일 생성 및 데이터 쓰기
with open(file_name, mode='w', encoding='utf-8') as f:
    f.write("종목명,시가총액\n") # 헤더 작성
    
    for url in urls:
        res = requests.get(url=url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # 테이블 내의 각 행(tr) 선택
        rows = soup.select("table.type_2 > tbody > tr")
        for row in rows:
            # 종목명이 없는 빈 행(구분선 등)은 건너뜀
            if not row.select_one("a.tltle"): continue

            # 종목명 추출
            name = row.select_one("a.tltle").get_text(strip=True)
            # 시가총액 추출 (콤마 제거 후 숫자 데이터로 준비)
            price = row.select(".number")[4].get_text(strip=True).replace(',', '')
            
            f.write(f"{name},{price}\n")

# 저장된 CSV 파일을 pandas DataFrame으로 읽기
df = pd.read_csv(file_name)
df['시가총액'] = pd.to_numeric(df['시가총액']) # 문자열을 숫자 타입으로 변환
df.index = df.index + 1 # 인덱스를 1부터 시작하도록 조정
print(df[['종목명', '시가총액']].head(5)) # 상위 5개 데이터 출력