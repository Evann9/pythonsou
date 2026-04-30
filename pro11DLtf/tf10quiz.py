# 자전거 공유 시스템 분석용 데이터 train.csv를 이용하여 대여횟수에 영향을 주는 변수들을 골라 다중선형회귀분석 모델을 작성하시오.
# 모델 학습시에 발생하는 loss를 시각화하고 설명력을 출력하시오.
# 새로운 데이터를 input 함수를 사용해 키보드로 입력하여 대여횟수 예측결과를 콘솔로 출력하시오.

# https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv

import os

# TensorFlow 실행 시 나오는 안내성 로그를 줄인다.
# TF_CPP_MIN_LOG_LEVEL = "2"는 INFO, WARNING 로그를 대부분 숨긴다.
# TF_ENABLE_ONEDNN_OPTS = "0"은 oneDNN 관련 안내 문구를 줄이고 결과 재현성을 조금 더 안정적으로 만든다.
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import Dense, Input
from tensorflow.keras.models import Sequential
from tensorflow.keras.optimizers import Adam
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


def add_datetime_features(df):
    """datetime 컬럼에서 회귀분석용 시간 변수를 만든다.

    원본 datetime은 "2011-01-01 00:00:00"처럼 문자열 형태라서
    그대로는 신경망/회귀모델의 입력 변수로 사용하기 어렵다.
    그래서 연, 월, 일, 시간, 요일처럼 숫자형 변수로 분해해서 사용한다.
    자전거 대여량은 특히 시간대(hour), 요일(weekday), 계절(season)의 영향을 많이 받는다.
    """
    result = df.copy()

    # 문자열을 pandas 날짜 타입으로 변환해야 dt.year, dt.hour 같은 속성을 사용할 수 있다.
    result["datetime"] = pd.to_datetime(result["datetime"])

    # 날짜에서 의미 있는 시간 관련 변수를 추출한다.
    # weekday는 월요일=0, 화요일=1, ..., 일요일=6 으로 만들어진다.
    result["year"] = result["datetime"].dt.year
    result["month"] = result["datetime"].dt.month
    result["day"] = result["datetime"].dt.day
    result["hour"] = result["datetime"].dt.hour
    result["weekday"] = result["datetime"].dt.weekday
    return result


def make_x(df, dummy_columns=None):
    """입력 변수 X를 만든다.

    base_cols에 있는 변수만 선택한 뒤, 범주형 변수는 one-hot encoding 한다.
    학습 데이터와 새 입력 데이터는 반드시 컬럼 개수와 순서가 같아야 하므로
    새 데이터 예측 시에는 dummy_columns를 이용해 학습 때의 컬럼 순서에 맞춘다.
    """
    # 모델에 넣을 입력 변수만 선택한다.
    x = df[base_cols].copy()

    # season, weather, hour 같은 숫자는 크고 작음의 의미가 약한 범주형 변수다.
    # 예를 들어 season=4가 season=1보다 4배 크다는 뜻이 아니므로 one-hot 처리한다.
    # drop_first=True는 더미 변수 간 완전 중복을 하나 줄이기 위한 옵션이다.
    x = pd.get_dummies(x, columns=category_cols, drop_first=True, dtype=float)

    if dummy_columns is not None:
        # 새 데이터에는 특정 범주가 없어서 더미 컬럼이 일부 안 생길 수 있다.
        # reindex로 학습 데이터의 컬럼과 똑같이 맞추고, 없는 컬럼은 0으로 채운다.
        x = x.reindex(columns=dummy_columns, fill_value=0)

    return x


def input_int(message, min_value=None, max_value=None):
    """정수 입력을 받을 때 범위 검사까지 처리한다."""
    while True:
        try:
            value = int(input(message))
            if min_value is not None and value < min_value:
                print(f"{min_value} 이상으로 입력하세요.")
                continue
            if max_value is not None and value > max_value:
                print(f"{max_value} 이하로 입력하세요.")
                continue
            return value
        except ValueError:
            print("정수를 입력하세요.")


def input_float(message, min_value=None, max_value=None):
    """실수 입력을 받을 때 범위 검사까지 처리한다."""
    while True:
        try:
            value = float(input(message))
            if min_value is not None and value < min_value:
                print(f"{min_value} 이상으로 입력하세요.")
                continue
            if max_value is not None and value > max_value:
                print(f"{max_value} 이하로 입력하세요.")
                continue
            return value
        except ValueError:
            print("숫자를 입력하세요.")


def input_datetime(message):
    """날짜/시간 문자열을 입력받아 pandas Timestamp로 변환한다."""
    while True:
        # lstrip("\ufeff")는 일부 콘솔/파일 입력에서 앞에 붙는 BOM 문자를 제거한다.
        value = input(message).strip().lstrip("\ufeff")

        # errors="coerce"는 변환 실패 시 예외 대신 NaT 값을 만든다.
        dt = pd.to_datetime(value, errors="coerce")
        if pd.isna(dt):
            print("예: 2012-07-15 17:00:00 형식으로 입력하세요.")
            continue
        return dt


