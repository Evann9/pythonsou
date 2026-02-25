# Socket : 소켓은 프로세스가 네트워크 세계로 데이터를 내보내거나
# 혹은 그 세계로 부터 데이터를 받기 위한 실제적인 창구 역할을 한다.
# 그러므로 프로세스가 데이터를 보내거나 박기 위해서는 반드시 소켓을 열어서 
# 소켓에 데이터를 소켓으로부터 데이터를 읽어들여야 한다.
# socket이란 TCP/IP의 프로그래머 인터페이스
# 통신 기기간 대화가 가능하도록 하는 통신방식으로 클라이언트/서버 모델에 기초

# 연결지향 : TCP/IP
# 비연결지향 : UDP

# socket 통신 확인
import socket

print(socket.getservbyname('http','tcp'))  # www환경 전송규약
print(socket.getservbyname('ssh','tcp'))   # 원격 컴 접속
print(socket.getservbyname('ftp','tcp'))   # 파일 전송
print(socket.getservbyname('smtp','tcp'))  # 메일 송수신
print(socket.getservbyname('pop3','tcp'))  # 이메일
print()
# 특정 웹서버의 ipaddress 확인
print(socket.getaddrinfo('www.daum.net', 80, proto=socket.SOL_TCP))
print(socket.getaddrinfo('www.naver.com', 80, proto=socket.SOL_TCP))

