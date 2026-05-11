
import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import tensorflow as tf
import sys
from tensorflow.keras.layers import Dense, Input, Activation, Flatten, Dropout


fashion_mist = tf.keras.datasets.fashion_mnist.load_data()
(x_train, y_train), (x_test, y_test) = fashion_mist
print(x_train.shape, y_train.shape, x_test.shape, y_test.shape)
# (60000, 28, 28) (60000,) (10000, 28, 28) (10000,)

class_names = ['T-shirt/top', 'Trouser', 'Pullover', 'Dress', 'Coat', 'Sandal', 'Shirt', 'Sneaker', 'Bag', 'Ankle boot']
print(set(map(int, y_test)))

# plt.imshow(x_train[0], cmap='gray')
# plt.show()

plt.figure(figsize=(10, 10))
for i in range(25):
    plt.subplot(5, 5, i + 1)
    plt.xticks([])
    plt.yticks([])
    plt.xlabel(class_names[y_train[i]])
    plt.imshow(x_train[i])
plt.show()

# 정규화
print(x_train[0])
x_train = x_train / 255.0
print(x_train[0])
x_test = x_test / 255.0

# model
model = tf.keras.models.Sequential([
    tf.keras.layers.Input(shape=(28, 28)),
    tf.keras.layers.Flatten(),  # 차원 축소: resize 안한 경우
    tf.keras.layers.Dense(units=128, activation='relu'),
    tf.keras.layers.Dense(units=64, activation='relu'),
    tf.keras.layers.Dense(units=32, activation='relu'),
    tf.keras.layers.Dense(units=10, activation='softmax')
])
print(model.summary())

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
model.fit(x_train, y_train, batch_size=128, epochs=10, verbose=1)

test_loss, test_acc = model.evaluate(x_test, y_test, verbose=0)
print(f'test_loss:{test_loss:.4f}, test_acc:{test_acc:.4f}')

pred = model.predict(x_test)
print(pred[0])
print('예측값 : ', np.argmax(pred[0]))
print('실제값 : ', y_test[0])

# 각 이미지 출력용 함수(예측 이미지와 실제 레이블 비교)
def plot_image(i, pred_arr, y_true, x_img):
    pred_arr = pred[i]
    true_label = y_true[i]
    img = x_img[i]
    pred_label = np.argmax(pred_arr)
    pred_percent = 100 * np.max(pred_arr)
    color='blue' if pred_label == true_label else 'red'
    plt.xticks([])
    plt.yticks([])
    plt.imshow(img, cmap='gray')
    plt.xlabel(
        f'예측:{class_names[pred_label]} {pred_percent:.0f}%\n'
        f'실제:{class_names[true_label]}', color=color
    )


# 각 이미지에 라벨 등의 정보 표시
def plot_values_arr(i, pred, y_true):
    pred_arr = pred[i]
    true_label = y_true[i]
    pred_label = np.argmax(pred_arr)

    plt.xticks(range(10), class_names, rotation=45, ha='right')
    plt.yticks([])
    plt.ylim([0, 1])
    bars = plt.bar(range(10), pred_arr)
    bars[pred_label].set_color('red')       # 예측값
    bars[true_label].set_color('blue')      # 실제값



def show_one_prediction(i, pred, y_true, x_img):
    plt.figure(figsize=(7, 3))

    plt.subplot(1, 2, 1)
    plot_image(i, pred, y_true, x_img)

    plt.subplot(1, 2, 2)
    plot_values_arr(i, pred, y_true)

    plt.tight_layout()
    plt.show()


show_one_prediction(0, pred, y_test, x_test) # 1개 이미지

# 여러 이미지 보기 3 * 3 출력
def show_prediction_grid(start, pred, y_true, x_img, rows=3, cols=3):
    plt.figure(figsize=(9,9))

    for n in range(rows * cols):
        i = start + n

        plt.subplot(rows, cols, n + 1)
        pred_label = np.argmax(pred[i])
        true_label = y_true[i]
        pred_percent = 100 * np.max(pred[i])

        color='blue' if pred_label == true_label else 'red'
        plt.xticks([])
        plt.yticks([])
        plt.imshow(x_img[i], cmap='gray')
        plt.xlabel(
            f'예측:{class_names[pred_label]} {pred_percent:.0f}%\n'
            f'실제:{class_names[true_label]}', color=color
        )
    
    plt.tight_layout()
    plt.show()

# 0번부터 9개 보기
show_prediction_grid(0, pred, y_test, x_test)

# 15번부터 9개 보기
show_prediction_grid(15, pred, y_test, x_test) 