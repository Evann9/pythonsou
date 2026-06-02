# 개념 이해를 위한 "실시간 LiDAR 애니메이션" 예제
# 보여주는 내용:
#   1) 자동차가 도시를 주행
#   2) LiDAR가 회전하며 스캔
#   3) 레이저가 건물/차량/보행자에 반사
#   4) 점군(Point Cloud)이 실시간으로 누적
#   5) 움직이는 객체도 계속 업데이트

# 특징: 실행만 하면 바로 움직임, matplotlib 사용

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D


# 1. 도시 환경
buildings = [
    (-20, -10, 25, 35, 0, 20),
    (10, 20, 45, 55, 0, 25),
    (-15, -5, 70, 80, 0, 18),
]


# 2. 움직이는 객체
def moving_car(frame):
    return np.array([
        7,
        frame * 0.8 + 20,
        1.5
    ])

def pedestrian(frame):
    return np.array([
        -5 + np.sin(frame * 0.2) * 2,
        frame * 0.5 + 25,
        1
    ])


# 3. LiDAR 스캔
def lidar_scan(car_pos, frame):
    points = []
    other_car = moving_car(frame)
    ped = pedestrian(frame)

    # 전방 스캔만 수행
    horizontal_angles = np.linspace(-35, 35, 120)
    vertical_angles = np.linspace(-12, 12, 6)
    max_distance = 60

    # 레이저 발사
    for h_deg in horizontal_angles:
        for v_deg in vertical_angles:
            h = np.radians(h_deg)
            v = np.radians(v_deg)

            # 방향 벡터 : 차량 전방(+Y) 기준
            dx = np.sin(h) * np.cos(v)
            dy = np.cos(h) * np.cos(v)
            dz = np.sin(v)

            # 레이저 진행
            for d in np.linspace(0, max_distance, 250):
                x = car_pos[0] + dx * d
                y = car_pos[1] + dy * d
                z = car_pos[2] + dz * d

                hit = False

                # 건물 충돌
                for b in buildings:
                    xmin, xmax, ymin, ymax, zmin, zmax = b
                    inside = (
                        xmin <= x <= xmax and ymin <= y <= ymax and zmin <= z <= zmax
                    )

                    if inside:
                        points.append([x, y, z])
                        hit = True
                        break

                if hit: break

                # 움직이는 자동차 충돌
                car_size = np.array([2, 4, 2])

                if np.all( np.abs([x, y, z] - other_car) <= car_size ):
                    points.append([x, y, z])
                    break

                # 보행자 충돌
                ped_size = np.array([0.5, 0.5, 1.7])

                if np.all( np.abs([x, y, z] - ped) <= ped_size ):
                    points.append([x, y, z])
                    break

    return np.array(points), other_car, ped

# 4. Figure 생성
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(111, projection='3d')

# 자율주행 차량
ego_car = np.array([0, 0, 2])

# 전체 point cloud 저장
global_cloud = []

# 5. 애니메이션 업데이트
def update(frame):
    global global_cloud
    ax.clear()

    # 차량 전진
    ego_car[1] = frame * 1.0

    # LiDAR 스캔
    scan_points, other_car, ped = lidar_scan(
        ego_car, frame
    )

    # Point Cloud 누적
    if len(scan_points) > 0:
        global_cloud.extend(scan_points.tolist())

    cloud = np.array(global_cloud)

    # Point Cloud 표시
    if len(cloud) > 0:
        ax.scatter(
            cloud[:, 0],
            cloud[:, 1],
            cloud[:, 2],
            s=2,
            c=cloud[:, 2],
            cmap='jet',
            alpha=0.8
        )

    # 자율주행 차량
    ax.scatter(
        ego_car[0],
        ego_car[1],
        ego_car[2],
        c='blue',
        s=180,
        label='Ego Car'
    )

    # LiDAR 위치
    ax.scatter(
        ego_car[0],
        ego_car[1],
        ego_car[2] + 1,
        c='yellow',
        s=100,
        label='LiDAR'
    )

    # 움직이는 차량
    ax.scatter(
        other_car[0],
        other_car[1],
        other_car[2],
        c='red',
        s=150,
        label='Moving Car'
    )

    # 보행자
    ax.scatter(
        ped[0],
        ped[1],
        ped[2],
        c='green',
        s=100,
        label='Pedestrian'
    )

    # 건물
    for b in buildings:
        xmin, xmax, ymin, ymax, zmin, zmax = b
        ax.bar3d(
            xmin,
            ymin,
            zmin,
            xmax - xmin,
            ymax - ymin,
            zmax - zmin,
            alpha=0.15,
            color='gray'
        )

    # 시야 설정
    ax.set_xlim(-30, 30)
    ax.set_ylim(0, 140)
    ax.set_zlim(0, 30)

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    ax.set_title(
        f"Front-Facing LiDAR Point Cloud | Frame {frame}"
    )

    # 카메라 시점
    ax.view_init( elev=25, azim=-70 )
    ax.legend(loc='upper left')

