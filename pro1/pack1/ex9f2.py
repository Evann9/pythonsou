# 사용자 정의 함수
'''
def 함수명(가인수,,,)
    # ...
    return 반환값   # 1개만 반환, return이 없으면 return None

함수명(실인수,,,)    # 함수 호출
'''

def doFunc1():
    print('함수 주소는',doFunc1)
    print('함수 주소는',id(doFunc1))

def doFunc2(name):
    print('name: ', name)
    # return None

def doFunc3(arg1,arg2):
    re = arg1 + arg2
    return re

def doFunc4(a1,a2):
    imsi = a1 + a2
    if imsi % 2 == 1:
        return
    else:
        return imsi

doFunc1()           # 함수 수행
print(doFunc1)      # 주소 포함
imsi = doFunc1      # 주소 치환
imsi()
print(doFunc1())    # 함수 수행 + None

print('------')
# doFunc2(7)   # 파라미터를 통해 변수 지정
doFunc2('길동')
# doFunc2('길동', '순신')
doFunc3('대한','민국')
print(doFunc3('대한','민국'))
print(doFunc3(5,6))
result = doFunc3('5','6')
print(result)

print(doFunc4(3,4))
print(doFunc4(3,5))

print('---------')
def triArea(a,b):
    c = a * b / 2 
    triAreaPrint(c)      # 다른 함수 호출

def triAreaPrint(cc):
    print('삼각형의 면적은 ', cc)

triArea(20, 30)

print('---------')
def passResult(kor,eng):
    ss = kor + eng
    if ss >= 50:
        return True
    else:
        return False
if passResult(20,20):
    print('합격')
else:
    print('불합격')

print()
def swapFunc(a, b):
    return b, a     # return (b, a)

a = 10; b = 20
print(a, ' ', b)
print(swapFunc(a,b))

print()
def funcTest():
    print('funcTest 맴버 처리')
    def funcInner():
        print('내부 함수')
    funcInner()

funcTest()

# if 조건식 안에 함수 사용
def isOdd(para):
    return para % 2 == 1 # 홀수이면 True 반환

mydict = {x:x * x for x in range(11) if isOdd(x)}
print(mydict)

print('변수의 생존 범위 (scope rule)-------')
# 변수가 저장되는 이름공간은 변수가 어디서 선언되었는가에 따라 생존시간이 다름.
# 전역, 지역 변수
# Local > Enclosing function > Global > Built-in

player = '전국대표'     # 전역변수 (현재 모듈 어디서든 호출 가능)
name = '한국인'   

def funcSoccer():   # 함수 안에서 정의된 것들은 함수 안에서만 사용가능
    name = '홍길동'    
    # player = '지역대표' # 지역변수( 현재 함수 내에서만 호출 가능)
    city = '서울'
    print(f'이름은 {name} 수준은 {player}')
    print(f'지역은 {city}')

funcSoccer()
print(f'이름: {name} 수준: {player}')
# print(f'지역은 {city}') # 안됨..(함수 안에서만 가능)

#다시 설명#
print()
a = 10; b = 20; c = 30  # Global
def Foo():
    a = 7        # 지역 변수
    b = 100
    def Bar():
        global c   # Bar 함수의 멤버X 모듈의 멤버.(자주 사용)
        nonlocal b  # 잘 안씀
        b = 8    # 지역 변수 
        print(f'Bar 수행 후 a:{a}, b:{b}, c:{c}')
        c = 9
        b = 200
    Bar ()
    print(f'Foo 수행 후 a:{a}, b:{b}, c:{c}')

Foo()
print(f'함수 수행 후 a:{a}, b:{b}, c:{c}')  # 함수 안 변수 영향X

print()
g = 1
print('g: ' ,g)
def func():
    global g
    a = g
    g = 2  
    return a

print(func())
print('g: ' ,g)





