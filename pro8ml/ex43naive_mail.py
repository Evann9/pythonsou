# 스팸 메일 분류기 - spam 자료를 파일에서 읽기

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics  import accuracy_score, confusion_matrix
import sklearn.metrics as metrics
import pandas as pd
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import koreanize_matplotlib

# 1. 데이터 읽기 및 라벨 정리
# text  : 메일 본문
# label : spam(스팸) / ham(정상 메일)
df = pd.read_csv("https://raw.githubusercontent.com/pykwon/python/refs/heads/master/testdata_utf8/mydata.csv")
print(df.head(2))

# label 값에 공백이나 대소문자 차이가 있으면 학습 결과가 달라질 수 있으므로 통일
df['label'] = df['label'].str.strip().str.lower()  # 공백 제거 + 소문자

# 학습용 입력 문장과 정답 라벨을 리스트로 분리
texts = df['text'].tolist() 
labels = df['label'].tolist()
print(texts[:3]) # ['광고성 메일을 확인하세요', '회의 일정 변경 공지', '무료 쿠폰을 지금 사용하세요']
print(labels[:3]) # ['spam', 'ham', 'spam']

print()
# 학습용 / 테스트용 데이터 분리
# stratify=labels : spam / ham 비율이 train, test에 비슷하게 유지되도록 함
x_train, x_test, y_train, y_test = train_test_split(texts, labels, test_size=0.25, random_state=42, stratify=labels)

# 2. 문장을 숫자 벡터로 변환
# CountVectorizer는 문장을 단어별 등장 횟수로 바꿔 준다.
# 예: "무료 쿠폰 무료" -> 무료:2, 쿠폰:1
vectorizer = CountVectorizer()
x_train_vec = vectorizer.fit_transform(x_train) # 단어 사전을 만듦
x_test_vec = vectorizer.transform(x_test)  # test는 transform만 해줘야 함.(숫자변환)
# print(x_train_vec.shape, x_test_vec.shape)

# 3. 모델 생성 및 학습
# MultinomialNB는 단어 빈도 기반 텍스트 분류에 자주 사용하는 모델이다.
model = MultinomialNB()
model.fit(x_train_vec, y_train)

# 4. 예측 및 평가
# confusion_matrix:
# [ [ham을 ham으로 맞춤, ham을 spam으로 틀림],
#   [spam을 ham으로 틀림, spam을 spam으로 맞춤] ]
y_pred = model.predict(x_test_vec)
acc = accuracy_score(y_test, y_pred)
print('분류 정확도 : ', acc)   # 0.8
print('confusion matrix : \n', confusion_matrix(y_test, y_pred))
#  [[2 1]
#   [0 2]]

# confusion matrix
cm = confusion_matrix(y_test, y_pred, labels=['ham', 'spam'])
print(cm)

# confusion matrix를 시각화 
disp = metrics.ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=['ham', 'spam'])
disp.plot(cmap='Blues')
plt.title('Confusion Matrix(혼동 행렬)')
plt.show()

# 사용자 입력 메일 내용 분류
while True:
    userInput = input('이메일 내용 입력(종료는 q): ')
    if userInput.lower() == 'q':
        break
    x_new = vectorizer.transform([userInput])
    prob = model.predict_proba(x_new)[0]
    spam_prob = prob[(model.classes_).tolist().index('spam')]
    
    result = '스팸이다!!' if spam_prob > 0.7 else '정상 메일'
    print(f"스팸 확률은 {spam_prob*100:.2f} -> {result}")

