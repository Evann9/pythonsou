# 알고리즘 : 알고리즘은 특정 문제를 해결하기 위한 명확하고 단계적인 절차나 규칙의 집합입니다. 
# 입력값을 받아 유한한 시간 내에 정해진 논리적 순서에 따라 문제를 해결하고 결과물을 도출하는 과정으로, 
# 컴퓨터 프로그래밍 및 일상생활의 문제 해결(예: 요리법)에 모두 적용됩니다.

# 1 부터 n까지 연속한 숫자의 합을 구하는 알고리즘
def sum_n(n):
    s = 0
    for i in range(1, n+1):
        s = s + i
    return s

print(sum_n(10))
print(sum_n(100))

print('가우스의 합 공식으로 n까지의 합')
def sum_n2(n):
    return n * (n + 1) // 2

print(sum_n2(10))
print(sum_n2(100))

print("최대값 구하기 ---")

d = [17, 92, 33, 58, 7, 32, 42]

def find_max(a):
    n = len(a)
    max_v = a[0]
    for i in range(1, n):
        if a[i] > max_v:
            max_v = a[i]
    return max_v

print(find_max(d))

print("\n최대공약수 구하기 ---")
# 예) 4, 6  : 4와 6은 2로 모두 나누어 떨어지므로 2가 최대공약수가 된다.
    
def gcd(a,b):
    i = min(a,b)
    while True:
        if a % i == 0 and b % i == 0:
            return i
        i = i - 1

print(gcd(4,6))
print(gcd(24,16))
print(gcd(81,27))


print("\n최대공약수 구하기2 (유클리드 방식) --- ")
def gcd2(a,b):
    if b == 0:
        return a
    
    return gcd2(b, a % b)  # 조금 더 작은 값으로 재귀 호출

print(gcd(4,6))
print(gcd(24,16))
print(gcd(81,27))

