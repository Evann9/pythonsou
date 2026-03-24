"""
자전거 공유 시스템 분석 (Bike Sharing Demand)
Kaggle의 Washington D.C. Dataset을 활용한 시각화 및 탐색적 데이터 분석(EDA)

주요 컬럼 설명:
- datetime: 대여 날짜 및 시간
- season: 계절 (1:봄, 2:여름, 3:가을, 4:겨울)
- holiday: 공휴일 여부 (1:공휴일, 0:평일)
- workingday: 근무일 여부 (1:근무일, 0:휴일)
- weather: 날씨 (1:맑음, 2:안개, 3:가벼운 눈/비, 4:폭우/폭설)
- temp: 섭씨 온도 / atemp: 체감 온도
- humidity: 습도 / windspeed: 풍속
- casual: 비회원 대여량 / registered: 회원 대여량
- count: 총 대여량 (casual + registered)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 시각화 스타일 설정 (R의 ggplot 스타일 적용)
plt.style.use('ggplot')

# 한글 폰트 설정 (Windows: Malgun Gothic)
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# 데이터 로드 (parse_dates를 사용하여 datetime 컬럼을 날짜 형식으로 변환)
train = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv", parse_dates=['datetime'])

# EDA (Exploratory Data Analysis): 탐색적 데이터 분석
pd.set_option('display.width', None)  # 모든 컬럼 표시 옵션

print("--- 데이터 기본 정보 ---")
print(train.info())      # 데이터 구조 및 결측치 확인

print("\n--- 데이터 형태 ---")
print(train.shape)       # (10886 행, 12 열)

print("\n--- 상위 3개 데이터 ---")
print(train.head(3))

print("\n--- 온도(temp) 기술 통계량 ---")
print(train['temp'].describe())

print("\n--- 결측치 존재 여부 ---")
print(train.isnull().sum()) # 모든 컬럼에서 결측치(NaN) 개수 확인

# 년월일 시분초 별도 칼럼 추가 생성
train['year'] = train['datetime'].dt.year  # dt 연산자 사용
train['month'] = train['datetime'].dt.month
train['day'] = train['datetime'].dt.day
train['hour'] = train['datetime'].dt.hour
train['minute'] = train['datetime'].dt.minute
train['second'] = train['datetime'].dt.second
print(train.head(1))
print(train.columns)

# 대여량 시각화: 연도, 월, 일, 시간별 평균 대여량 확인
figure, (ax1,ax2,ax3,ax4) = plt.subplots(nrows=1, ncols=4)
figure.set_size_inches(15, 5)

# sns.barplot: 카테고리별 평균값과 신뢰구간을 막대 그래프로 표시
sns.barplot(data=train, x='year', y='count', ax=ax1)  # 연도별 대여량
sns.barplot(data=train, x='month', y='count', ax=ax2) # 월별 대여량
sns.barplot(data=train, x='day', y='count', ax=ax3)
sns.barplot(data=train, x='hour', y='count', ax=ax4)
ax1.set(ylabel='대여수', title='연도별 대여수')
ax2.set(ylabel='대여수', title='월별 대여수')
ax3.set(ylabel='대여수', title='일별 대여수')
ax4.set(ylabel='대여수', title='시간별 대여수')
plt.show()

# 박스 플롯(Box Plot): 데이터의 분포, 중앙값 및 이상치 확인
fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_size_inches(12, 10)

sns.boxplot(data=train, y='count', orient='v', ax=axes[0][0])             # 전체 대여량 분포
sns.boxplot(data=train, y='count', x='season', orient='v', ax=axes[0][1]) # 계절별 대여량
sns.boxplot(data=train, y='count', x='hour', orient='v', ax=axes[1][0])
sns.boxplot(data=train, y='count', x='workingday', orient='v', ax=axes[1][1])
axes[0][0].set(ylabel='대여수', title='대여')
axes[0][1].set(xlabel='계절', ylabel='대여수', title='계절별 대여수')
axes[1][0].set(xlabel='시간', ylabel='대여수', title='시간별 대여수')
axes[1][1].set(xlabel='근무일', ylabel='대여수', title='근무일별 대여수')
plt.show()

# 산점도 및 회귀선(regplot): 수치형 변수 간의 상관관계 분석
figure, (ax1,ax2,ax3) = plt.subplots(ncols=3)
fig.set_size_inches(12, 5)
sns.regplot(x='temp', y='count', data=train, ax=ax1)      # 온도와 대여량의 관계
sns.regplot(x='humidity', y='count', data=train, ax=ax2)  # 습도와 대여량의 관계
sns.regplot(x='windspeed', y='count', data=train, ax=ax3) # 풍속과 대여량의 관계
plt.show()
