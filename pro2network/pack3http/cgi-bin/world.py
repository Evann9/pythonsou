s1 = '자료1'
s2 = '두번째 자료'

# 클라이언트 브라우저로 출력
print('Content-Type:text/html;charset=utf-8')

print('''
<html lang="kr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>world</title> 
</head>
<body>
    <h1>world 페이지</h1>
    자료 출력 : {0}, {1} 
    <br/>
    <img src ="../images/dog.jpeg" />
    <br/>
    <a href="../index.html">메인으로</a>
</body>
</html>
'''.format(s1,s2))