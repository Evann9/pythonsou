# tf.constant(), tf.Variable(), autograph 기능
import tensorflow as tf
import numpy as np

node1 = tf.constant(3, dtype=tf.float32)
node2 = tf.constant(4.0)
print(node1)
print(node2)
adddata = tf.add(node1, node2)
print(adddata)
print()
node3 = tf.Variable(3, dtype=tf.float32)
node4 = tf.Variable(4.0)
print(node3) # <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=3.0>
print(node4) # <tf.Variable 'Variable:0' shape=() dtype=float32, numpy=4.0>

adddata2 = tf.add(node3, node4)  # 텐서 더하기 연산
print(adddata2) # tf.Tensor(7.0, shape=(), dtype=float32)

node4.assign_add(node3)  # 변수값에 더한 후 치환
print(node4) # tf.Variable(7.0, dtype=float32, name='Variable')

print()
a = tf.constant(5)
b = tf.constant(10)
# 조건처리(tf.cond(조건, 함수1, 함수2))
result = tf.cond(a < b, lambda:tf.add(10, a), lambda:tf.square(a))
# result = tf.cond(a < b, tf.add(10, a), tf.square(a)) # TypeError: 'true_fn' must be callable.
print(result) # tf.Tensor(15, shape=(), dtype=int32)

# autograph 기능 : 파이썬 코드를 tensorflow 그래프 코드로 자동변환
# tensorflow의 두가지 실행 방법
# 1) Eager Execution : 파이썬 코드처럼 즉시 실행(기본)
# 2) Grape Execution : 별도 운영이 가능한 계산 그래프를 만들어 최적화 후 실행(텐서 처리)

@tf.function   # AutoGraph가 개입 (tensorflow 그래프 연산)
def calcFunc1(a,b):  # 위 tf. cond()를 autograph를 사용한 경우
    if a < b:
        return tf.add(10, a)
    else:
        return tf.square(a)
    
result2 = calcFunc1(a,b)
print(result2) # tf.Tensor(15, shape=(), dtype=int32)

# 참고 : 
# @tf.function 안에서 if, for, while, break, continue, return 등을 사용하면 AutoGraph가 실행

print()
# 반복문 처리
@tf.function
def calcFunc2(n):
    hap = tf.constant(0)
    for i in tf.range(n + 1):
        hap += i
    return hap

print(calcFunc2(10)) # 55

print('\n 1부터 3까지 출력')
imsi = tf.constant(0)
su = tf.Variable(1)  # tf 변수는 @tf.function 밖에 선언

@tf.function
def calcFunc3():
    # imsi = tf.constant(0)
    global imsi  # imsi가 local이 아님을 알림

    # su = tf.Variable(1) # AutoGraph에서 구조가 고정적이여야 함. -> ValueError

    for _ in range(3):
        # imsi = imsi + su # 파이썬 연산자
        imsi = tf.add(imsi, su) # 텐서 연산자(권장)
    return imsi
print('imsi : ', calcFunc3()) # 3


print('\n 구구단 3단 출력')
@tf.function
def calcFunc4(dan):
    for i in range(1, 10):
        result = tf.multiply(dan, i)
        tf.print(dan, 'x', i, '=', result)

calcFunc4(3)


