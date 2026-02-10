# 반복문 for
#for i in [1,2,3,4,5]:
#for i in (1,2,3,4,5):
for i in {1,2,3,4,5}:   # 반복할 묶음형 자료만
    print(i, end = ' ')

print('분산/표준편차 ---')
# numbers = [1,3,5,7,9]      # 합은 25, 평균은 5.0
# numbers = [3,4,5,6,7]  # 합은 25, 평균은 5.0
numbers = [-3,4,5,7,12]      # 합은 25, 평균은 5.0
tot = 0
for a in numbers:
    tot += a
print(f'합은 {tot}, 평균은 {tot / len(numbers)}')
avg = tot / len(numbers)
# 편차의 합
hap = 0 
for i in numbers:
    hap += (i - avg) ** 2
print(f'편차 제곱의 합 {hap}')
vari = hap / len(numbers)
print(f'분산은 {vari}')
print(f'표준편차 {vari ** 0.5}')

print()
colors = ['r', 'g', 'b']
for v in colors:
    print(v, end = ' ')

print('iter() : 반복 가능한 객체를 하나씩 꺼낼 수 있는 상태로 만드는 함수')
iterator = iter(colors)
for v in iterator:
    print(v, end = ', ')

print()
for idx, d in enumerate(colors):          # enumerate: 인덱스와 값을 반환
    print(idx, ' ' , d)

print('\n사전형 ---')
datas = {'python':'만능언어', 'java': '웹용언어', 'mariadb':"RDBMS"}
for i in datas.items():      # tuple type
    #print(i)
    print(i[0], '~~', i[0])

for k, v in datas.items():
    print(k, '--', v)

print()
for key in datas.keys():
    print(k, end =' ')

for val in datas.keys():
    print(val, end =' ')

print('다중 for ---------')
for n in [2,3]:
    print('--{}단--'.format(n))
    for i in [1,2,3,4,5,6,7,8,9]:
        print('{} * {} = {}'.format(n, i, n * i))

print('continue, break ---------')
nums = [1,2,3,4,5]
for i in nums:
    if i == 2:continue
    #if i == 4:break
    print(i, end=' ')
else:
    print('정상종료')

print('\n정규표현식 + for')
str = '''청와대가 뉴미디어 분야를 대상으로 신규 출입기자 모집 공고를 냈다. 이재명 대통령은 정책에 대한 홍보가 중요하다고 강조해왔고, 투명성을 강조해온 이재명 정부는 청와대를 출입하는 유튜브 기반 매체를 늘리겠다고 한 바 있다. 청와대는 기존 신문·방송과 달리 '1인미디어'라고 불리는 매체들을 중심으로 '뉴미디어 풀'을 신설해 변화하는 미디어 환경에도 대응하겠다는 계획이다.
청와대는 2일 오전 청와대 홈페이지에 '신규 출입 뉴미디어 등록 공고'를 올려 출입 매체 확장에 나섰다. 미디어오늘 취재에 따르면 춘추관은 기존 출입매체와 별도로 '뉴미디어 풀'을 신설할 예정이다. 기존 신문·방송과 달리 이른바 '1인 미디어'로 불리면서 모바일, SNS 등을 통해 뉴스를 전하는 매체들을 기반으로 기존 매체들과 구분되는 새로운 카테고리를 만드는 것이다.
청와대 그리고 홈페이지에 올림 sbs'''

import re
str2 = re.sub(r'[^가-힣\s]','', str)     # 한글과 공백 이외의 문자는 공백처리 # 대괄호 안 ^: 부정
print(str2)
str3 = str2.split(' ')  # 공백을 기준으로 문자열 구분
print(str3)
cou = {}  
for i in str3:
    if i in cou:
        cou[i] += 1   # 같은 단어가 있으면 누적
    else:
        cou[i] = 1    # 최초 단어인 경우 '단어': 1

print(cou)

print('정규표현식 좀 더 연습')
for test_ss in ['111-1234', '일이삼-일이삼사', '222-1234', '333&1234']:
    if re.match(r'^\d{3}-\d{4}$', test_ss):   # 대괄호 밖 ^: 시작   $: 끝
        print(test_ss, '전화번호 맞아요')
    else:
        print(test_ss, '전화번호 아니야')

print('comperhension : 반복문 + 조건문 + 값 생성을 한 줄로 표현' )
a = [1,2,3,4,5,6,7,8,9,10]
li = []
for i in a:
    if i % 2 == 0:
        li.append(i)
print(li)
print(list(i for i in a if i % 2 == 0))

#datas = [1,2, 'a' ,True, 3.0]
datas = {1,2, 'a' ,True, 3.0, 2, 1, 2, 2, 2}           # {} : 중복 제거
li2 = [i * i for i in datas if type(i) == int]
print(li2)

id_name = {1:'tom', 2:'oscar'}
name_id = {val:key for key, val in id_name.items()}
print(name_id)
print()
print([1,2,3])
print(*[1,2,3])  #*: unpack 기능
aa = [(1,2), (3,4), (5,6)]
for a, b in aa:
    print(a + b)

print([a + b for a, b in aa])        # [3, 7, 11]
print(*[a + b for a, b in aa], sep='\n')

print('\n 수열 생성: range')
print(list(range(1,6)))      # [1, 2, 3, 4, 5]
#print(list(range(1,6,1)))
print(tuple(range(1,6,2)))   # (1, 3, 5)
print(list(range(-10,-100,-20))) #[-10, -30, -50, -70, -90]
print(set(range(1,6,2))) #{1, 3, 5}
print()
for i in range(6):
    print(i, end= ' ')      # 0 1 2 3 4 5

for _ in range(6):
    print('반복')

tot = 0
for i in range(1,11):
    tot += i
print('tot :',tot)
print('tot :', sum(range(1,11)))     # sum() : 내장함수

for i in range(1,10):
    print(f'2*{i} = {2 * i}')

print('\n')
# 문1 : 2~9 구구단 출력 (단은 행 단위 출력)
for n in range(2,10):
    for i in range(1,10):
        print('{} * {} = {}'.format(n, i, n * i), end= ' ')
    
print()
# 문2 : 주사위를 두 번 던져서 나온 숫자들의 합이 4의 배수가 되는 경우만 출력 
for i in range(1,7,1):
    for d in range(1,7,1):
        h = i + d
        if h % 4 == 0:
            print(i,d)



print('\nend')