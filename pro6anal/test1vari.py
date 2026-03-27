# 표준편차, 분산의 중요성

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib

np.random.seed(42)

# 목표 평균
target_mean = 60
std_dev_small = 10
std_dev_large = 20

# data
class1_raw = np.random.normal(loc=target_mean, scale=std_dev_small, size=100)
class2_raw = np.random.normal(loc=target_mean, scale=std_dev_large, size=100)

print(class1_raw[:5])

# 평균 보정
class1_adj = class1_raw - np.mean(class1_raw) + target_mean
print(class1_adj[:5])
class2_adj = class2_raw - np.mean(class2_raw) + target_mean
print(class2_adj[:5])

# 정수화
# np.clip(배열, 최소값, 최대값) : np.clip(배열, 10, 60) -> (5, 45, 78, ...) => (10, 45, 60, ...) 
class1 = np.clip(np.round(class1_adj), 10, 100).astype(int)
class2 = np.clip(np.round(class2_adj), 10, 100).astype(int)
print(class1[:10])
print(class2[:10])

# 기술 통계 계산
mean1, mean2 = np.mean(class1), np.mean(class2)
std1, std2 = np.std(class1), np.std(class2)
var1, var2 = np.var(class1), np.var(class2)

print('\n결과')
print('1반(성적 편차 작음)')
print(f'평균:{mean1}, 표준편차:{std1}, 분산:{var1}')
print('2반(성적 편차 큼)')
print(f'평균:{mean2}, 표준편차:{std2}, 분산:{var2}')

# 자료를 파일로 저장
df = pd.DataFrame({
    'class': ['1반'] * 100 + ['2반'] * 100,
    'score': np.concatenate([class1, class2]),
})

print(df.head())
df.to_csv('test1vari.csv', index=False, encoding='utf-8-sig')

print("--------- 시각화 ----------")
x1 = np.random.normal(1, 0.05, size=100)
x2 = np.random.normal(2, 0.05, size=100)

# 산포도
plt.figure(figsize=(10, 5))
plt.scatter(x1, class1, alpha=0.8, label=f'1반(평균={mean1:.2f}, 표준편차={std1:.2f})')
plt.scatter(x2, class2, alpha=0.8, label=f'2반(평균={mean2:.2f}, 표준편차={std2:.2f})')
plt.hlines(target_mean, 0.5, 2.5, color='r', linestyle='dashed', label=f'공통평균={target_mean}')
plt.xticks([1,2], ['1반', '2반'])
plt.ylabel('시험 점수')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# 박스플롯
plt.figure(figsize=(8, 5))
plt.boxplot([class1, class2], labels=['1반', '2반'])
plt.grid(True)
plt.show()

# 히스토그램
plt.figure(figsize=(10, 6))
plt.hist(class1, bins=15, alpha=0.6, label='1반', edgecolor='black')
plt.hist(class2, bins=15, alpha=0.6, label='2반', edgecolor='blue')
plt.axvline(target_mean, color='r', linestyle='dotted', label=f'공통평균={target_mean}')
plt.xlabel('시험 점수')
plt.ylabel('빈도')
plt.legend()
plt.tight_layout()
plt.show()

# 국어선생님 입장
# 귀무 가설(전통적 주장) : 두 반의 국어 점수의 표준편차(평균)는 차이가 없다.
# 누군가 실험을 통해 데이터 수집 후 두 반의 점수에 대한 통계 계산 후 새로운 주장(의견)
# => 대립 가설 : 두 반의 국어 점수의 표준편차(평균)는 차이가 있다.
# 가설 검젇(t-test)을 통해 두 의견의 채택, 기각을 판단할 수 있다.
