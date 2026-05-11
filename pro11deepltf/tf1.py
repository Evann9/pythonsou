import tensorflow as tf
import numpy as np

print(tf.__version__)   # 2.21.0
print('즉시 실행 모드 : ', tf.executing_eagerly())  # True
print('GPU 사용 정보 확인 : ', tf.config.list_physical_devices('GPU'))  # [] GPU 없음

print('\nTensor : 텐서플로에서 데이터를 담는 기본 자료구조 (숫자 데이터 저장용 다차원 배열)')
# ndarray와 유사하지만 텐서플로에서 연산에 사용되도록 만들어진 객체

print(12, type(12))   # 12 <class 'int'> 파이썬 상수로 파이썬이 직접 계산
print(tf.constant(12))   # tf.Tensor(12, shape=(), dtype=int32) 0d 텐서 (scaler)
print(tf.constant([12]))   # tf.Tensor([12], shape=(1,), dtype=int32) 1d 텐서 (vector)
print(tf.constant([[12]]))   # tf.Tensor([[12]], shape=(1, 1), dtype=int32) 2d 텐서 (matrix)
print(tf.constant([[12, 1]]))   # tf.Tensor([[12  1]], shape=(1, 2), dtype=int32)
print(tf.rank(tf.constant([[12, 1]])))  # tf.Tensor(2, shape=(), dtype=int32)
tf.print(tf.constant(12))   # 12
print('파이썬 기본함수, 객체 자체를 문자열로 변환 후 출력, 정보 중심 출력')
tf.print('텐서플로 전용 출력함수, 텐서 실제값을 중심으로 출력')

print()
imsi = np.array([1, 2]) # 일반 수치 연산(CPU연산이 기본, 자동 미분 불가, 값변경 가능)
print(type(imsi))       # <class 'numpy.ndarray'>
imsi[0] = 10            # 값변경 가능

a = tf.constant([1, 2]) # 딥러닝 연산(GPU연산도 가능, 자동 미분 불가, 값변경 불가능)
print(type(a))          # <class 'tensorflow.python.framework.ops.EagerTensor'>
# a[0] = 10               # 값변경 불가능
b = tf.constant([3, 4])

c = a + b   # 텐서 요소값 더하기 (열단위 연산)
tf.print(c)     # [4 6]
d = tf.constant([3])
e = c + d
tf.print(e)     # [7 9] Broadcast 연산

print('\n넘파이와 텐서플로 형변환 가능')
print(7)
print(tf.convert_to_tensor(7))  # tf.Tensor(7, shape=(), dtype=int32)
print(tf.constant(7).numpy())   # 7

arr = np.array([1, 2])  # ndarray type
tfarr = tf.add(arr, 5)  # 텐서 연산을 하면 텐서 타입으로 자동 형변환됨
print(tfarr)    # tf.Tensor([6 7], shape=(2,), dtype=int64)
print(np.add(tfarr, 2)) # [8 9] 배열 연산을 하면 넘파이 타읍으로 자동 형변환 됨


print('\n텐서플로 변수 선언 후 사용하기 -------------------')
# tf.Variable()     - 텐서플로에서 값이 바뀔 수 있는 텐서를 만들 때 사용. 예) weight, bias ...
v1 = tf.Variable(1.0)   # 변수에 값 기억
tf.print('v1 : ', v1)   # 1
v2 = tf.Variable(tf.ones((2, )))    # 1으로 채워진 변수
tf.print('v2 : ', v2)   # [1 1]
v3 = tf.Variable(tf.zeros((2, )))   # 0으로 채워진 변수
tf.print('v3 : ', v3)   # [0 0]


# v1 = 123    # 에러 : 'int' object has no attribute 'assign'
v1.assign(123)  # 변수값 변경
tf.print('v1 : ', v1)   # 123
v2.assign([30, 40])
tf.print('v2 : ', v2)   # [30 40]
print()
aa = tf.Variable(tf.zeros((2, 1)))    # 2행 1열에 모두 1을 기억
tf.print('aa : ', aa)   # [[0][0]]
aa.assign(tf.ones((2, 1)))
tf.print('aa : ', aa)   # [[1][1]]


aa.assign_add([[2],[3]])    # 더하기 치환
tf.print('aa : ', aa)       # [[3][4]]
aa.assign_sub([[2],[3]])    # 빼기 치환
tf.print('aa : ', aa)       # [[1][1]]
aa.assign(aa * [[2],[3]])   # 곱하기 치환. assign_mul() X
tf.print('aa : ', aa)       # [[2][3]]
aa.assign(aa / [[2],[3]])   # 나누기 치환. assign_div() X
tf.print('aa : ', aa)       # [[1][1]]

print('난수 처리')
print(tf.random.uniform([1], 0, 1)) # 균등분포 ([shape], 최소, 최대)
print(tf.random.normal([3], 0, 1)) # 균등분포 ([shape], 평균, 표준편차)
print(tf.random.normal([3, 2], mean=0, stddev=1))












