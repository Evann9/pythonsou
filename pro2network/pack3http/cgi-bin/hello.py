ss = '파이썬 자료 출력'
# print(ss)  개발자가 자신의 컴 표준 출력장치로 값 확인
# ....
ss2 = 123 + 5

# 클라이언트 브라우저로 출력
print('Content-Type:text/html;charset=utf-8\n')
print("<html><body>")
print("<b>안녕. 파이썬 모듈로 작성한 문서야</b><br/>")
print("파이썬 변수 값1 : %s"%(ss, ))
print("<br/>파이썬 변수 값2 : %d"%(ss2, ))
print("</html></body>")
