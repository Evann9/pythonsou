# 스팸 메일 분류기

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics  import accuracy_score
# Multinomial Naive Bayes (다항 나이브 베이즈).
# 텍스트에서 가장 많이 쓰는 NB 모델
# 단어의 “빈도(count)”를 기반으로 분류함
# 형태: 단어가 많이 나왔으면 그 단어 빈도에 비례해 확률이 커짐

# 학습용 자료
texts = [
    "무료 쿠폰 지금 무료 클릭하면 무료 선물",
    "한번만 클릭하면 무료 무료 대박",
    "오늘 회의는 2시",
    "지금 할인 행사 진행중",
    "회의 자료는 메일로 보내주세요",
    "지금 바로 쿠폰 확인"
]
labels = ["spam", "spam", "ham", "spam", "ham", "spam"]

# 단어 등장 횟수 기반 벡터
vect = CountVectorizer()  # 문서들로 부터 단어의 순서 정보는 버리고, 단어 빈도수 정보를 추출
x = vect.fit_transform(texts)
print(vect.get_feature_names_out())  # 공백을 기준으로 문장을 자름.
# ['2시' '메일로' '무료' '바로' '보내주세요' '오늘' '자료는' '지금' '진행중' '쿠폰' '클릭' '클릭하면' '한번만'
#  '할인' '행사' '확인' '회의' '회의는']
print(x) # (0, 2)  2  <= (문서번호, 단어 번호)  반복 횟수
print(x.toarray())
# [[0 0 2 0 0 0 0 1 0 1 1 0 0 0 0 0 0 0]
#  [0 0 1 0 0 0 0 0 0 0 0 1 1 0 0 0 0 0]
#  [1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 1]
#  [0 0 0 0 0 0 0 1 1 0 0 0 0 1 1 0 0 0]
#  [0 1 0 0 1 0 1 0 0 0 0 0 0 0 0 0 1 0]
#  [0 0 0 1 0 0 0 1 0 1 0 0 0 0 0 1 0 0]]
print(vect.vocabulary_)  # 인덱싱 정보 확인 가능

# 모델 생성
model = MultinomialNB()
model.fit(x, labels)
pred = model.predict(x)
print('정확도 : ', accuracy_score(labels, pred))

# 새로운 문장 테스트
test_text = ['무료 쿠폰 지금 발급','간부 회의는 언제 시작하나요?']
x_test = vect.transform(test_text)
print(x_test)

preds = model.predict(x_test)
probs = model.predict_proba(x_test)
class_names = model.classes_  # ['ham','spam']

for text, pred, prob in zip(test_text, preds, probs):
    prob_str = ", ".join([f"{cls}: {p:.4f}" for cls, p in zip(class_names, prob)])
    print(f"'{text}' -> 예측:{pred} / 확률:{prob_str}")