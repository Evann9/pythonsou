# iris dataset으로 꽃 종류 분류기 (ROC Curve 까지 표현)
# layer 수에 따른 모델 성능 비교
#
# 이 파일의 흐름
# 1) 붓꽃 4개 수치 feature로 3개 품종을 분류한다.
# 2) 은닉층 개수가 다른 모델 3개를 만들어 validation 성능을 비교한다.
# 3) ROC Curve와 AUC로 모델별 분류 성능을 시각화한다.

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input, Dropout

iris = load_iris()
# print(iris.DESCR)
print(iris.keys())

# x는 꽃받침/꽃잎 길이와 너비, y는 품종 번호이다.
x = iris.data   # feature
print(x[:2])
y = iris.target # label
print(y[:2])
names = iris.target_names
print(names)    # ['setosa' 'versicolor' 'virginica']
feature_names = iris.feature_names
print(feature_names)    # ['sepal length (cm)', ...

# label 원핫 처리
# softmax + categorical_crossentropy를 사용할 것이므로 정답을 one-hot으로 바꾼다.
onehot = OneHotEncoder(categories='auto')
# y = onehot.fit_transform(y[:, np.newaxis]).toarray()
y = onehot.fit_transform(y[:, None]).toarray()
print('후 : ', y.shape)
print(y[:2])

# feature 표준화
# 네 feature의 단위는 같지만 평균/분산을 맞추면 신경망 학습이 더 안정적이다.
scaler = StandardScaler()
x_scale = scaler.fit_transform(x)
print(x[:2])
print(x_scale[:2])


x_train, x_test, y_train, y_test = train_test_split(
    x_scale, y, test_size=0.3, random_state=42, stratify=y
)
print(x_train.shape, x_test.shape)  # (105, 4) (45, 4)

n_features = x_train.shape[1]
n_classes = y_train.shape[1]
print(n_features, ' ', n_classes)

# layer의 갯수가 다른 모델 여러 개 생성 함수
def create_custom_model(input_dim, output_dim, out_nodes, n, model_name='model'):
    # 함수를 반환하는 함수이다. n을 바꿔 은닉층 개수가 다른 모델 생성기를 만든다.
    # print(input_dim, output_dim, out_nodes, n, model_name)
    def create_model():
        model = Sequential(name = model_name)
        model.add(Input(shape=(input_dim, )))
        for _ in range(n):
            model.add(Dense(units=out_nodes, activation='relu'))

        model.add(Dense(units=output_dim, activation='softmax'))
        return model
    return create_model     # 클로저

models = [create_custom_model(n_features, n_classes, 10, n, f'model_{n}') for n in range(1, 4)]
# print(models)

# 구조 확인
for create_model in models:
    print()
    create_model().summary()

history_dict = {}

for create_model in models:
    model = create_model()
    print('모델명:', model.name)
    model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    historys = model.fit(x_train, y_train, batch_size=4, epochs=50, verbose=0, validation_split=0.3)
    score = model.evaluate(x_test, y_test, verbose=0)
    print(f'loss:{score[0]}, acc:{score[1]}')
    # 학습 기록과 모델 객체를 함께 보관해 뒤에서 그래프와 ROC 계산에 재사용한다.
    history_dict[model.name] = [historys, model]

print(history_dict)

# 시각화
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 8))

for model_name in history_dict:
    print('h_d : ', history_dict[model_name][0].history['accuracy'])
    val_acc = history_dict[model_name][0].history['val_accuracy']
    val_loss = history_dict[model_name][0].history['val_loss']
    # 은닉층 개수별 validation accuracy/loss를 같은 축에 그려 비교한다.
    ax1.plot(val_acc, label=model_name)
    ax2.plot(val_loss, label=model_name)
    ax1.set_ylabel('val acc')
    ax2.set_ylabel('val loss')
    ax2.set_xlabel('epoch')
    ax1.legend()
    ax2.legend()
plt.show()

print()
# ROC Curve - 분류기에 대한 성능 평가 기법
from sklearn.metrics import roc_curve, auc

plt.figure()
plt.plot([0, 1], [0, 1], 'k--')

for model_name in history_dict:
    model = history_dict[model_name][1]
    y_pred = model.predict(x_test)

    # 다중분류 결과를 펼쳐 one-vs-rest 방식처럼 전체 ROC를 계산한다.
    fpr, tpr, _ = roc_curve(y_test.ravel(), y_pred.ravel())
    plt.plot(fpr, tpr, label='{}, AUC:{:.3f}'.format(model_name, auc(fpr, tpr)))

plt.xlabel('fpr(false positive rate)')
plt.ylabel('tpr(true positive rate)')
plt.title('ROC Curve')
plt.legend()
plt.show()

