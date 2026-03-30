from pathlib import Path
import pandas as pd
import scipy.stats as stats
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import koreanize_matplotlib

BRAND_ORDER = ['스타벅스','폴바셋','이디야','탐앤탐스']

def analysis_func(rdata:list[dict]):
    df = pd.DataFrame(rdata)
    
    if df.empty:
        return pd.DataFrame(), '데이터가 없어요', pd.DataFrame()
    
    df = df.dropna(subset=['gender','co_survey'])

    # 성별 브랜드별 선호 빈도수
    crossTab = pd.crosstab(index=df['gender'], columns=df['co_survey'])

    if crossTab.size == 0 or crossTab.shape[0] < 2 or crossTab.shape[1] < 2:
        return crossTab, '표본자료가 부족해 카이제곱 검정 수행 불가', df
    
    # 유의수준 : 0.05 (5%)
    alpha = 0.05
    # 카이제곱 검정 수행
    chi2, p, dof, expected = stats.chi2_contingency(crossTab)
    
    min_expected = expected.min()
    note =""
    if min_expected < 5:
        note = f"<br><small>* 주의 : 기대빈도 최소값 {min_expected:.2f} (5 미만)</small>"
    
    if p >= alpha:
        results = f"p값  {p:.5f} >= {alpha} : 성별에 따라 커피 선호 브랜드는 <b>차이가 없다(귀무가설)</b> {note}"
    else:
        results = f"p값  {p:.5f} < {alpha} : 성별에 따라 커피 선호 브랜드는 <b>차이가 있다(대립가설)</b> {note}"

    return crossTab, results, df

def save_barchart_func(df:pd.DataFrame, out_path:Path) -> bool:  # :pd.DataFrame 타입 힌트
    if df is None or df.empty or "co_survey" not in df.columns:
        return False
    
    counts = df['co_survey'].value_counts().reindex(BRAND_ORDER, fill_value=0)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    
    fig = plt.figure()
    ax = counts.plot(kind='bar', width=0.6, edgecolor="black")
    ax.set_xlabel("커피 브랜드")
    ax.set_ylabel("선호 건수")
    ax.set_title("커피 브랜드별 선호 건수")
    ax.set_xticklabels(BRAND_ORDER, rotation=0)
    fig.tight_layout()
    fig.savefig(str(out_path), dpi=120, bbox_inches="tight")
    plt.close(fig)  # 메모리 누수 방지

    return True