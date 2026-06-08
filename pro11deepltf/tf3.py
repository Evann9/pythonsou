# 연산자와 기초함수
import tensorflow as tf
import numpy as np

x = tf.constant(7)
y = tf.constant(3)

# cond() : 삼항연산
result1 = tf.cond(x > y, lambda:tf.add(x, y), lambda:tf.subtract(x, y))
print(result1)   # tf.Tensor(10, shape=(), dtype=int32)

# case() 조건 연산
f1 = lambda:tf.constant(1)  # lambda에 의해 1을 반한
f2 = lambda:tf.constant(tf.multiply(2, 3))
result2 = tf.case([(tf.less(x, y), f1)], default=f2)    # if(x < y) return 1 else return 0
print(result2)

print('관계연산 ---')
print(tf.equal(1, 2))
print(tf.not_equal(1, 2))
print(tf.less(1, 2))
print(tf.greater(1, 2))
print(tf.greater_equal(1, 2))

print('논리 연산 ---')
print(tf.logical_and(True, False))
print(tf.logical_or(True, False))
print(tf.logical_not(True))

print('유일 합집합 ---')
kbs = tf.constant([1, 2, 2, 3, 2])
val, idx = tf.unique(kbs)   # 유일값과 인덱스 반환
print('val : ', val)    # tf.Tensor([1 2 3], shape=(3,), dtype=int32)
print('idx : ', idx)    # tf.Tensor([0 1 1 2 1], shape=(5,), dtype=int32)

print('reduce ~ 함수 ---')
ar = [[1., 2.], [3., 4.]]
print(tf.reduce_mean(ar).numpy())     # 2.5 평균:차원축소
print(tf.reduce_mean(ar, axis=0).numpy())     # [2. 3.] 열 기준
print(tf.reduce_mean(ar, axis=1).numpy())     # [1.5 3.5] 행 기준
print(tf.reduce_max(ar).numpy())        # 4.0

print('reshape 함수 ---')
t = np.array([[[0, 1, 2], [3, 4, 5], [6, 7, 8], [9, 10, 11]]])
print(t.shape)
print(tf.reshape(t, shape=[12]))        # [ 0 1 2 3 4 ... shape(12,)]
print(tf.reshape(t, shape=[2, 6]))      # [[ 0 1 2 ... shape=(2, 6)]]
print(tf.reshape(t, shape=[-1, 6]))     # 행 갯수 자동 결정
print(tf.reshape(t, shape=[2, -1]))     # 열 갯수 자동 결정

print('squeeze 함수 ---')
print(tf.squeeze(t))    # 차원 축소(열 요소가 1인 배열의 경우)
t2 = np.array([[[0],[3],[6],[9]]])
print(t2.shape) # (1, 4, 1)
print(tf.squeeze(t2))   # tf.Tensor([0 3 6 9], shape(4,), dtype=int64)

print('expand_dims 함수 : 차원 확대 ---')
tarr = tf.constant([[1, 2, 3], [4, 5, 6]])
print(tarr.shape)   # (2, 3) : 2행 3열, 2차원 Tensor

sbs = tf.expand_dims(tarr, 0)
# axis=0 위치에 새 차원 추가. shape: (2, 3) -> (1, 2, 3)
print(sbs.numpy())  # [[[1 2 3][4 5 6]]

sbs = tf.expand_dims(tarr, 1)
# axis=1 위치에 새 차원 추가. shape: (2, 3) -> (2, 1, 3)
print(sbs.numpy())  # [[[1 2 3]] [[4 5 6]]]

sbs = tf.expand_dims(tarr, 2)   # 세번째 차원을 추가해 확장
# axis=2 위치에 새 차원 추가. shape: (2, 3) -> (2, 3, 1)
print(sbs.numpy())  # [[[1][2][3]] [[4][5][6]]]

sbs = tf.expand_dims(tarr, -1)
# axis=-1은 마지막 위치에 새 차원 추가
# 현재 2차원 Tensor에서는 axis=2와 같은 결과, shape: (2, 3) -> (2, 3, 1)
print(sbs.numpy())  # [[[1][2][3]] [[4][5][6]]]
# 예:이미지 처리에서 (height,width) 형태의 이미지를 (height,width,1)처럼 바꿀 때 사용.

print('cast 함수 : 자료형 변환---')
num = tf.constant([1, 2, 3])    # int type
num2 = tf.cast(num, tf.float32)
print(num2, num2.dtype) # tf.Tensor([1. 2. 3.], shape=(3,), dtype=float32) <dtype: 'float32'>

