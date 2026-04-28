# 연산자와 기초함수
import tensorflow as tf
import numpy as np

x = tf.constant(7)
y = tf.constant(3)

# cond() : 삼항연산, 산술연산
result1 = tf.cond(x > y, lambda:tf.add(x, y), lambda:tf.subtract(x, y))
tf.print(result1)  # 10

# case() : 조건 연산
f1 = lambda: tf.constant(1)  # lambda에 의해 1을 반환
f2 = lambda: tf.constant(tf.multiply(2,3))
result2 = tf.case([(tf.less(x, y), f1)], default=f2) # 다중 조건 처리
tf.print(result2)  # 6

print('관계연산')
print(tf.equal(1,2)) # False (같은지 비교)
print(tf.not_equal(1,2)) # True (다른지 비교)
print(tf.less(1,2)) # True (작은지 비교)
print(tf.greater(1,2)) # False (큰지 비교)
print(tf.greater_equal(1,2)) # False (크거나 같은지 비교)

print('논리연산')
print(tf.logical_and(True, False)) # False (논리곱)
print(tf.logical_or(True, False)) # True (논리합)
print(tf.logical_not(True)) # False (논리부정)

print('유일 합집합')
kbs = tf.constant([1,2,2,3,2])
val, idx = tf.unique(kbs)  # 유일 값과 인덱스 반환 
tf.print(val) # [1 2 3]
tf.print(idx) # [0 1 1 2 1]

print('reduce() 함수')
ar = [[1.,2.],[3.,4.]]
print(tf.reduce_mean(ar).numpy()) # 평균 : 차원축소
print(tf.reduce_mean(ar, axis=0).numpy()) # 열 기준
print(tf.reduce_mean(ar, axis=1).numpy()) # 행 기준
print(tf.reduce_max(ar).numpy()) # 최대값

print('reshape 함수')
t = np.array([[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]])
print(t.shape) # (2, 2, 3)
print(tf.reshape(t, shape=[12])) # 1차원 벡터로 변환
print(tf.reshape(t, shape=[2, 6])) # 2행 6열로 변환
print(tf.reshape(t, shape=[-1, 6])) # 행 개수 자동 결정
print(tf.reshape(t, shape=[2, -1])) # 열 개수 자동 결정

print('squeeze 함수')
print(tf.squeeze(t)) # 차원 축소 (크기가 1인 차원 제거)
t2 = np.array([[[0], [3], [6], [9]]])
tf.print(tf.squeeze(t2))  # [0 3 6 9]

print('expand_dims 함수')
tarr = tf.constant([[1,2,3],[4,5,6]])
print(tarr.shape) # (2, 3)
sbs = tf.expand_dims(tarr, 0) # 첫번째 차원을 추가해 확장
# axis=0 위치에 새 차원 추가. shape: (2,3) -> (1,2,3)
print(sbs.numpy())
sbs = tf.expand_dims(tarr, 1) # 두번째 차원을 추가해 확장
# axis=1 위치에 새 차원 추가  shape: (2,3) -> (2,1,3)
print(sbs.numpy())
sbs = tf.expand_dims(tarr, 2) # 세번째 차원을 추가해 확장
# axis=2 위치에 새 차원 추가 shape: (2,3) -> (2,3,1)
print(sbs.numpy())
sbs = tf.expand_dims(tarr, -1) # 마지막 차원을 추가해 확장
# axis=-1 마지막 위치에 새 차원 추가 shape: (2,3) -> (2,3,1)
print(sbs.numpy())
# ex) 이미지 처리에서 (height, width) 현태의 이미지를 (height, width)

print('cast 함수 : 자료형 변환')
num = tf.constant([1,2,3])
num2 = tf.cast(num, dtype=tf.float32)
print(num2, num2.dtype)