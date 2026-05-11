import numpy as np
import matplotlib.pyplot as plt
import joblib
import pandas as pd

# ============================================================
# PLOT_SVR.py
# - 이동거리(distance)가 0이면 x축은 고도(Altitude)
# - 이동거리(distance)가 0이 아니면 x축은 이동거리(Distance)
# - 웹페이지 그래프와 유사하게 보기 좋게 출력
# ============================================================

model = joblib.load("best_svr_model.pkl")

wind = 5           # 0 ~ 5
altitude = 10      # 10 ~ 200
rotation = 0       # 0 ~ 720
distance = 0       # 0이면 고도축, 0보다 크면 이동거리축


def make_input_dataframe(x_vals, wind, altitude, rotation, distance):
    if distance == 0:
        return pd.DataFrame({
            "풍속(m/s)": [wind] * len(x_vals),
            "비행고도(m)": x_vals,
            "2D이동거리(m)": [0] * len(x_vals),
            "총회전량(deg)": [rotation] * len(x_vals)
        })

    return pd.DataFrame({
        "풍속(m/s)": [wind] * len(x_vals),
        "비행고도(m)": [altitude] * len(x_vals),
        "2D이동거리(m)": x_vals,
        "총회전량(deg)": [rotation] * len(x_vals)
    })


# =========================
# x-axis logic
# =========================
if distance == 0:
    x_vals = np.linspace(0.1, altitude, 20)
    x_label = "Altitude (m)"
else:
    x_vals = np.linspace(0.1, distance, 20)
    x_label = "Distance (m)"

df_input = make_input_dataframe(x_vals, wind, altitude, rotation, distance)

pred = model.predict(df_input)
pred = np.clip(pred, 0, 100)
battery = np.clip(100 - pred, 0, 100)

# =========================
# cutoff logic
# =========================
idx = np.where(battery <= 0)[0]
if len(idx) > 0:
    cut = idx[0] + 2
    x_vals = x_vals[:cut]
    battery = battery[:cut]

# =========================
# Clean web-style plot
# =========================
fig, ax = plt.subplots(figsize=(10, 5.2))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# risk bands
ax.axhspan(25, 30, color="#facc15", alpha=0.14, linewidth=0)
ax.axhspan(15, 20, color="#fb923c", alpha=0.14, linewidth=0)
ax.axhspan(5, 10, color="#ef4444", alpha=0.14, linewidth=0)

# line
ax.plot(
    x_vals,
    battery,
    color="#16a34a",
    linewidth=3,
    marker="o",
    markersize=5,
    markerfacecolor="#16a34a",
    markeredgecolor="#16a34a"
)

# final annotation
if len(x_vals) > 0:
    ax.annotate(
        f"{battery[-1]:.1f}%",
        xy=(x_vals[-1], battery[-1]),
        xytext=(8, 8),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color="#0f172a"
    )

# labels on bands
left_x = x_vals[0] + (x_vals[-1] - x_vals[0]) * 0.02 if len(x_vals) > 1 else 0
ax.text(left_x, 27.2, "WARNING", fontsize=10, color="#ca8a04", weight="bold")
ax.text(left_x, 17.2, "RTL", fontsize=10, color="#ea580c", weight="bold")
ax.text(left_x, 7.2, "CRITICAL", fontsize=10, color="#dc2626", weight="bold")

# axis style
ax.set_title("Battery Remaining Prediction", fontsize=16, weight="bold", pad=12)
ax.set_xlabel(x_label, fontsize=12)
ax.set_ylabel("Battery (%)", fontsize=12)

ax.set_ylim(0, 100)
ax.set_xlim(left=0)

ax.grid(axis="y", color="#e2e8f0", linewidth=1)
ax.grid(axis="x", color="#f1f5f9", linewidth=0.8)

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#cbd5e1")
ax.spines["bottom"].set_color("#cbd5e1")

ax.tick_params(axis="both", colors="#64748b")

plt.tight_layout()
plt.show()
