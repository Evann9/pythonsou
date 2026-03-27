# 교차분석(카이제곱, 카이스퀘어) 가설 검정
# 범주형 자료(변수)를 대상으로 교차 반도에 대한 기술 통계량을 제공
# 교차빈도에 대한 통계적 유의성을 검증해주는 분석기법
# 분산이 퍼져있는 모습을 분포로 만든 것이 카이제곱 분포(음수는 안나옴)
# X² = ∑(관측값 - 기대값)² / 기대값

# 적합도 : 일원카이제곱 검정
# 독립성, 동질성 검정 : 이일원카이제곱 검정

# 가설을 채택하는 두가지 방법 연습
import pandas as pd
data = pd.read_csv("pass_cross.csv", encoding="euc-kr")
print(data.head())
print(data.shape)  # (50, 4)
print(data.shape[0])
print(data.shape[1])
print()

# 귀무가설(H0) : 벼락치기 공부하는 것과 합격 여부는 관계가 없다.
# 대립가설(H1) : 벼락치기 공부하는 것과 합격 여부는 관계가 있다.

print(data[(data['공부함'] == 1) & (data['합격'] == 1)].shape[0])    # 18
print(data[(data['공부함'] == 1) & (data['불합격'] == 1)].shape[0])  # 7

print('---빈도표 작성 ------------------')
ctab = pd.crosstab(index=data['공부안함'], columns=data['불합격'],margins=True)
ctab.columns = ['합격', '불합격', '행합']
ctab.index = ['공부함', '공부안함', '열합']
print(ctab) # 관찰값(빈도)

# 검정방법1 : 카이제곱표 => 임계값 구할 수 있음
# 기대도수 = (각 행의 주변 합) * (각 열의 주변 합) / 총합<전체 표본수>

print((18-15)**2/15 + (7-10)**2/10 + (12-15)**2/15 + (13-10)**2/10)
# chi2 = 3.0
# df = 2 - 1 = 1
# 유의수준 : 0.05
# 임계값 : 3.84
# 판정 : 카이제곱 통계량(3.0) < 임계값(3.84) 이므로 귀무가설 채택(유의미한 차이가 없다)
# 그러므로 벼락치기 공부하는 것과 합격 여부는 관계가 없다.는 귀무가설 의견 유지.

print()
# 검정방법2 : p-value 사용
import scipy.stats as stats

# chi2_contingency는 관측빈도표를 입력받아 카이제곱 통계량, p-value, 자유도, 기대빈도를 반환함
chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f'카이제곱 통계량: {chi2}')   # 카이제곱 통계량: 3.0
print(f'p-value: {p}')             # p-value: 0.5578254003710748

# 판정 : 유의수준 0.05 < p: 0.557825 이므로 귀무 채택
# 검정에 사용된 자료는 우연히 발생한 자료라고 할 수 있다.

# chi2 검정 정식명칭 : Perason's chi-suare test
# 두개의 불연속 변수(범주형) 간의 상관관계를 측정. 관찰 빈도가 통계적으로 유의한지 확인.
