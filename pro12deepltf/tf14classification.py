# 딥러닝으로 이진분류 - 전통적 방식인 LogisticRegression의 확장

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.optimizers import Adam
import tensorflow as tf
import numpy as np

np.random.seed(42)
tf.keras.utils.set_random_seed(42)

x_data = np.array([[1,2],[2,3],[3,4],[4,3],[3,2],[2,1]], dtype=np.float32)
y_data = np.array([[0],[0],[0],[1],[1],[1]], dtype=np.float32)

print('1) Sequential API 버전 (빠른 구현)')
# 층을 순서대로 쌓는 단순 구조, 분기 구조나 다중 입출력 불가능
model = Sequential([
    Input(shape=(2, )),
    Dense(units=1, activation='sigmoid')
])
model = Sequential()
model.add(Input(shape=(2, )))
model.add(Dense(units=4, activation='relu'))
model.add(Dense(units=1, activation='sigmoid'))
print(model.summary())

# Binary Cross-Entropy(BCE)는 이진 분류(0 또는 1) 문제에서 모델의 예측 확률값과 실제값 사이의 오차를 계산한다.
model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
model.fit(x_data, y_data, epochs=20, batch_size=1, verbose=2)
m_eval = model.evaluate(x_data, y_data, verbose=0)
print(m_eval)
print(f'평가 결과 : 손실={m_eval[0]:.4f}, 정확도={m_eval[1]:.4f}')
# 손실을 최소화 하기 위해 경사하강법 사용
# z = w•x + b -> sigmoid(z) -> BCE계산 -> 역전파 gradient (y^ - y) -> w,b갱신

# 예측값과 실제값으로 시각화(S 곡선 형태)
import matplotlib.pyplot as plt
# 2차원 입력(x1, x2)을 가진 모델을 1차원 처럼 만들어 시그모이드(S곡선)를 보기위한 
x1_range = np.linspace(0, 6, 100)
x2_fixed = 2.5

# 입력 데이터 생성. 두 배열을 합쳐서 (x1, x2) 쌍 만들기
# np.full_like(x1_range, x2_fixed) x1_range와 같은 길이의 배열
x_vis = np.column_stack([x1_range, np.full_like(x1_range, x2_fixed)])
# print(x_vis)

y_prob = model.predict(x_vis, verbose=0)    # x1변화에 따른 출력확률

x1_real = x_data[:, 0]
y_real = y_data.ravel()

plt.figure(figsize=(7, 5))
plt.plot(x1_range, y_prob, label='sigmoid curve')
plt.scatter(x1_real, y_real, color='red', label='True data')
plt.xlabel('x data')
plt.ylabel('probability')
plt.legend(loc='lower right')
plt.grid()
plt.show()

from sklearn.metrics import accuracy_score
pred = model.predict(x_data, verbose=0)
pred_class = (pred >= 0.5).astype(int)
accuracy = accuracy_score(y_data, pred_class)
print(f'1) 정확도 | {accuracy:.4f}')

# 새로운 값으로 분류 예측
new_data = np.array([[1,2],[10,5]], dtype=np.float32)
pred = model.predict(new_data, verbose=0)
print('예측 확률 : ', pred.ravel())

print('예측 결과 : ', (pred >= 0.5).astype(int).ravel())
print('예측 결과 : ', [1 if i >= 0.5 else 0 for i in pred])
print('예측 결과 : ', np.where(pred >= 0.5, 1, 0).ravel())

print('2) Functional API 버전 (실무에서 주로 사용)')
# 다중 입출력 가능, 구조가 유연. 복잡한 모델에 효과적
from tensorflow.keras.models import Model

inputs = Input(shape=(2, ))
outputs = Dense(units=4, activation='relu')(inputs)
outputs = Dense(units=1, activation='sigmoid')(outputs)
model_func = Model(inputs=inputs, outputs=outputs)
print(model_func.summary())

model_func.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
model_func.fit(x_data, y_data, epochs=20, batch_size=1, verbose=2)
m_eval2 = model_func.evaluate(x_data, y_data, verbose=0)
print(m_eval2)
print(f'평가 결과 : 손실={m_eval2[0]:.4f}, 정확도={m_eval2[1]:.4f}')

print('\n3) Functional API 버전2 (다중 입력)')
# 이전 : [x1, x2] -> Dense -> Dense -> 출력
# 다중 입력 : 입력을 따로 받아서 각각 특징을 뽑아 합치는 방식. 각각 따로 전처리가 가능
# x1 -> Dense
#               -> concat -> Dense -> 출력
# x2 -> Dense

from tensorflow.keras.layers import Concatenate
# 입력 분리
input1 = Input(shape = (1, ))
input2 = Input(shape = (1, ))
# 각각 처리
x1 = Dense(units=2, activation='relu')(input1)
x2 = Dense(units=4, activation='relu')(input2)

merged = Concatenate()([x1, x2])
output = Dense(units=1, activation='sigmoid')(merged)  # 출력층
multi_model = Model(inputs=[input1, input2], outputs=[output])
print(multi_model.summary())

multi_model.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
# 데이터를 분리해서 입력
x1_data = x_data[:, 0].reshape(-1, 1)
x2_data = x_data[:, 1].reshape(-1, 1)
multi_model.fit([x1_data, x2_data], y_data, epochs=20, batch_size=1, verbose=2)
m_eval2_multi = multi_model.evaluate([x1_data, x2_data], y_data, verbose=0)
print(m_eval2_multi)
print(f'평가 결과 : 손실={m_eval2_multi[0]:.4f}, 정확도={m_eval2_multi[1]:.4f}')


print('\n3) Functional API 버전2 (다중 입력)')
class MyModel(Model):
    def __init__(self):
        super().__init__()
        # 사용할 레이어를 미리 정의
        self.dense1 = Dense(units=4, activation='relu')
        self.dense2 = Dense(units=1, activation='sigmoid')
    
    def call(self, x):
        # 순전파 흐름 정의
        x = self.dense1(x)
        x = self.dense2(x)
        return x

model_sub = MyModel()
model_sub.compile(loss='binary_crossentropy', optimizer=Adam(learning_rate=0.01), metrics=['accuracy'])
model_sub.fit(x_data, y_data, epochs=20, batch_size=1, verbose=2)
m_eval_sub = model_sub.evaluate(x_data, y_data, verbose=0)
print(f'평가 결과 : 손실={m_eval_sub[0]:.4f}, 정확도={m_eval_sub[1]:.4f}')