def make_new_data_from_keyboard():
    """키보드로 새 조건을 입력받아 예측용 DataFrame을 만든다."""
    print("\n새로운 자전거 대여 조건을 입력하세요.")
    dt = input_datetime("날짜와 시간(예: 2012-07-15 17:00:00): ")

    # 학습에 사용한 base_cols와 같은 이름, 같은 의미의 값을 입력받아야 한다.
    # 사용자가 datetime을 입력하면 year/month/day/hour/weekday는 자동으로 계산한다.
    row = {
        "season": input_int("계절 season(1:봄, 2:여름, 3:가을, 4:겨울): ", 1, 4),
        "holiday": input_int("공휴일 holiday(0:아님, 1:맞음): ", 0, 1),
        "workingday": input_int("근무일 workingday(0:아님, 1:맞음): ", 0, 1),
        "weather": input_int("날씨 weather(1:좋음, 2:보통, 3:나쁨, 4:매우 나쁨): ", 1, 4),
        "temp": input_float("온도 temp: "),
        "atemp": input_float("체감온도 atemp: "),
        "humidity": input_float("습도 humidity(0~100): ", 0, 100),
        "windspeed": input_float("풍속 windspeed: ", 0),
        "year": dt.year,
        "month": dt.month,
        "day": dt.day,
        "hour": dt.hour,
        "weekday": dt.weekday(),
    }

    # DataFrame으로 만들어야 make_x 함수에서 학습 데이터와 같은 전처리를 적용할 수 있다.
    return pd.DataFrame([row], columns=base_cols)


# 난수 seed를 고정하면 실행할 때마다 결과가 크게 달라지는 것을 줄일 수 있다.
# 완전히 같은 결과가 보장되는 것은 아니지만, 학습 결과 비교가 쉬워진다.
tf.random.set_seed(123)
np.random.seed(123)

# 데이터 읽기
url = "https://raw.githubusercontent.com/pykwon/python/refs/heads/master/data/train.csv"
data = pd.read_csv(url)

# datetime 문자열을 모델에서 사용할 수 있는 시간 관련 숫자 변수로 변환한다.
data = add_datetime_features(data)

print(data.head())
print(data.shape)

# 사용할 입력 변수 목록
#
# casual + registered = count 이므로 예측 변수에서 제외한다.
# 만약 casual과 registered를 넣으면 정답 count의 구성 요소를 입력으로 주는 것이므로
# 설명력이 비정상적으로 높아지는 데이터 누수(data leakage)가 발생한다.
#
# datetime은 year/month/day/hour/weekday로 변환해서 사용한다.
base_cols = [
    "season",
    "holiday",
    "workingday",
    "weather",
    "temp",
    "atemp",
    "humidity",
    "windspeed",
    "year",
    "month",
    "day",
    "hour",
    "weekday",
]

# 숫자로 저장되어 있지만 실제 의미는 범주에 가까운 변수들이다.
# 예: weather=3이 weather=1보다 정확히 3배 나쁘다는 뜻은 아니다.
# 이런 변수는 선형회귀에서 잘못된 순서/거리 의미를 주지 않도록 one-hot 처리한다.
category_cols = [
    "season",
    "holiday",
    "workingday",
    "weather",
    "year",
    "month",
    "hour",
    "weekday",
]

# x_data: 모델 입력값
# y_data: 정답값, 즉 자전거 대여횟수 count
x_data = make_x(data)
y_data = data[["count"]].values

print("\n사용한 입력 변수")
print(base_cols)
print("one-hot 처리 후 입력 변수 수:", x_data.shape[1])

# train/test 분리
#
# train 데이터는 모델 학습에 사용하고, test 데이터는 학습에 쓰지 않은 데이터로 성능을 확인한다.
# test_size=0.3 이므로 전체 데이터 중 30%를 테스트용으로 사용한다.
# random_state를 고정하면 매번 같은 방식으로 데이터가 나뉜다.
x_train, x_test, y_train, y_test = train_test_split(
    x_data.values,
    y_data,
    test_size=0.3,
    random_state=123,
    shuffle=True,
)

# MinMaxScaler는 각 값을 0~1 범위로 맞춰준다.
# 입력 변수마다 단위가 다르다. 예를 들어 temp, humidity, windspeed는 값의 범위가 서로 다르다.
# 스케일을 맞추면 optimizer가 더 안정적으로 학습한다.
x_scaler = MinMaxScaler()
y_scaler = MinMaxScaler()

