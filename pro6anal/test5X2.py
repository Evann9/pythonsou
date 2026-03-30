# [이원 카이제곱 검정 (Two-way Chi-square test)]
# 목적: 독립성 검정 (Independence Test) 또는 동질성 검정 (Homogeneity Test)
# 내용: 두 범주형 변수 간에 연관성이 있는지(독립적인지) 검정
# 대상: 두 개의 범주형 변수

# [실습 예제]
# 교육 수준(대학원졸, 대졸, 고졸)과 흡연 여부 간의 관련성 검정

# 귀무가설(H0): 교육 수준과 흡연 여부는 관련이 없다. (독립적이다)
# 대립가설(H1): 교육 수준과 흡연 여부는 관련이 있다. (독립적이지 않다)

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/smoke.csv")
print(data.head())
print(data['education'].unique())  # [1 : 대학원졸, 2 : 대졸, 3 : 고졸]
print(data['smoking'].unique())  # [1 : 과흡연,  2 : 보통,  3: 노담]
print(data.shape)  # (355, 2)


# 학력 수준별 흡연 빈도수 : 교차표 사용
# 이원 카이제곱 검정은 두 변수 간의 빈도 합계를 기반으로 하므로, 
# 분석 전 반드시 pd.crosstab() 등을 사용하여 교차표(Contingency Table)를 만들어야 함.
ctab = pd.crosstab(index=data['education'], columns=data['smoking'])
# ctab = pd.crosstab(index=data['education'], columns=data['smoking'], normalize=True)  # 비율로 출력
ctab.columns = ['과흡연', '보통', '노담']
ctab.index = ['대학원졸', '대졸', '고졸']
print(ctab)

# 이원 카이제곱 검정
# chi_result = [ctab.loc['대학원졸'], ctab.loc['대졸'], ctab.loc['고졸']]
# chi2, p, dof, expected = stats.chi2_contingency(chi_result)
chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f"\n카이제곱 통계량: {chi2}")   # 카이제곱 통계량: 18.9109
print(f"p-value: {p}")                # p-value: 0.0008
print(f"자유도: {dof}")                # 자유도: 4
print(f"기대값: {expected}")  # 예측된 기대도수
# 기대값: [[68.94647887 83.8056338  58.24788732]
#         [16.9915493  20.65352113 14.35492958]
#         [30.06197183 36.54084507 25.3971831 ]]

# [판정] 유의수준 0.05 기준
# p-value가 0.05보다 작으므로 귀무가설을 기각한다. 교육 수준과 흡연 여부는 관련이 있다.

# 판정2 : chi2: 18.910915, 자유도 : 4 , critical value : 9.49
# chi2 값이 임계치 우측에 있으므로 귀무가설이 기각되고 대립가설이 채택

# 이후 다양한 자료, 의견 등으로 보고서를 작성

print('---독립성 검정 : 실습 2---------')
# 남성과 여성의 스포츠 음료 선호도 검정

# 귀무(H0) : 성별과 스포츠 음료 선호도는 관련이 없다.
# 대립(H1) : 성별과 스포츠 음료 선호도는 관련이 있다. 

data = pd.DataFrame({
    '게토레이':[30,20],
    '포카리':[20,30],
    '비타500':[10, 30],
},index=['남성', '여성'])
print(data)

chi2, p, dof, expected = stats.chi2_contingency(data)
print(f"\n카이제곱 통계량: {chi2}")   # 카이제곱 통계량: 11.375
print(f"p-value: {p}")                # p-value: 0.003388 )
print(f"자유도: {dof}")               # 자유도: 2
print(f"기대값: {expected}")           # 예측된 기대도수
# [[21.42857143 21.42857143 17.14285714]
#  [28.57142857 28.57142857 22.85714286]]

# [판정] 유의수준 0.05 기준
# p-value(0.0033) < 0.05 이므로 귀무가설을 기각하고 대립가설을 채택한다.
# 결론: 성별과 스포츠 음료 선호도 간에는 유의미한 관련이 있다. (독립적이지 않다)

# 히트맵 시각화
import matplotlib.pyplot as plt
import seaborn as sns
import koreanize_matplotlib

sns.heatmap(data, annot=True, fmt='d', cmap='Blues')
plt.title('성별과 스포츠 음료 선호도')
plt.xlabel('스포츠 음료')
plt.ylabel('성별')
plt.show()