# 6. 실행
ani = FuncAnimation( fig, update, frames=120, interval=80 )
plt.show()

"""
실행 결과에 대한 설명 -------------
자동차에 장착된 전방 LiDAR가 도시 환경을 스캔하면서 3D 점군(Point Cloud)을 만드는 과정을 보여줌.
그림의 각 요소를 하나씩 설명하면
1. 파란 점 (Ego Car) : 파란 큰 점이 자율주행 차량이다.
   현재 위치: 거의 중앙. Y축 방향으로 앞으로 주행 중. 이 차량 위에 LiDAR가 장착되어 있음.
   즉: 센서를 가진 내 자동차.
2. 노란 점 (LiDAR) : 노란 점이 LiDAR 센서다. 차량 지붕 위에 있다고 가정함.
   여기서 수백 개 레이저를 전방으로 발사해 주변 환경을 측정한다.
   레이저는 이런 방향 벡터로 나감.
   d =(sinhcosv, coshcosv, sinv)  
   h: 좌우 방향 각도, v: 위아래 방향 각도
3. 회색 반투명 건물 : 회색 직육면체는 건물이다.
   LiDAR 레이저가 건물 벽에 닿으면 해당 위치 좌표를 저장한다.
   그래서 건물 벽면에 점들이 생김.
4. 무지개색 점들 = Point Cloud  
   이 점들은 LiDAR가 측정한 좌표이다. 각 점은 [x, y, z] 형태의 3차원 좌표다.
   왜 벽처럼 보이는가? LiDAR가 건물 표면에 맞을 때마다 거리 측정, 위치 계산, 점 저장을 반복한다.
   수천 개 점이 쌓이면 건물 '표면' 모양이 나타난다.
   즉, 점 하나 = 거리 측정 1회,  점 수천 개 = 3D 구조
5. 색깔 의미 : 색은 높이(Z축)를 의미다.
   보통 파란색 → 낮은 위치, 초록색 → 중간 높이, 빨간색 → 높은 위치
   즉, 아래쪽 점은 바닥 근처, 위쪽 빨간 점은 건물 상부를 나타낸다.
6. 빨간 점 (Moving Car) : 빨간 점은 다른 차량이다.
   내 LiDAR가 움직이는 차량도 측정 하고 있다는 의미다.
   즉, LiDAR는 정적인 건물만 보는 게 아니라 움직이는 객체도 계속 감지한다.
7. 초록 점 (Pedestrian) : 초록 점은 보행자이다. 사람도 하나의 객체로 측정된다.
   실제 자율주행에서는 점군(Point Cloud) → 객체 인식 AI → 차량/사람 분류 과정을 거친다.
8. 왜 점들이 전방에만 있는가? 현재 코드는 전방 약 70도만 스캔 하도록 했다.
   즉, 후방은 보지 않음. 좌우도 제한. 자동차 앞쪽만 집중 탐색한다.
   그래서 점군이 차량 앞쪽, 건물 전면, 앞 차량 주변에만 형성된다.
9. 실제 LiDAR에서는 무슨 일이 일어나는가?
   실제 자율주행 LiDAR는 초당 수십만~수백만 번의 레이저 발사, 반사 수신, 거리 계산, 좌표 생성을 수행한다.
   거리 계산은 시간 기반이다.  d= ct / 2  (c: 빛 속도, t: 왕복 시간) 

결국 이 그림은 "LiDAR는 수많은 3차원 점 좌표를 모아서 주변 환경의 3D 지도를 만든다" 를 보여주는 것이다.
즉, 건물 → 점들의 벽, 차량 → 점들의 덩어리, 사람 → 작은 점들의 집합으로 표현된다.
"""