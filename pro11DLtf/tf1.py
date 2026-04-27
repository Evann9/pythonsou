import tensorflow as tf
import numpy as np

print(tf.__version__) # 2.21.0
print('즉시 실행 모드 : ', tf.executing_eagerly()) # 즉시 실행 모드 :  True
print('GPU 사용 가능 여부 : ', tf.config.list_physical_devices('GPU')) # GPU 사용 가능 여부 :  []

print('\nTensor : tensorflow에서 데이터를 담는 기본 자료 구조 (숫자 데이터 저장용 다차원 배열)')
# ndarray와 유사하지만 텐서플로에서 연산에 사용되도록 만들어진 객체

print(12, type(12))  # 파이썬 상수로 파이썬이 직접 계산
# 12 <class 'int'>

print(tf.constant(12))  # 0d tensor (scaler)
# tf.Tensor(12, shape=(), dtype=int32)

print(tf.constant([12])) # 1d tensor (vector)
# tf.Tensor([12], shape=(1,), dtype=int32)

print(tf.constant([[12]])) # 2d tensor (matrix)
# tf.Tensor([[12]], shape=(1, 1), dtype=int32)

print(tf.constant([[12,1]]))
# tf.Tensor([[12  1]], shape=(1, 2), dtype=int32)

print(tf.rank(tf.constant(12))) # 0
print(tf.rank(tf.constant([12]))) # 1
print(tf.rank(tf.constant([[12]]))) # 2
print(tf.rank(tf.constant([[[12]]]))) # 3

tf.print(tf.constant(12))  # 12
print('파이썬 기본 함수, 객체 자체를 문자열로 변환 후 출력, 정보 중심 출력')
tf.print('텐서플로 함수, 텐서 실제값을 중심으로 출력')

print()
imsi = np.array([1,2])  # 일반 수치 연산(CPU 연산이 기본, 자동 미분 불가, 값 변경 가능)
print(type(imsi))       # <class 'numpy.ndarray'>
imsi[0] = 10            # 값 변경 가능

a = tf.constant([1,2])  # 딥러닝 연산(GPU 연산 가능, 자동 미분 가능, 값 변경 불가능)
print(type(a))          # <class 'tensorflow.python.framework.ops.EagerTensor'>
# a[0] = 10             # TypeError: 'tensorflow.python.framework.ops.EagerTensor' object does not support item assignment
b = tf.constant([3,4])

c = a + b  # 텐서 요소값 더하기  (열단위 연산)
tf.print(c) # [4 6]
d = tf.constant([3])
e = c + d
tf.print(e) # [7 9] : Broadcast 연산

print('\npython과 tensorflow 형 변환')
print(7)
print(tf.convert_to_tensor(7))  # tf.Tensor(7, shape=(), dtype=int32)
print(tf.constant(7).numpy())   # 7
arr = np.array([1,2])  # ndarray type
# tf.add(), tf.sub(). tf.multiply(), tf.divide() 가능
tfarr = tf.add(arr, 5) # tensor 연산을 하면 tensor type으로 자동 형태 변환
print(tfarr) # tf.Tensor([6 7], shape=(2,), dtype=int64)
print(np.add(tfarr, 5)) # [11 12]  tensor -> ndarray

print('\ntensorflow 변수 선언 후 사용')
# tf.Variable() : tensorflow에서 값이 바뀔 수 있는 tensor를 만들때 사용
# ex) weight, bias ...
v1 = tf.Variable(1.0)
tf.print('v1 : ', v1)  # v1 :  1

v2 = tf.Variable(tf.zeros((2,))) # 0으로 채워진 변수
tf.print('v2 : ', v2)  # v2 :  [0 0]

v3 = tf.Variable(tf.ones((2,))) # 1로 채워진 변수
tf.print('v3 : ', v3)  # v3 :  [1 1]
print()
# tensor 값 변경 - assign()
# v1 =123   # AttributeError: 'int' object has no attribute 'assign'
v1.assign(123)  # 변수값 변경
tf.print('v1 : ', v1)  # v1 :  123
v2.assign([30, 40])
tf.print('v2 : ', v2)  # v2 :  [30, 40]
print()
aa = tf.Variable(tf.zeros((2,1)))  # 2행 1열에 모두 1을 기억
tf.print('aa : ', aa)  # [[0] [0]]
aa.assign(tf.ones((2,1)))  
tf.print('aa : ', aa)  # [[1] [1]]
aa.assign_add([[2],[3]]) # 더하기 치환
tf.print('aa : ', aa)  #  [[3] [4]]
aa.assign_sub([[1],[1]]) # 빼기 치환
tf.print('aa : ', aa)  # [[2] [3]]
aa.assign(aa * [[2],[3]]) # 곱하기 치환 assign_mul() : X
tf.print('aa : ', aa)  # [[4] [9]]
aa.assign(aa / [[2],[3]]) # 나누기 치환 assign_div() : X
tf.print('aa : ', aa)   # [[2] [3]]

print('난수 처리')
tf.print(tf.random.uniform([1], 0, 1))  # 균등분포 ([shape], min, max)
tf.print(tf.random.normal([3], mean=0, stddev=1))  # 정규분포 ([shape], avg, std)