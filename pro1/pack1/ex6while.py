a = 1
while a <= 5:
    print(a, end = ' ')
    a = a + 1
else:
    print('수행성공')

print()
i = 1
while i <=3:
    j = 1
    while j <= 4:
        print('i=' + str(i) + '/j=' +str(j))
        j = j + 1
    i = i + 1

print('1 ~ 100 사이의 정수 중ㅇ 3의 배수의 합 ---')
su = 1; hap = 0
while su <= 100:
    # print(su)
    if su % 3 == 0:
        #print(su)
        hap += su    #hap = hap + i
    su += 1
print('합은 ', hap)

print()
colors =['빨강', '파랑','노랑']
# num = 0
# print(colors[num])
# print(colors[1])
# print(colors[2])
num = 0
# while num < 3:
while num < len(colors):
    print(colors[num])
    num += 1

print('\n별찍기------')
i = 1
while i <= 10:
    j = 1
    msg=''
    while j <= i:
        msg += "*"
        j += 1
    print(msg)
    i += 1

"""
print('\if 블럭 내 while 블럭 사용 ----')
import time 
sw = input('폭탄 스위치를 누르까요?[y/n]')  # input이 문자로 인식 후 처리
# print("sw :", sw)
if sw == 'Y' or  sw == 'y':
    count = 5
    while 1 <= count:
        print('%d초 남았습니다'%count)
        time.sleep(1)   # 1초 후 다음 문장 실행
        count -= 1
    print('폭발')
elif sw == 'N' or sw == 'n':
    print('작업취소')
else:
    print('y 또는 n을 누르세요')
"""

print('\ncontinue/break ---')       #반복문에서만 사용
a = 0
while a < 10:
    a += 1 
    if a == 3:continue  # 아래 문을 무시하고 while로 이동
    if a == 5:
        continue        # 두 형식 모두 사용 가능
    # if a == 7:break     # while 문 무조건 탈출 (else도 패스)
    print(a)
else:
    print('정상 종료')

print('while 수행 후 %d' %a)

print('\n키보드로 숫자를 입력받아 홀수 짝수 확인하기(무한 반복----')
while True:       # True, 1, 100, -12, 4.5, 'ok' ...
    mysu = int(input('확인할 숫자 입력(예: 5):'))
    if mysu == 0:
        print('프로그램 종료')
        break
    elif mysu % 2 == 0:
        print("%d는 짝수"%mysu)
        continue
    elif mysu % 2 == 1:
        print("%d는 홀수"%mysu)



print('end')
