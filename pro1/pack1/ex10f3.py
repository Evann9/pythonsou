# 매개변수 유형
# 위치 매개변수 : 인수와 순서대로 대응
# 기본값 매개변수 : 매개변수에 입력값이 없으면 기본값 사용
# 키워드 매개변수 : 실인수와 가인수 간 동일 이름으로 대응
# 가변 매개변수 : 인수의 갯수가 동적인 경우

def showGugu(start, end=5):
    for dan in range(start, end + 1, 1):
        print(str(dan) + '단 출력')
        for i in range(1,10):
            print(str(dan) + ' * ' + \
                  str(i) + ' = ' + str(dan * i), end= ' ')
        print()

showGugu(2,3)
print()
showGugu(2)
print()
showGugu(end = 9,start = 7) # 순서 바뀌어도 가능함(키워드 매개변수이기 때문)
print()
showGugu(7,end = 9)
# showGugu(start = 7, 9)  # SyntaxError: positional argument follows keyword argument
# showGugu(end = 9, 7)    # SyntaxError: positional argument follows keyword argument

print('가변 매개변수')
def func1(*ar):     # *변수 : 여러개의 인자를 tuple로 묶어서 받겠다는 의미(인자의 갯수를 잘 모를때 사용)
    print(ar)
    for i in ar:
        print('밥: ' + i)

func1('김밥','비빔밥','볶음밥')
func1('김밥','비빔밥','볶음밥','공기밥')
func1('김밥')  # ('김밥',) 이 모양으로 전달됨(tuple)
print()

#def func2(*a, ar):  # TypeError: func2() missing 1 required keyword-only argument: 'ar'(실행오류)
def func2(a, *ar):  
    print(a)
    print(ar)

func2('김밥','비빔밥')
func2('김밥','비빔밥','볶음밥','공기밥')

print()
def func3(w, h, **other):     # **변수 : dict로 받겠다
    print(f'몸무게 : {w}, 키 : {h}')
    print(f'기타 : {other}')

func3(80, 180, irum = '신기루', nai = 23)
# func3(80, 180, {'irum' : '신기루', 'nai' : 23})

print()
def func4(a, b, *c, **d):
    print(a,b)
    print(c)
    print(d)

func4(1,2)
func4(1,2,3,4,5)
func4(1,2,3,4,5, kbs = 9, mbc = 11)


print()
#type hint : 함수의 인자와 반환값에 type을 적어 가독성 향상
def typeFunc(num:int, data:list[str]) -> dict[str,int]:   # type hint은 구속력X
    print(num)
    print(data)
    result = {}
    for idx, item in enumerate(data, start = 1):
        print(f'idx:{idx}, item: {item}')
        result[item] = idx
    return result

rdata = typeFunc(1, ['일', '이', '삼'])
print(rdata)
print()
rdata = typeFunc('한개', [10,20,30])
print(rdata)