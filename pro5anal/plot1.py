# matplotlib : 플로팅 라이브러리.   그래프 생성을 위한 다양한 함수를 제공
# 시각화의 중요성

import numpy as np
import matplotlib.pyplot as plt
plt.rc('font', family='Malgun Gothic')  # 한글 깨짐 방지를 위한 폰트 설정
plt.rcParams['axes.unicode_minus'] = False

# x = ["서울","인천","수원"]    # [0, 1, 2]
x = ("서울","인천","수원")
# x = {"서울","인천","수원"}   # TypeError: unhashable type: 'set'
y = [5, 3, 7]
plt.xlim([-1,3])
plt.ylim([0,10])
# tick 설정 : y축의 라벨을 인위적으로 표시
plt.yticks(list(range(0,11,3)))
plt.plot(x,y)
plt.show()

data = np.arange(1,11,2)
plt.plot(data)  
x = [0,1,2,3,4]
for a, b in zip(x, data):
    plt.text(a, b, str(b))
plt.show()  # y축의 값만 주게 되면 x축의 값을 자동으로 생성됨

x = np.arange(10)
y = np.sin(x)
# print(x,y)
# plt.plot(x,y)
# plt.plot(x,y, 'bo')
plt.plot(x,y, 'go--', linewidth=2, markersize=12)
plt.show()

# hold : 복수의 plot으로 여러개의 차트를 겹쳐 그림
x = np.arange(0,np.pi * 3, 0.1)
y_sin = np.sin(x)
y_cos = np.cos(x)
plt.figure(figsize=(10,5))  # 그래프 전체 크기(w, h)
plt.plot(x, y_sin, 'r')  # 선
plt.scatter(x, y_cos)  # 산점도
plt.xlabel('x 축')  # x축 라벨
plt.ylabel('y 축')  # y축 라벨
plt.title('sine & cosine')  # 그래프 제목
plt.legend(['sine', 'cosine'])  # 범례
plt.show()

print()
# subplot: 하나의 Figure를 여러개의 Axes(plot)으로 나누기
plt.subplot(2, 1, 1) # 2행 1열 1행
plt.plot(x, y_sin)
plt.title('sine')

plt.subplot(2, 1, 2) # 2행 1열 2행
plt.plot(x, y_cos)
plt.title('cosine')
plt.show()

print()
irum = ['a', 'b', 'c', 'd', 'e']
kor = [80, 50, 70, 70, 90]
eng = [60, 70, 80, 90, 100]
plt.plot(irum, kor, 'ro-')
plt.plot(irum, eng, 'bo--')
plt.ylim([50, 100])
plt.title('시험 점수')
plt.legend(['국어', '영어'], loc=4)   # loc = 'best' : 자동으로 범례 위치 설정
plt.grid(True)

fig = plt.gcf()
plt.show()
fig.savefig('plot1.png')

from matplotlib.pyplot import imread
img = imread('plot1.png')
plt.imshow(img)
plt.show()