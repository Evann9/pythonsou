# 단순한 HTTPServer 구축 - 기본적인 socket 연결 관리

from http.server import SimpleHTTPRequestHandler, HTTPServer

PORT = 7777

handler = SimpleHTTPRequestHandler  # get 요청에 의해 문서를 읽어 클라이언트로 전송하는 역할

# HTTPServer 객체 생성
serv = HTTPServer(('192.168.0.27', PORT), handler)
print('웹 서비스 시작...')
serv.serve_forever()   # 웹 서비스 무한 루핑









