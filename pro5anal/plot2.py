import matplotlib.pyplot as plt
import numpy as np

# 차트 영역(Figure & Axes) 객체 선언 시 인터페이스 유형 두가지

# 1) Matplotlib 스타일의 인터페이스
# 상태 기반 인터페이스로, 현재 활성화된 Figure나 Axes에 명령을 내리는 방식
x = np.arange(10)
plt.figure()          # 새로운 차트 윈도우(Figure) 생성
plt.subplot(2, 1, 1)  # 2행 1열 중 1번째 패널 선택 (row, column, panel number)
plt.plot(x, np.sin(x)) # 사인 그래프
plt.subplot(2, 1, 2)  # 2행 1열 중 2번째 패널 선택
plt.plot(x, np.cos(x)) # 코사인 그래프
plt.show()

# 2) 객체 지향 인터페이스
# Figure와 Axes 객체를 직접 생성하고 변수에 할당하여 제어하는 방식 (복잡한 레이아웃에 유리)
fig, ax = plt.subplots(nrows=2, ncols=1) # 한 번에 여러 개의 서브플롯 생성
ax[0].plot(x, np.sin(x)) # 첫 번째 축(Axes) 객체에 그리기
ax[1].plot(x, np.cos(x)) # 두 번째 축(Axes) 객체에 그리기
plt.show()


# 차트의 종류 일부 확인
fig = plt.figure() # 전체 차트 배경 생성
ax1 = fig.add_subplot(1, 2, 1) # 1행 2열의 첫 번째 영역 추가
ax2 = fig.add_subplot(1, 2, 2) # 1행 2열의 두 번째 영역 추가

# 히스토그램: 데이터의 분포를 막대 형태로 표현
ax1.hist(np.random.randn(1000), bins=100, alpha=0.9)   # bins: 구간 개수, alpha: 투명도
ax2.plot(np.random.randn(10)) # 일반 선 그래프
plt.show()

# 막대그래프(bar 차트)
data = [50, 80, 100, 90, 70]
plt.bar(range(len(data)), data) # 수직 막대 그래프
plt.show()

# 가로 막대그래프(horizontal bar 차트)
plt.barh(range(len(data)), data) # 수평 막대 그래프
plt.show()

# 오차 막대(Error Bar)가 포함된 막대 그래프
err = np.random.rand(len(data))
plt.barh(range(len(data)), data, alpha=0.5, xerr=err) # xerr: x축 방향 오차 표시
plt.show()

# 원형 차트(Pie Chart)
# 데이터의 비율을 시각화
plt.pie(data, colors=['yellow','blue','red'], 
        explode=(0, 0.2, 0, 0.1, 0))  # explode: 특정 조각을 밖으로 튀어나오게 설정
plt.title('Pie Chart')
plt.show()

# 박스 플롯(Box plot) : 전체 데이터의 분포를 확인하기에 적합. 또한 이상치 확인에 도움됨.
data = [1, 50, 80, 100, 90, 70, 300]
plt.boxplot(data)
plt.show()

# scatter (bubble chart) : 산점도 차트에 점의 크기를 동적으로 표시
n = 30
np.random.seed(0)
x = np.random.rand(n)
y = np.random.rand(n)
color = np.random.rand(n)
scale = np.pi * (np.random.rand(n) * 15) ** 2 # 점의 크기(scale) 계산
plt.scatter(x, y, c=color, s=scale) # c: 색상, s: 크기
plt.show()

# 시계열 데이터(Time Series)로 선 그래프
import pandas as pd
fdata = pd.DataFrame(np.random.randn(1000, 4), 
                    index=pd.date_range('1/1/2000', periods=1000),
                    columns=list('abcd'))
print(fdata.head(3))
print(fdata.tail(3))
fdata = fdata.cumsum() # 누적합 계산
print(fdata.head(3))
plt.plot(fdata)
plt.show()

# pandas의 plot 기능
fdata.plot() # DataFrame 객체에서 직접 plot 호출
fdata.plot(kind='bar') # kind 속성으로 차트 종류 변경 가능
plt.xlabel("time")
plt.ylabel("data")
plt.show()
