# 이원카이제곱
# 동질성 검정 : 두 집단의 분포가 동일한가 다른 분포인가를 검증하는 방법이다.
# 분포 비율 차이 검정
# 두 집단 이상에서 각 범주 집단 간의 비율이 서로 동일한가를 검정하게 된다
# 두 개 이상의 범주형 자료가 동일한 분포를 갖는 모집단에서 추출된 것인지 검정하는 방법이다.

# 동질성 검정실습 1 :
# 교육방법(독립변수)에 따른 교육생들의 만족도 분석 동질성 검정

# 귀무 : 교육방법에 따른 교육생들의 만족도에 차이가 없다.
# 대립 : 교육방법에 따른 교육생들의 만족도에 차이가 있다.

import pandas as pd
import scipy.stats as stats

# 만족도에 대한 설문조사 수집 자료
data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/survey_method.csv")
print(data.head(3))
print(data['method'].unique())   # [1 2 3]
print(data['survey'].unique())   # [1 2 3 4 5]

ctab = pd.crosstab(index=data['method'], columns=data['survey'])
print(ctab)
ctab.index = ['방법1', '방법2', '방법3']
ctab.columns = ['매우만족', '만족', '보통', '불만족도', '매우불만족']
print(ctab)  # 관측된 분포 비율

chi2, p, dof, expected = stats.chi2_contingency(ctab)
print(f"카이제곱 통계량: {chi2}")  # 카이제곱 통계량: 6.544667820529891
print(f"p-value: {p}")  # p-value: 0.5864574374550608
print(f"자유도: {dof}") # 자유도: 8
print(f"기대값: {expected}")  # 예측 비율

# 판정 : p-value(0.5864) > 0.05 이므로 귀무가설을 채택한다.
# 결론: 교육방법에 따른 교육생들의 만족도에 유의미한 차이가 없다. (동질적이다)



# 동질성 검정 실습2) 연령대별 sns 이용률의 동질성 검정
# 20대에서 40대까지 연령대별로 서로 조금씩 그 특성이 다른 SNS 서비스들에 대해 이용 현황을 조사한 자료를 바탕으로 연령대별로 홍보
# 전략을 세우고자 한다.
# 연령대별로 이용 현황이 서로 동일한지 검정해 보도록 하자.

# 귀무 : 연령대 별로 sns 서비스별 이용률 현황은 동일하다.
# 대립 : 연령대 별로 sns 서비스별 이용률 현황은 불일치하다. 

import pandas as pd
import scipy.stats as stats

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/snsbyage.csv")
print(data.head(3))
print(data['age'].unique())       # [1 : 20대, 2 : 30대, 3 : 40대]
print(data['service'].unique())   # ['F' 'T' 'K' 'C' 'E']
print(data.shape)  # (1439, 2)

ctab2 = pd.crosstab(index=data['age'], columns=data['service'])
print(ctab2)

chi2, p, dof, expected = stats.chi2_contingency(ctab2)
print(f"\n카이제곱 통계량: {chi2}")   # 카이제곱 통계량: 102.75202494484225
print(f"p-value: {p}")                # p-value: 1.1679064204212775e-18
print(f"자유도: {dof}")                # 자유도: 8
print(f"기대값: {expected}")  # 예측된 기대도수

# 판정 : 유의수준 0.05 기준
# p-value(1.167e-18) < 0.05 이므로 귀무가설을 기각하고 대립가설을 채택한다.
# 결론: 연령대별로 SNS 서비스 이용 현황은 통계적으로 유의미한 차이가 있다. (동질적이지 않다)

print('-'*40)
print('전체 건수 : ', len(data))  # 전체 건수 :  1439

# [샘플링을 하는 이유]
# 1. 비용 및 시간 절약: 모집단 전체를 조사하기 어려운 경우 일부만 추출하여 효율적으로 분석하기 위함.
# 2. 데이터 크기 조절: 너무 방대한 데이터는 연산 속도를 저하시키므로 적절한 크기로 줄여 분석의 편의성을 높임.
# 3. 일반화 가능성 확인: 추출된 샘플이 모집단의 특성을 잘 반영하는지(대표성) 확인하기 위함.

samp_data = data.sample(n=500, replace=True, random_state=1)
print(samp_data.head(), ' ', len(samp_data))

ctab3 = pd.crosstab(index=samp_data['age'], columns=samp_data['service'])
chi2, p, dof, expected = stats.chi2_contingency(ctab3)
print(f"\n[샘플 데이터 검정 결과]")
print(f"카이제곱 통계량: {chi2:.4f}")   # 카이제곱 통계량: 36.2075
print(f"p-value: {p:.7f}")             # p-value: 0.0000161

# [샘플 데이터 판정] p-value(0.0000161) < 0.05 이므로 귀무가설 기각.
# 샘플링된 데이터에서도 연령대별 SNS 서비스 이용 현황은 차이가 있다는 결론이 나옴.
print(f"자유도: {dof}")                # 자유도: 8
print(f"기대값: {expected}")  # 예측된 기대도수
