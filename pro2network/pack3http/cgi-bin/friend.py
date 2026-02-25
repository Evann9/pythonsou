import sys
sys.stdout.reconfigure(encoding='utf-8')

import os
import urllib.parse

""" --- get 요청 받을 때 ---------
# 웹 서버가 URL의 ? 뒤 부분을 환경변수 QUERY_STRING에 넣어줌
# 그 값을 가져오는 코드
query = os.environ.get("QUERY_STRING", "")
# 문자열을 딕셔너리 형태로 변환
params = urllib.parse.parse_qs(query)

# 값 꺼내기  - 첫 번째 값 꺼내기 [0]
irum = params.get("name", [""])[0] # 없으면 빈 리스트 대신 [""] 사용
junhwa = params.get("phone", [""])[0]
gen = params.get("gen", [""])[0]
---- """

# ---get / post 요청 받을 때 ---------
method = os.environ.get("REQUEST_METHOD", "GET")

if method == "POST":
    length = int(os.environ.get("CONTENT_LENGTH", 0))  # post일 떄
    body = sys.stdin.read(length)
else:
    body = os.environ.get("QUERY_STRING", "")   # get일 때

params = urllib.parse.parse_qs(body)

irum = params.get("name", [""])[0]
junhwa = params.get("phone", [""])[0]
gen = params.get("gen", [""])[0]

print("Content-Type: text/html; charset=utf-8")
print()
print("""
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>world</title>
</head> 
<body>
    입력한 값은 : 이름은 {0} 전화는 {1} 성별은 {2} 
</body>
</html>
""".format(irum, junhwa, gen))