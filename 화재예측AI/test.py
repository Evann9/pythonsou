import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from xgboost import XGBClassifier, XGBRegressor
from sklearn.metrics import (
    accuracy_score, f1_score,
    mean_squared_error, r2_score,
    confusion_matrix, ConfusionMatrixDisplay
)

# ================================================================
# 경로 설정
# ================================================================
TRAIN_PATH = r'C:\work\projects\team_project\train'
TEST_PATH  = r'C:\work\projects\team_project\test'

# ================================================================
# 데이터 로드
# ================================================================
def load_data(path):
    dfs = []
    for file in os.listdir(path):
        df = pd.read_csv(os.path.join(path, file))
        df['country'] = file
        dfs.append(df)
    return pd.concat(dfs, ignore_index=True)

train = load_data(TRAIN_PATH)
test  = load_data(TEST_PATH)

print(f'train : {train.shape}')
print(f'test  : {test.shape}')

# ================================================================
# 전처리
# ================================================================
def get_conf_level(c):
    if c <= 30:   return 0  # 저신뢰
    elif c <= 65: return 1  # 중신뢰
    else:         return 2  # 고신뢰

def get_country_code(name):
    if 'Korea' in name: return 0
    if 'Japan' in name: return 1
    return 2  # China

def preprocess(df):
    df = df.copy()

    # 날짜 분리
    df['acq_date'] = pd.to_datetime(df['acq_date'])
    df['month']    = df['acq_date'].dt.month
    df['day']      = df['acq_date'].dt.day

    # 범주형 → 숫자
    df['satellite']    = (df['satellite'] == 'Aqua').astype(int)
    df['daynight']     = (df['daynight']  == 'D').astype(int)
    df['country_code'] = df['country'].apply(get_country_code)

    # 타겟 생성
    df['conf_level'] = df['confidence'].apply(get_conf_level)

    return df

train = preprocess(train)
test  = preprocess(test)

# ================================================================
# 피처 / 타겟 분리
# ================================================================
FEATURES = [
    'latitude', 'longitude',
    'brightness', 'scan', 'track',
    'bright_t31', 'satellite',
    'daynight', 'month', 'day',
    'country_code'
]

X_train = train[FEATURES]
X_test  = test[FEATURES]

y_cls_train = train['conf_level']
y_cls_test  = test['conf_level']
y_reg_train = train['frp']
y_reg_test  = test['frp']

# 정규화
scaler  = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test  = scaler.transform(X_test)

# ================================================================
# 모델 정의
# ================================================================
cls_models = {
    '로지스틱 회귀' : LogisticRegression(max_iter=1000),
    'Random Forest' : RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost'       : XGBClassifier(random_state=42, eval_metric='mlogloss')
}

reg_models = {
    '선형 회귀'     : LinearRegression(),
    'Random Forest' : RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost'       : XGBRegressor(random_state=42)
}

# ================================================================
# 모델 학습 및 평가
# ================================================================
def train_cls(models, X_train, y_train, X_test, y_test):
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'model'    : model,
            'y_pred'   : y_pred,
            'accuracy' : accuracy_score(y_test, y_pred),
            'f1'       : f1_score(y_test, y_pred, average='macro')
        }
        print(f'{name} → 정확도 {results[name]["accuracy"]:.4f} | F1 {results[name]["f1"]:.4f}')
    return results

def train_reg(models, X_train, y_train, X_test, y_test):
    results = {}
    for name, model in models.items():
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        results[name] = {
            'model'  : model,
            'y_pred' : y_pred,
            'rmse'   : np.sqrt(mean_squared_error(y_test, y_pred)),
            'r2'     : r2_score(y_test, y_pred)
        }
        print(f'{name} → RMSE {results[name]["rmse"]:.4f} | R² {results[name]["r2"]:.4f}')
    return results

print('\n===== 분류 =====')
cls_results = train_cls(cls_models, X_train, y_cls_train, X_test, y_cls_test)

print('\n===== 회귀 =====')
reg_results = train_reg(reg_models, X_train, y_reg_train, X_test, y_reg_test)


# 실제값 vs 예측값 비교 테이블
print('\n===== 분류 : 실제 vs 예측 (상위 20개) =====')
cls_compare = pd.DataFrame({
    '실제값' : y_cls_test.values[:20],
    'XGBoost 예측' : cls_results['XGBoost']['y_pred'][:20]
})
cls_compare['실제값(라벨)']   = cls_compare['실제값'].map({0:'저신뢰', 1:'중신뢰', 2:'고신뢰'})
cls_compare['예측값(라벨)']   = cls_compare['XGBoost 예측'].map({0:'저신뢰', 1:'중신뢰', 2:'고신뢰'})
cls_compare['정답여부']       = cls_compare['실제값'] == cls_compare['XGBoost 예측']
cls_compare['정답여부']       = cls_compare['정답여부'].map({True:'✅', False:'❌'})
print(cls_compare[['실제값(라벨)', '예측값(라벨)', '정답여부']].to_string(index=False))

