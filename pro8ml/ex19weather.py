# LogisticRegression - 날씨 예보 (비가 올지 여부)
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import statsmodels.api as sm
import statsmodels.formula.api as smf

data = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/weather.csv")
print(data.head(2), data.shape) # (366, 12)
data2 = pd.DataFrame()
data2 = data.drop(['Date','RainToday'], axis=1)
data2['RainTomorrow'] = data2['RainTomorrow'].map({'Yes':1, 'No':0})
print(data2.head(2), data2.shape) # (366, 10)
print(data2.RainTomorrow.unique()) # [1 0]

# RainTomorrow : 종속변수(범주형, label, class), 나머지 열 : 독립변수(feature)

print('데이터 분리 : 학습용(train data), 검증용(test data) ----')
# 모델의 성능을 객관적으로 파악 가능.  모델학습과 검증에 사용된 자료가 같다면 오버피팅(과적합) 우려 발생.
train, test = train_test_split(data2, test_size=0.3, random_state=42)
print(train.shape, test.shape)  #  (256, 10) (110, 10)
print(train.head(3))
print(test.head(3))

# 분류 모델 생성
col_select = "+".join(train.columns.difference(['RainTomorrow']))
my_formula = 'RainTomorrow ~ ' + col_select
# model = smf.glm(formula=my_formula, data=train, family=sm.families.Binomial()).fit()
model = smf.logit(formula=my_formula, data=train).fit()
print(model.summary())
print(model.params)

# 예측 및 성능 평가
pred = model.predict(test)
print('예측값(확률) :\n', pred[:5].values)
print('실제값 : ', test['RainTomorrow'][:5].values)

# 0.5를 기준으로 이진 분류 (1: 비 옴, 0: 비 안 옴)
pred_binary = np.around(pred.values)
print('예측값(분류) :', pred_binary[:5])
print('실제값(분류) :', test['RainTomorrow'][:5].values)

# 분류 정확도
conf_mat = model.pred_table()
print(conf_mat)
print('분류 정확도 :', (conf_mat[0][0] + conf_mat[1][1]) / len(train))
# 분류 정확도 : 0.87109375
print('분류 정확도 :', accuracy_score(test['RainTomorrow'], pred_binary))
# 분류 정확도 : 0.8727272727272727