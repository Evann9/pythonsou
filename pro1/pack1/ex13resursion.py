# 재귀함수 : 함수가 자기 자신을 호출 - 반복 처리
def countDown(n):
    if n == 0:
        print('완료')
        # return 
    else:
        print(n,end=' ')
        countDown(n - 1)   # 재귀
countDown(5)

print('--1 부터 n 까지 합--------')
def totFunc(n):
    if n == 0:
        print('탈출')
        return 1
    return n + totFunc(n - 1) # 재귀

result = totFunc(5)
print('result:', result)

print('--5 factorial(계승)--------')
def factFunc(a):
    if a == 1: return 1
    print(a)
    return a * factFunc(a - 1)

result2 = factFunc(5)
print('result2:', result2)

print('end')