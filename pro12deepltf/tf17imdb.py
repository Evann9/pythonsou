# imdb dataset으로 이진 분류 : 영화 리뷰(긍정,부정)
# train : 25000, test : 25000

from tensorflow.keras.datasets import imdb
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Embedding, GlobalAveragePooling1D, Dropout, Input
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import os


num_words = 10000
# 자주 등장하는 단어 1만개만 사용
(train_data, train_label), (test_data, test_label) = imdb.load_data(num_words=10000)
print(type(train_data), train_data.shape)   # <class 'numpy.ndarray'> (25000,)
print(type(test_data), test_data.shape)     # <class 'numpy.ndarray'> (25000,)
print(train_data[0], len(train_data[0]))    # ... 19, 178, 32, 218
# 전처리된 데이터로 각 리뷰(단어)가 숫자화 되었다. 각 숫자는 고유 단어 색인
print(train_label[0])   # 0-부정 , 1-긍정

# 참고로 이 리뷰 데이터 한 개를 원래 문장으로 보기
word_index = imdb.get_word_index()
# print('word_index : ', word_index)
sorted_word_index = sorted(word_index.items(), key=lambda x:x[1])
for word, index in sorted(word_index.items())[:10]:
    print(word, index)

reverse_word_index = {
    index + 3:word      # 특수토큰 세개가 선행하므로 실제단어 index + 3
    for word, index in word_index.items()
}
# 특수 토큰
reverse_word_index[0] = "<PAD>"     # 패딩
reverse_word_index[1] = "<START>"   # 문장 시작
reverse_word_index[2] = "<UNK>"     # 모르는 단어
reverse_word_index[3] = "<UNUSED>"  # 사용 안함
# 0 번째 리뷰 문장으로 복원
decord_review = " ".join(
    reverse_word_index.get(i, "?") for i in train_data[0]
)

print('0번째 문장:', decord_review)
# load_data() 안에서는 0~3번을 특수 토큰으로 쓰기 때문에 실제 리뷰 데이터에서 the는 4
print('0번째 라벨:', train_label[0])

# 리뷰 길이 확인
review_len = [len(review) for review in train_data]
print('최소 길이 : ', np.min(review_len))
print('최대 길이 : ', np.max(review_len))
print('평균 길이 : ', np.mean(review_len))
print('중앙 값 : ', np.median(review_len))

plt.figure(figsize=(8, 5))
plt.hist(review_len, bins=50)
plt.xlabel('리뷰길이')
plt.ylabel('건수')
plt.grid(True)
plt.show()

# padding : 리뷰 문장 길이가 다름. 모델에 넣기 전에 길이를 맞춤
# 각 리뷰를 최대 200 단어 index로 맞춤. 길면 앞부분 자르고, 짧으면 0을 채움
maxlen = 200
x_train = pad_sequences(train_data, maxlen=maxlen)
x_test = pad_sequences(test_data, maxlen=maxlen)
y_train = np.array(train_label).astype(np.float32)
y_test = np.array(test_label).astype(np.float32)
print('x_train : ', x_train.shape)  # (25000, 200)
print('x_test : ', x_test.shape)    # (25000, 200)
print('y_train : ', y_train.shape)  # (25000,)
print('y_train : ', y_test.shape)   # (25000,)
print('패딩된 1번째 : ', x_train[1])    #  [   0    0    0    0    0    0    0    0    0    0    0    1  194 1153


# 모델 저장용 폴더 준비
MODEL_DIR = "./imdb_model/"
if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

modelpath = "./imdb_model/imdb_best.keras"

model = Sequential([
    Input(shape=(maxlen, )),
    Embedding(  # 단어 index를 밀집벡터로 변환
        input_dim=num_words,    # 리뷰1개가 단어번호 200개로 들어옴
        output_dim=32   # 단어 하나를 32개의 실수로 표현함
        # 밀집벡터화 : 실수 기반의 고정 크기에 실수값으로 채움. 예[0.2, -0.1, 0.03, 0.5...]
    ),
    GlobalAveragePooling1D(),   
    # 200개의 단어 벡터를 평균내서 리뷰 전체를 하나의 32차원 벡터화. 이것이 리뷰 전체의 특징이 됨
    Dense(units=32, activation='relu'),
    Dropout(0.3),
    Dense(units=16, activation='relu'),
    Dropout(0.3),
    Dense(units=1, activation='sigmoid')
])

print(model.summary())  # Total params: 321, 601 (1.23 MB)

model.compile(optimizer=Adam(learning_rate=0.001), loss='binary_crossentropy', metrics=['accuracy'])

early_stop = EarlyStopping(monitor='val_loss', patience=3, restore_best_weights=True)
chkpoint = ModelCheckpoint(filepath=modelpath, monitor='val_loss', save_best_only=True, verbose=0)

history = model.fit(x_train, y_train, epochs=50, batch_size=512, validation_split=0.2, callbacks=[early_stop, chkpoint], verbose=2)

loss, acc = model.evaluate(x_test, y_test, verbose=0)
print('테스트 평가 손실 : ', loss)
print('테스트 평가 정확도 : ', acc)

plt.figure(figsize=(12, 5))

# loss, acc 시각화
plt.subplot(1, 2, 1)
plt.plot(history.history['loss'], label='loss')
plt.plot(history.history['val_loss'], label='val_loss')
plt.xlabel('epoch')
plt.ylabel('loss')
plt.legend()

plt.subplot(1, 2, 2)
plt.plot(history.history['accuracy'], label='accuracy')
plt.plot(history.history['val_accuracy'], label='val_accuracy')
plt.xlabel('epoch')
plt.ylabel('accuracy')
plt.legend()
plt.grid(True)
plt.show()

print('\n\n저장된 모델 읽어 분류 예측')
best_model = load_model(modelpath)
best_loss, best_acc = best_model.evaluate(x_test, y_test, verbose=0)
print('best_model 평가 손실 : ', best_loss)
print('best_model 평가 정확도 : ', best_acc)

# 기존 데이터를 사용해 예측
new_data = x_test[:5]
new_label = y_test[:5]
pred_prob = best_model.predict(new_data, verbose=0)
pred_class = (pred_prob >= 0.5).astype(int).ravel()
print('예측 확률 : ', pred_prob.ravel())
print('예측 값 : ', pred_class)
print('실제 값 : ', new_label.astype(int).ravel())

for i in range(5):
    result = "긍정" if pred_class[i] == 1 else "부정"
    real = "긍정" if new_label[i] == 1 else "부정"
    print(f'{i + 1}번 리뷰 예측:{result}, 실제:{real}, 긍정확률:{pred_prob[i][0]}')



