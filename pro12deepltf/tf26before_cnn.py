# 합성곱의 원리 이해 - 컵의 특징 추출
#
# 이 파일의 목적
# - CNN이 이미지를 한 번에 통째로 보지 않고, 작은 필터를 움직이며 지역 특징을 뽑는 원리를 확인한다.
# - 여기서는 3x3 필터를 직접 정의하고, 이미지 위를 이동시키며 원소별 곱의 합을 계산한다.

import matplotlib.pyplot as plt
from scipy.ndimage import correlate
import numpy as np
from skimage import data
from skimage.color import rgb2gray
from skimage.transform import resize

# 컵 이미지를 읽어와 (64, 64)로 리사이즈
# rgb2gray는 컬러 이미지를 흑백으로 바꾸고, resize는 계산을 쉽게 하려고 크기를 줄인다.
im = rgb2gray(data.coffee())
im = resize(im, (64, 64))
print(im.shape)     # (64, 64)

plt.axis('off')
plt.imshow(im, cmap='gray')
plt.show()

# 합성곱 필터 ( 3 * 3 )  # 실제 CNN에서는 이런 필터 값을 학습 과정에서 자동으로 찾아간다.
# filter = np.array([
#     [1, 1, 1],
#     [0, 0, 0],
#     [-1, -1, -1]
# ])
filter = np.array([
    [-1, 1, 1],
    [-1, 0, 0],
    [-1, 0, -1]
])

# padding : 상하좌우에 1 픽셀씩 0으로 채우기
new_image = np.zeros(im.shape)  # Feature Map: 필터를 적용한 결과 이미지
im_pad = np.pad(im, 1, mode='constant') # 0으로 채우기

# 합성곱(원소별 곱의 합) 연산(Convolution)을 수행
# 원래 이미지 im의 크기에 대해 모든 픽셀 좌표(i,j)를 훑는다.
# 각 위치 주변의 3x3 픽셀과 filter의 3x3 값을 곱한 뒤 모두 더해 new_image에 저장한다.
for i in range(1, im.shape[0]):    #  0 ~ 63 : 세로 방향
    for j in range(1, im.shape[1]):    #  0 ~ 63 : 가로 방향
        try:
            new_image[i, j] = im_pad[i-1, j-1] * filter[0, 0] + \
                                im_pad[i-1, j] * filter[0, 1] + \
                                im_pad[i-1, j+1] * filter[0, 2] + \
                                im_pad[i, j-1] * filter[1, 0] + \
                                im_pad[i, j] * filter[1, 1] + \
                                im_pad[i, j+1] * filter[1, 2] + \
                                im_pad[i+1, j-1] * filter[2, 0] + \
                                im_pad[i+1, j] * filter[2, 1] + \
                                im_pad[i+1, j+1] * filter[2, 2]
        except:
            # 가장자리 계산에서 인덱스가 범위를 벗어나면 해당 위치는 건너뛴다.
            pass

print(new_image.shape)
plt.axis('off')
plt.imshow(new_image, cmap='gray')
plt.show()
