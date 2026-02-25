import socket
import sys

# HOST = '127.0.0.1'
HOST = ''
PORT = 7788

serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    serversock.bind((HOST,PORT))
    serversock.listen(5)
    print('서버(무한 루핑) 서비스 중...')

    while True:
        conn,addr = serversock.accept()
        print('client info : ', addr[0], ' ' , addr[1])
        print(conn.recv(1024).decode())   # 수신 메세지 출력   # .decode()  : 코드 해체
        # 메세지 송신 to client 
        conn.send(('from server : ' + str(addr[1]) + ' 너도 잘 지내라').encode('utf_8'))

except Exception as err:
    print('err : ', err)
    sys.exit()
finally:
    conn.close()
    serversock.close()


