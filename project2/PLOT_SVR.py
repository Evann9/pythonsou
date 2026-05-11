import numpy as np
import matplotlib.pyplot as plt
import joblib
import pandas as pd

model = joblib.load("best_svr_model.pkl")

wind = 1            # 0 ~ 5
altitude = 10       # 10 ~ 200
rotation = 720        # 0 ~ 720 waypoint를 4개로 제한
distance = 0.1        #  0보단 큰 값으로, 0이면 못 그림

x_vals = np.linspace(0, distance, 20)

df_input = pd.DataFrame({
    "풍속(m/s)": [wind] * len(x_vals),
    "비행고도(m)": [altitude] * len(x_vals),
    "2D이동거리(m)": x_vals,
    "총회전량(deg)": [rotation] * len(x_vals)
})

pred = model.predict(df_input)
pred = np.clip(pred, 0, 100)        # 배터리 소모량 0 ~ 100으로 출력

battery = 100 - pred

# =========================
# cutoff logic (핵심)
# =========================
idx = np.where(battery <= 0)[0]

if len(idx) > 0:
    cut = idx[0] + 2
    x_vals = x_vals[:cut]
    battery = battery[:cut]

# =========================
# plot
# =========================
plt.figure(figsize=(8,6))

plt.plot(x_vals, battery, c='green', marker="o")

plt.axhspan(25, 30, facecolor="white", alpha=0.25, hatch="//", edgecolor="yellow")
plt.axhspan(15, 20, facecolor="white", alpha=0.25, hatch="//", edgecolor="orange")
plt.axhspan(5, 10, facecolor="white", alpha=0.25, hatch="//", edgecolor="red")

bbox=dict(facecolor="white", alpha=0.5, edgecolor="none")

left_x = x_vals[0] + (x_vals[-1] - x_vals[0]) * 0.02 

plt.text(left_x, 27.5, "WARNING",
         ha="left", va="center",
         fontsize=14, color="#F1C40F",
         fontweight="bold",
         bbox=dict(facecolor="white", alpha=0.4, edgecolor="none"))

plt.text(left_x, 17.5, "RTL",
         ha="left", va="center",
         fontsize=14, color="#E67E22",
         fontweight="bold",
         bbox=dict(facecolor="white", alpha=0.4, edgecolor="none"))

plt.text(left_x, 7.5, "CRITICAL",
         ha="left", va="center",
         fontsize=14, color="#E74C3C",
         fontweight="bold",
         bbox=dict(facecolor="white", alpha=0.4, edgecolor="none"))

plt.xlim(left=0)
plt.ylim(bottom=0)

plt.xlabel("Distance (m)")
plt.ylabel("Battery (%)")
plt.title("Battery Curve")

plt.show()