# scaler는 반드시 train 데이터로만 fit 한다.
# test 데이터까지 fit에 사용하면 test 정보가 학습 과정에 새는 문제가 생긴다.
x_train_scaled = x_scaler.fit_transform(x_train)
x_test_scaled = x_scaler.transform(x_test)

# y도 정규화해서 학습한다.
# count는 값의 범위가 넓어서 그대로 학습하면 loss가 커지고 학습이 불안정할 수 있다.
# 단, 최종 R2와 예측 결과는 원래 count 단위로 보기 위해 inverse_transform 한다.
y_train_scaled = y_scaler.fit_transform(y_train)
y_test_scaled = y_scaler.transform(y_test)

print("\ntrain/test shape")
print(x_train_scaled.shape, x_test_scaled.shape, y_train_scaled.shape, y_test_scaled.shape)

# 다중선형회귀 모델
#
# 입력 변수는 여러 개이고 출력은 대여횟수 1개다.
# Dense(1, activation="linear")는 다음과 같은 선형식을 학습하는 것과 같다.
# count = w1*x1 + w2*x2 + ... + wn*xn + b
# 은닉층을 추가하면 비선형 신경망 회귀가 되므로, "다중선형회귀" 과제 의도에 맞게 출력층 하나만 둔다.
model = Sequential()
model.add(Input(shape=(x_train_scaled.shape[1],)))
model.add(Dense(units=1, activation="linear"))
model.summary()

# optimizer는 가중치를 조금씩 수정하는 알고리즘이다.
# loss="mse"는 실제 대여횟수와 예측 대여횟수 차이의 제곱 평균을 최소화한다.
model.compile(
    optimizer=Adam(learning_rate=0.005),
    loss="mse",
    metrics=["mse"],
)

# validation_split=0.2는 train 데이터 중 20%를 검증용으로 떼어 학습 중 성능을 확인한다.
# history에는 epoch별 train loss와 validation loss가 저장되어 아래에서 그래프로 그린다.
history = model.fit(
    x_train_scaled,
    y_train_scaled,
    epochs=200,
    batch_size=32,
    verbose=0,
    validation_split=0.2,
)

print("\n학습 완료")

# 학습에 사용하지 않은 test 데이터로 최종 loss를 확인한다.
ev_loss = model.evaluate(x_test_scaled, y_test_scaled, verbose=0)
print("\nevaluate loss, mse:", ev_loss)

# predict 결과는 y를 0~1로 정규화한 스케일이므로 아직 실제 대여횟수가 아니다.
train_pred_scaled = model.predict(x_train_scaled, verbose=0)
test_pred_scaled = model.predict(x_test_scaled, verbose=0)

# inverse_transform으로 원래 count 단위로 되돌린다.
train_pred = y_scaler.inverse_transform(train_pred_scaled)
test_pred = y_scaler.inverse_transform(test_pred_scaled)

# R2 score는 설명력 또는 결정계수라고 부른다.
# 1에 가까울수록 실제값을 잘 설명하고, 0이면 평균값만 예측하는 수준이다.
# train R2와 test R2 차이가 너무 크면 과적합을 의심할 수 있다.
print("train 설명력(R2):", r2_score(y_train, train_pred))
print("test 설명력(R2):", r2_score(y_test, test_pred))

# epoch가 진행되면서 loss가 어떻게 변했는지 시각화한다.
# train_loss와 val_loss가 함께 감소하면 학습이 잘 진행된 것이다.
# train_loss만 감소하고 val_loss가 증가하면 과적합 가능성이 있다.
plt.figure(figsize=(10, 6))
plt.plot(history.history["loss"], label="train_loss")
plt.plot(history.history["val_loss"], label="val_loss")
plt.title("Bike Sharing Regression Loss")
plt.xlabel("Epoch")
plt.ylabel("MSE")
plt.legend()
plt.grid()
plt.show()

# 새 데이터 입력 및 예측
#
# 사용자가 입력한 값도 학습 데이터와 완전히 같은 전처리를 거쳐야 한다.
# 순서: 키보드 입력 -> DataFrame 생성 -> one-hot 컬럼 맞춤 -> x_scaler 변환 -> model.predict
new_data = make_new_data_from_keyboard()
new_x = make_x(new_data, dummy_columns=x_data.columns)
new_x_scaled = x_scaler.transform(new_x.values)

# 예측값은 정규화된 y 스케일이므로 다시 count 단위로 복원한다.
new_pred_scaled = model.predict(new_x_scaled, verbose=0)
new_pred = y_scaler.inverse_transform(new_pred_scaled)

print("\n입력 데이터")
print(new_data)

# 선형회귀 특성상 예측값이 아주 드물게 음수가 될 수 있다.
# 대여횟수는 음수가 될 수 없으므로 출력할 때만 0 이상으로 보정한다.
print(f"예상 대여횟수: {max(0, new_pred[0, 0]):.0f}대")
