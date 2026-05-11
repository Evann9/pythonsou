
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt

# tf23mnist.py에서 저장한 모델로 직접 만든 숫자 이미지(num.png)를 예측한다.
# 중요한 점은 학습 때와 완전히 같은 전처리(28x28, 흑백, 784개 입력, 0~1 정규화)를 적용하는 것이다.

im = Image.open('num.png')
img = np.array(im.resize((28, 28), Image.Resampling.LANCZOS).convert('L'))
# L 모드 : 흑백 이미지 픽셀값이 0 ~ 255 범위(0:검정, 255:흰색)
print(img.shape)    # (28, 28)

plt.imshow(img, cmap='Greys')
plt.show()

data = img.reshape([1, 784]).astype('float32') # 모델 입력 shape: (샘플 수, 784)
data /= 255.0

import tensorflow as tf
# 저장된 Keras 모델 구조와 가중치를 함께 불러온다.
mymodel = tf.keras.models.load_model('tf23model.keras')
new_pred = mymodel.predict(data, verbose=0)
print('new_pred : ', new_pred)
# softmax 확률 중 가장 큰 index가 예측한 숫자이다.
print('예측값 : ', np.argmax(new_pred, axis=1)[0])
# 예측값 :  4

