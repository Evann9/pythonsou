# 데이터 전처리
import pandas as pd
import numpy as np
# data_raw.csv : 비행 log 데이터
# train_data_raw.csv : 학습 데이터 (오차 미반영)
# train_data.csv : 최종 학습 데이터 (오차 반영)
# test_data.csv : 최종 검증 데이터

# train_data.csv, test_data.csv 사용하여 학습 진행
# train_data.csv standardscaler로 사용할 것

# case기준 train / test split 기준
# 1. 2D이동거리(m) 분포 균일
# 2. 풍속(m/s) 분포 균일
# 3. 총회전량(deg) 분포 균일
# 4. 비행고도(m) 분포 균일
train = [   # train case info
    "case002","case003","case004","case005","case006","case007",
    "case008","case009","case010","case011","case012","case013",
    "case014","case016","case018","case019","case020","case021",
    "case024","case025","case028",
]

test = [    # test case info
    "case001","case015","case017","case022","case023",
    "case026","case027","case029","case030",
]

np.random.seed(4)

col = ["케이스ID", "풍속(m/s)","비행고도(m)","2D이동거리(m)", "회전각도(deg)","웨이포인트회전횟수","시뮬레이션전체시간(s)","배터리소모율(%)"]
df = pd.read_csv("data_raw.csv", usecols=col)

# case별 train / test 분리
df_train = df[df["케이스ID"].isin(train)]
df_test = df[df["케이스ID"].isin(test)]

# 총회전량(deg) = 회전각도(deg) * 웨이포인트회전횟수 열 추가
df_train["총회전량(deg)"] = df_train["회전각도(deg)"] * df_train["웨이포인트회전횟수"]
df_test["총회전량(deg)"] = df_test["회전각도(deg)"] * df_test["웨이포인트회전횟수"]

# "회전각도(deg)", "웨이포인트회전횟수" 열 제거
df_train = df_train.drop(["회전각도(deg)", "웨이포인트회전횟수"], axis=1)
df_test = df_test.drop(["회전각도(deg)", "웨이포인트회전횟수"], axis=1)

# 시뮬레이션상 시뮬레이션전체시간(s) 오차 반영
df_train['시뮬레이션전체시간(s)'] = df_train['시뮬레이션전체시간(s)'] - 60
df_test['시뮬레이션전체시간(s)'] = df_test['시뮬레이션전체시간(s)'] - 60

# csv 저장
df_train.to_csv("train_data_raw.csv", index=False, encoding="utf-8-sig")
df_test.to_csv("test_data.csv", index=False, encoding="utf-8-sig")

# 배터리 소모량에 오차 ±2% 반영
aug = []
for _ in range(10):         # case별 10개 sample
    temp = df_train.copy()

    # ±2% 범위 내에서 random하게 오차반영
    noise = np.random.uniform(0.98, 1.02, size=len(temp))
    temp["배터리소모율(%)"] = (temp["배터리소모율(%)"] * noise).round(2)

    aug.append(temp)

train_aug = pd.concat(aug).reset_index(drop=True)
train_aug = train_aug.sort_values(by="케이스ID").reset_index(drop=True)
train_aug.to_csv("train_data.csv", index=False, encoding="utf-8-sig")

print("2% 오차 반영 : ", len(df_train), "→", len(train_aug))