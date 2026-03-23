# css selecter를 이용
from bs4 import BeautifulSoup
html_page = """
<html>
<body>
<div id="hello">
    <a href="https://www.naver.com">naver</a>
    <span>
        <a href="https://www.daum.net">daum</a>
    </span><br>
    <ul class='world'>
        <li>안녕</li>
        <li>반가워</li>
    </ul>
</div>
<div id='hi' class='good'>
    두번째 div
</div>
</body>
</html>
"""
soup = BeautifulSoup(html_page, 'html.parser')
# aa = soup.select_one("div")
# aa = soup.select_one("div#hello")
aa = soup.select_one("div#hello > a")
print('aa : ', aa, ' ', aa.string)

print()
# bb = soup.select("div")
# bb = soup.select("div#hello > ul.world")
bb = soup.select("div#hello > ul.world > li")
print('bb : ', bb)
for i in bb:
    print(i, ' ', i.text)

print("--------위키 백과 사이트에서 이순신으로 검색된 자료 읽기--------" )
import requests
url = "https://ko.wikipedia.org/wiki/이순신"
header = {"User-Agent": "Mozilla/5.0"}
wiki = requests.get(url=url, headers=header)
# print(wiki.text[:100])

soup = BeautifulSoup(wiki.text, 'html.parser')
result = soup.select("#mw-content-text p")
# result = soup.select("p#mwHw")
# print(result)
for s in result:
    for sup in s.find_all('sup'):
        sup.decompose()   # 태그 삭제
    print(s.get_text(strip=True))


print("\n--------교촌치킨 사이트에서 메뉴,가격 자료 읽기--------")
import pandas as pd
url = "https://kyochon.com/menu/chicken.asp"
header = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=header)
# print(response.text)
soup2 = BeautifulSoup(response.text, 'html.parser')
# 메뉴명 얻기
# names = soup2.select("dl.txt > dt")
# print(names)
names = [tag.text.strip() for tag in soup2.select("dl.txt > dt")]
# print(names) 

prices = [int(tag.text.strip().replace(',','')) for tag in soup2.select("p.money strong")]
# print(prices)

df = pd.DataFrame({'상품명': names, '가격': prices})
print(df.head(3))
print(f"가격 평균 : {df['가격'].mean():.2f}")
print(f"가격 표준편차 : {df['가격'].std():.2f}")
print(f"가격 중앙값 : {df['가격'].median():.2f}")
cv = df['가격'].std() / df['가격'].mean() * 100
print(f'가격 변동계수(cv) : {cv:.2f}%')  # 28.31%
# 해석 : 가격 변동계수(cv) : 28.31%이므로 평균 대비 적당히 퍼져 있는 편