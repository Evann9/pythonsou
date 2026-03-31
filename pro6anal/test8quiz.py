import numpy as np 
import pandas as pd
import scipy.stats as stats
from scipy.stats import wilcoxon
from xlrd import open_workbook


# [one-sample t 검정 : 문제1]  
# 영사기( 프로젝터 )에 사용되는 구형 백열전구의 수명은 250 시간이라고 알려졌다. 
# 한국 연구소에서 수명이 50 시간 더 긴 새로운 백열전구를 개발하였다고 발표하였다. 
# 연구소의 발표결과가 맞는지 새로 개발된 백열전구를 임의로 수집하여 수명 시간 관련 자료를 얻었다. 
# 한국 연구소의 발표가 맞는지 새로운 백열전구의 수명을 분석하라.
# 수집된 자료 :  305 280 296 313 287 240 259 266 318 280 325 295 315 278

# 귀무 : 백열전구는 수명이 300시간이다. 
# 대립 : 백열전구는 수명이 300시간이 아니다.

data = [305, 280, 296, 313, 287, 240, 259, 266, 318, 280, 325, 295, 315, 278]
print(f"표본 평균: {np.mean(data):.2f}")  # 289.79

result = stats.ttest_1samp(data, popmean=300)  # (데이터, 예상평균값(모수의 평균))
print(f"t-통계량: {result.statistic:.4f}")  # t-통계량: -1.5564
print(f"p-value: {result.pvalue:.4f}")      #  p-value: 0.1436

# [판정] 유의수준 0.05 기준
# p-value(0.1436) >= 0.05 이므로 백열전구는 수명이 300시간이다. (귀무가설 채택)

print('-'*40)
# [one-sample t 검정 : 문제2] 
# 국내에서 생산된 대다수의 노트북 평균 사용 시간이 5.2 시간으로 파악되었다. 
# A회사에서 생산된 노트북 평균시간과 차이가 있는지를 검정하기 위해서 
# A회사 노트북 150대를 랜덤하게 선정하여 검정을 실시한다.  

# 참고 : time에 공백을 제거할 땐 ***.time.replace("     ", ""),
#           null인 관찰값은 제거.

# 귀무 : 노트북 평균 사용시간은 5.2시간이다.
# 대립 : 노트북 평균 사용시간은 5.2시간이 아니다.

data2 = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/one_sample.csv")
print(data2.head())

# 데이터 전처리: 결측치 제거 및 공백 제거 후 수치형 변환
data2 = data2.dropna(subset=['time'])
data2['time'] = data2['time'].astype(str).str.strip()
data2 = data2[data2['time'] != ""]
data2['time'] = data2['time'].astype(float)

print(f"표본 평균: {data2['time'].mean():.2f}")

# 단일표본 t-검정
result2 = stats.ttest_1samp(data2['time'], popmean=5.2)
print(f"t-통계량: {result2.statistic:.4f}, p-value: {result2.pvalue:.4f}")

# [판정] 유의수준 0.05 기준
# p-value(0.0001) < 0.05 이므로 귀무가설을 기각한다.
# 결론: A회사 노트북의 평균 사용 시간은 5.2시간과 차이가 있다. (대립가설 채택)

print('-'*40)
# [one-sample t 검정 : 문제3] 
# https://www.price.go.kr/tprice/portal/main/main.do 에서 
# 메뉴 중  가격동향 -> 개인서비스요금 -> 조회유형:지역별, 품목:미용 자료(엑셀)를 파일로 받아 미용 요금을 얻도록 하자. 
# 정부에서는 전국 평균 미용 요금이 15000원이라고 발표하였다. 이 발표가 맞는지 검정하시오. (월별)

# 귀무 : 전국 평균 미용 요금이 15000원이다.
# 대립 : 전국 평균 미용 요금이 15000원이 아니다.

data3 = pd.read_excel('price.xls')

data4 = data3.iloc[0, 2:]    
data4 = pd.to_numeric(data4, errors='coerce') # 추출된 데이터를 숫자 타입으로 변환
data4 = data4.dropna()       #  결측치(NaN)를 제거

print('표본 평균 미용 요금 :', data4.mean())
print('표본 크기 :', len(data4))

# 정규성 검정
result3 = stats.shapiro(data4)
print(f"Shapiro p-value: {result3.pvalue:.4f}")
# [판정] p-value(0.0880) > alpha 0.05 이므로 정규성을 만족함. 

# one-sample t-test
t_result3 = stats.ttest_1samp(data4, popmean=15000)
print(f"t-통계량: {t_result3.statistic:.4f}, p-value: {t_result3.pvalue:.4f}")

# [최종 판정] 유의수준 0.05 기준
# 판정: p-value < 0.05 이므로 전국 평균 미용 요금은 15000원이 아니다. (대립가설 채택)