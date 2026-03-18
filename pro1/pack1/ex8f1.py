# function : 여러 개의 수행문을 하나의 이름으로 묶음 실행단위
# 함수 고유의 실행 공간을 갖음
# 자원의 재활용

# 내장 함수 일부 체험
print(sum([1,2,3]))
print(bin(8))
print(eval('4 + 5'))   # 문자 연산
print(round(1.2), round(1.6))  # 반올림
import math
print(math.ceil(1.2), ' ', math.ceil(1.2))
print(math.floor(1.2), ' ', math.floor(1.2))


b_list =  [True, 1, False]
print(all(b_list))    # 모두 참 -> True
print(any(b_list))    # 하나만 참이어도 -> True

data1 = [10, 20, 30]
data2 = ['a', 'b']
for i in zip(data1,data2):
    print(i)

# ...
