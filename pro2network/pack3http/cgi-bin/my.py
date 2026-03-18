import os
import urllib.parse

# 웹 서버가 URL의 ? 뒤 부분을 환경변수 QUERY_STRING에 넣어줌
# 그 값을 가져오는 코드
query = os.environ.get("QUERY_STRING", "")
# 문자열을 딕셔너리 형태로 변환
# {'name': ['홍길동'], 'age': ['20'] }
params = urllib.parse.parse_qs(query)

# 값 꺼내기  - 첫 번째 값 꺼내기 [0]
irum = params.get("name", [""])[0] # 없으면 빈 리스트 대신 [""] 사용
nai = params.get("age", [""])[0]

print("Content-Type: text/html; charset=utf-8")
print()
print("""
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>world</title>
</head> 
<body>
    넘겨 받은 값 : 이름은 {0}, 나이는 {1}
</body>
</html>
""".format(irum, nai))