print('\n===== 회귀 : 실제 vs 예측 (상위 20개) =====')
reg_compare = pd.DataFrame({
    '실제 FRP'       : y_reg_test.values[:20],
    'RF 예측 FRP'    : reg_results['Random Forest']['y_pred'][:20].round(2),
})
reg_compare['차이'] = (reg_compare['실제 FRP'] - reg_compare['RF 예측 FRP']).abs().round(2)
print(reg_compare.to_string(index=False))


# ================================================================
# 시각화
# ================================================================
def save(filename):
    plt.tight_layout()
    plt.savefig(filename, dpi=150)
    plt.show()

# 01 데이터 분포
fig, axes = plt.subplots(1, 2, figsize=(12, 4))

counts = train['conf_level'].value_counts().sort_index()
axes[0].bar(['저신뢰', '중신뢰', '고신뢰'], counts.values,
            color=['#4CAF50', '#FFC107', '#F44336'])
axes[0].set_title('화재 신뢰도 분포 (train)')
axes[0].set_xlabel('신뢰도 등급')
axes[0].set_ylabel('데이터 수')
for i, v in enumerate(counts.values):
    axes[0].text(i, v + 100, str(v), ha='center')

country_counts = train['country_code'].value_counts().sort_index()
axes[1].bar(['한국', '일본', '중국'], country_counts.values,
            color=['#2196F3', '#FF5722', '#9C27B0'])
axes[1].set_title('국가별 데이터 수 (train)')
axes[1].set_xlabel('국가')
axes[1].set_ylabel('데이터 수')
for i, v in enumerate(country_counts.values):
    axes[1].text(i, v + 100, str(v), ha='center')

save('01_data_distribution.png')

# 02 분류 성능
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
names     = list(cls_results.keys())
accuracys = [cls_results[n]['accuracy'] for n in names]
f1s       = [cls_results[n]['f1']       for n in names]

axes[0].bar(names, accuracys, color=['#64B5F6', '#42A5F5', '#1E88E5'])
axes[0].set_title('분류 모델 정확도 비교')
axes[0].set_ylabel('정확도')
axes[0].set_ylim(0.5, 0.85)
for i, v in enumerate(accuracys):
    axes[0].text(i, v + 0.005, f'{v:.4f}', ha='center')

axes[1].bar(names, f1s, color=['#EF9A9A', '#EF5350', '#B71C1C'])
axes[1].set_title('분류 모델 F1 비교')
axes[1].set_ylabel('F1 Score')
axes[1].set_ylim(0.3, 0.75)
for i, v in enumerate(f1s):
    axes[1].text(i, v + 0.005, f'{v:.4f}', ha='center')

save('02_classification_results.png')

# 03 회귀 성능
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
names = list(reg_results.keys())
rmses = [reg_results[n]['rmse'] for n in names]
r2s   = [reg_results[n]['r2']   for n in names]

axes[0].bar(names, rmses, color=['#A5D6A7', '#66BB6A', '#2E7D32'])
axes[0].set_title('회귀 모델 RMSE 비교 (낮을수록 좋음)')
axes[0].set_ylabel('RMSE')
for i, v in enumerate(rmses):
    axes[0].text(i, v + 0.1, f'{v:.4f}', ha='center')

axes[1].bar(names, r2s, color=['#FFE082', '#FFD54F', '#F9A825'])
axes[1].set_title('회귀 모델 R² 비교 (높을수록 좋음)')
axes[1].set_ylabel('R²')
axes[1].set_ylim(0, 1.1)
for i, v in enumerate(r2s):
    axes[1].text(i, v + 0.01, f'{v:.4f}', ha='center')

save('03_regression_results.png')

# 04 혼동행렬 (XGBoost)
fig, ax = plt.subplots(figsize=(6, 5))
cm = confusion_matrix(y_cls_test, cls_results['XGBoost']['y_pred'])
ConfusionMatrixDisplay(cm, display_labels=['저신뢰', '중신뢰', '고신뢰']).plot(
    ax=ax, cmap='Blues', colorbar=False
)
ax.set_title('XGBoost 혼동행렬')
save('04_confusion_matrix.png')

# 05 회귀 산점도 (Random Forest)
fig, ax = plt.subplots(figsize=(7, 5))
idx = np.random.choice(len(y_reg_test), 500, replace=False)
ax.scatter(y_reg_test.iloc[idx], reg_results['Random Forest']['y_pred'][idx],
           alpha=0.4, color='steelblue', s=20)
max_val = max(y_reg_test.max(), reg_results['Random Forest']['y_pred'].max())
ax.plot([0, max_val], [0, max_val], 'r--', label='완벽한 예측')
ax.set_xlabel('실제 FRP')
ax.set_ylabel('예측 FRP')
ax.set_title('Random Forest : 실제 vs 예측 (화재 강도)')
ax.legend()
save('05_regression_scatter.png')

# 06 변수 중요도
fig, ax = plt.subplots(figsize=(8, 5))
importances = cls_results['Random Forest']['model'].feature_importances_
idx         = np.argsort(importances)[::-1]
ax.bar([FEATURES[i] for i in idx], importances[idx], color='steelblue')
ax.set_title('Random Forest 변수 중요도 (분류)')
ax.set_xlabel('피처')
ax.set_ylabel('중요도')
plt.xticks(rotation=45, ha='right')
save('06_feature_importance.png')

print('\n✅ 완료!')