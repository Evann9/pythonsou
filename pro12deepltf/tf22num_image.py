# MNIST는 60,000개의 훈련 이미지와 10,000개의 손글씨 숫자 테스트 이미지를 포함합니다.
# 데이터 세트는 28x28 픽셀 크기의 흑백 이미지로 표현합니다.
#
# 이 파일의 목적
# - 직접 준비한 숫자 이미지(num.png)를 MNIST 모델 입력 형식과 같게 전처리한다.
# - 이미지 크기, 색상 채널, 배열 shape, 픽셀 범위를 확인한다.

# 손글씨 이미지 읽기
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib

# PIL로 이미지 파일을 연 뒤, MNIST와 같은 28x28 흑백 이미지로 바꾼다.
im = Image.open('num.png')
img = np.array(im.resize((28, 28), Image.Resampling.LANCZOS).convert('L'))
# L 모드 : 흑백 이미지 픽셀값이 0 ~ 255 범위(0:검정, 255:흰색)
print(img.shape)    # (28, 28)

plt.imshow(img, cmap='Greys')
plt.show()

# Dense 기반 MNIST 모델은 28x28 이미지를 784개 숫자로 펼친 입력을 받는다.
data = img.reshape([1, 784]).astype('float32')
print(data, data.shape)

# 픽셀값 0~255를 0~1 범위로 맞춰 학습 데이터와 같은 스케일로 만든다.
data = data / 255.0
print(data)

# (1, 784)로 정규화됨 -> (28, 28) 구조를 바꾼 후 시각화
plt.imshow(data.reshape(28, 28), cmap='Greys')
plt.show()
