# 조건 판단문 if 
var = 5

if var >=3:
    print('크네')
    print('흠 느낌')

if var >=3:
    print('크구나')
else:
    print('작구나')

print('end')

print()
money = 200
age = 35
if money >= 500:
    item = '사과'
    if age <= 30:
        msg = "참 참"
    else:
        msg = '참 거짓'
else:
    item = '한라봉'
    if age >= 20:
        msg = "거짓 참"
    else:
        msg = '거짓 거짓'

print(f'중복 if 수행후 결과 {item} {msg}')

print()
# data = input('점수:')   #입력 값은 모두 문자열 타입
# jumsu = int(data)
jumsu = 77
if jumsu >= 90:
    print('우수')
elif jumsu >= 80:
    print('보통')
else:
    print('저조')


jum = 80
if 90 <= jum <= 100:
    print("A")
elif 90 <= jum < 90:
    print('B')
else:
    print('C')


print('------------')
names = ['홍길동', '신선해', '이기자']
if '홍길동' in names:
    print('친구이름이야')
else:
    print("누구야?")


if (count :=len(names)) >= 3:  # := 대입 표현식
    print(f'인원수가 {count}명이므로 단체할인 적용')
else:
    print('ㅠㅠ')

scores = [95, 88, 76, 92, 81]
if (avg := sum(scores) / len(scores)) >= 80:
    print(f'우수반 : 평균점수 {avg}')

print('삼항 연산')
a = 'kbs'
b = 9 if a == 'kbs' else 11
print('b : ', b)
a= 11 
b= 'mbc' if a == 9 else 'kbs'
print('b : ', b)
a = 3
if  a < 5:
    print(0)
elif a < 10:
    print(1)
else:
    print(2)


print(0 if a < 5 else 1 if a < 10 else 2)

print('end')





