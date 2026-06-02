# pip install gymnasium


import numpy as np
import matplotlib.pyplot as plt
import koreanize_matplotlib
import gymnasium  # 실습 환경 제공(현재상태 제공 -> 행동선택 -> 환경에서 행동 반영)
import gymnasium as gym
import math
from gymnasium import spaces  # 행동 공간과 관측 공간을 정의

# 환경 / 장애물 / 라이다 설정
WORLD_W, WORLD_H = 20.0, 15.0
OBSTACLES = [
    (6.0, 4.0, 0.5),
    (8.0, 10.0, 1.5),
    (15.0, 5.0, 1.0),
]
NUM_RAYS = 32   # 레이저 갯수
FOV = np.deg2rad(180)  # 전방 각도
MAX_RANGE = 8.0  # 라이다 최대 감지 거리
STEP_MARCH = 0.05  # 레이 전진 단위 거리


# 좌표값이 시뮬레이터 공간 경계 내에 있는지 여부
def inside_world(x, y):  
    return (0.0 <= x <= WORLD_W) and (0.0 <= y <= WORLD_H)

# 라이다 광선의 종점이 장애물과 충돌했는지 여부
def hit_circle(px, py, cx, cy, r):
    return (px - cx)**2 + (py - cy)**2 <= r**2

# 에이전트(x, y, theta)에서 시야각(FOV)으로 NUM_RAYS개의 광선을 쏴, 각 레이가 처음 부딪히는 지점까지 거리 구하기
def cast_lidar(x, y, theta, num_rays=NUM_RAYS, fov=FOV, max_range=MAX_RANGE, step=STEP_MARCH):
    start = theta - fov/2  # 전방 시야각 왼쪽 끝 각도(첫번째 레이 시작 각도)
    angles = start + np.arange(num_rays) * (fov / max(num_rays - 1, 1))
    dists = np.full(num_rays, max_range, dtype=np.float32)  # 초기 거리 배열 초기화 = 최대거리
    for i, ang in enumerate(angles):
        dist = 0.0
        hit = False

        while dist < max_range:
            px = x + np.cos(ang) * dist
            py = y + np.sin(ang) * dist
            if not inside_world(px, py):
                hit = True
                break

            for (cx, cy, r) in OBSTACLES:
                if hit_circle(px, py, cx, cy, r):
                    hit = True
                    break
            
            if hit: 
                break

            dist += step

        dists[i] = min(dist, max_range) 
        
    return dists, angles

class SimpleLidarEnv(gym.Env):
    def __init__(self, render_mode="human"):
        super().__init__()
        self.render_mode = render_mode
        # 강화학습 환경 설정 시 두가지는 반드시 선언
        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            low=0.0, high=MAX_RANGE, shape=(NUM_RAYS,), dtype=np.float32
        # 관측값은 길이 20짜리 배열, 각 값의 범위는 0.0 ~ MAX_RANGE 
        )

        self.v = 0.25   # 전진속도
        self.steer_delta = np.deg2rad(8)  # 회전각도
        self.goal = np.array([18.0, 12.0], dtype=np.float32)  # 최종 목표
        self.goal_radius = 0.6  # 목표 판정 반경
        self.max_steps = 400  # 최대 step수 : 하나의 에피소드에서 허용되는 최대 행동 수

        self.fig, self.ax = None, None  # 랜더링용 객체
        self._state = None  # [x,y,theta]
        self._prev_goal_dist = None  # 이전 목표 거리
        self._steps = 0  # step counter
    
    def _get_obs(self):
        obs, _ = cast_lidar(self._state[0], self._state[1], self._state[2])
        return obs
    
    def _get_info(self):
        x, y, _ = self._state
        if not inside_world(x, y):
            return True
    
    def _collision(self):
        x, y, _ = self._state
        if not inside_world(x, y):
            return True
        
        for (cx, cy, r) in OBSTACLES:
            if hit_circle(x, y, cx, cy, r):
                return True
            
        return False
    
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self._state = np.array([2.0, 2.0, np.deg2rad(0.0)], dtype=np.float32)
        self._steps = 0
        self._prev_goal_dist = np.linalg.norm(self._state[:2] - self.goal)
        obs = self._get_obs()
        info = {}
        return obs, info
    
    def step(self, action):
        self._steps += 1
        # action: 0(좌회전), 1(직진), 2(우회전)
        if action == 0: self._state[2] += self.steer_delta
        elif action == 2: self._state[2] -= self.steer_delta
        
        self._state[0] += self.v * np.cos(self._state[2])
        self._state[1] += self.v * np.sin(self._state[2])

        obs = self._get_obs()
        collision = self._collision()
        curr_dist = np.linalg.norm(self._state[:2] - self.goal)
        reached = curr_dist < self.goal_radius

        reward = (self._prev_goal_dist - curr_dist) * 10.0
        self._prev_goal_dist = curr_dist

        terminated = False
        truncated = False
        if collision:
            reward = -10.0
            terminated = True
        elif reached:
            reward = 100.0
            terminated = True
        elif self._steps >= self.max_steps:
            truncated = True

        return obs, reward, terminated, truncated, {}

if __name__ == "__main__":
    env = SimpleLidarEnv()
    obs, info = env.reset()
    for _ in range(10):
        obs, reward, done, trunc, info = env.step(env.action_space.sample())
        print(f"Step: {env._steps}, Pos: {env._state[:2].round(2)}, Reward: {reward:.2f}")
        if done or trunc: break


"""
# 1. 도시 환경(건물 박스들) 만들기
# 건물은 AABB(축 정렬 박스)로 표현: (min_xyz, max_xyz)
def make_city():
    buildings = []
    rng = np.random.default_rng(42)

    # x,y 평면에 건물 여러 개를 랜덤 배치
    for _ in range(20):
        cx, cy = rng.uniform(-40, 40, size=2)      # 건물 중심
        sx, sy = rng.uniform(4, 12, size=2)        # 가로/세로 크기
        h = rng.uniform(6, 25)                     # 높이

        min_xyz = np.array([cx - sx/2, cy - sy/2, 0.0])
        max_xyz = np.array([cx + sx/2, cy + sy/2, h])
        buildings.append((min_xyz, max_xyz))

    # 큰 건물 몇 개 추가(시각적으로 “도시 느낌”)
    buildings.append((np.array([-10, -10, 0]), np.array([5, 5, 30])))
    buildings.append((np.array([15, 10, 0]), np.array([30, 25, 18])))
    return buildings


# 2. Ray vs AABB 교차(레이가 박스를 맞는지) 계산
# origin: 레이 시작점(차량 위치)
# dir: 레이 방향(단위벡터 권장)
# box_min, box_max: AABB
# 반환: (맞으면 True, t_hit) / (아니면 False, None)
def ray_aabb_intersect(origin, dir, box_min, box_max):
    # "슬랩(slab) 방법" - 축마다 교차 구간을 계산하여 겹치면 hit
    # dir이 0인 축은 분모가 0이 되므로 작은 값으로 처리
    eps = 1e-9
    d = np.where(np.abs(dir) < eps, eps, dir)

    t1 = (box_min - origin) / d
    t2 = (box_max - origin) / d

    tmin = np.maximum.reduce(np.minimum(t1, t2))
    tmax = np.minimum.reduce(np.maximum(t1, t2))

    # tmax < 0: 박스가 레이 시작점 뒤에 있음
    # tmin > tmax: 교차 구간이 없음
    if tmax < 0 or tmin > tmax:
        return False, None

    # tmin이 음수면 레이가 박스 내부에서 시작한 케이스 등 → tmax를 쓸 수도 있음
    t_hit = tmin if tmin >= 0 else tmax
    return True, t_hit


# 3. LiDAR 스캔 방향(레이들) 만들기
def make_lidar_directions(num_az=120, num_el=8, el_min_deg=-10, el_max_deg=10):
    # 방위각(azimuth): 0~360도
    az = np.linspace(0, 2*np.pi, num_az, endpoint=False)

    # 고도각(elevation): -10~+10도 정도로 좁게(차량 LiDAR 느낌)
    el = np.deg2rad(np.linspace(el_min_deg, el_max_deg, num_el))

    dirs = []
    for e in el:
        for a in az:
            # 구면좌표 → 직교좌표
            x = np.cos(e) * np.cos(a)
            y = np.cos(e) * np.sin(a)
            z = np.sin(e)
            v = np.array([x, y, z])
            v = v / np.linalg.norm(v)
            dirs.append(v)
    return np.array(dirs)


# 4. 차량 경로 만들기(도시를 관통하는 간단한 궤적)
def make_vehicle_path(T=80):
    # S자 형태로 이동하도록 구성 (교육용으로 보기 좋게)
    t = np.linspace(0, 1, T)
    x = -45 + 90 * t
    y = 15 * np.sin(2*np.pi * t)
    z = np.full_like(x, 1.5)  # LiDAR 높이(지면에서 1.5m)
    return np.stack([x, y, z], axis=1)


# 5. 스캔 실행: 차량이 이동하며 점군 누적 → 3D 지도 생성
def simulate_mapping(buildings, path, dirs, max_range=60.0):
    all_points = []

    for pose in path:
        origin = pose

        for d in dirs:
            # 각 레이에 대해 "가장 가까운 hit" 찾기
            best_t = None

            for (bmin, bmax) in buildings:
                hit, t_hit = ray_aabb_intersect(origin, d, bmin, bmax)
                if not hit:
                    continue

                # LiDAR 최대 거리 제한
                if t_hit > max_range:
                    continue

                if (best_t is None) or (t_hit < best_t):
                    best_t = t_hit

            if best_t is not None:
                p = origin + best_t * d
                # 약간의 센서 노이즈(실제처럼 점이 완전히 격자처럼 안 보이게)
                p = p + np.random.normal(scale=0.05, size=3)
                all_points.append(p)

    if len(all_points) == 0:
        return np.empty((0, 3))
    return np.array(all_points)


# 6. 시각화(3D 점군 + 차량 경로)
def plot_result(points, path, buildings):
    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    # 누적 점군(3D 지도)
    if len(points) > 0:
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], s=1)

    # 차량 경로
    ax.plot(path[:, 0], path[:, 1], path[:, 2], linewidth=2)

    # 건물의 바닥 윤곽(가볍게 표시)
    for (bmin, bmax) in buildings:
        # 바닥( z=0 ) 사각형 라인
        xs = [bmin[0], bmax[0], bmax[0], bmin[0], bmin[0]]
        ys = [bmin[1], bmin[1], bmax[1], bmax[1], bmin[1]]
        zs = [0, 0, 0, 0, 0]
        ax.plot(xs, ys, zs, linewidth=1)

    ax.set_title("LiDAR 주행 스캔 → 점군 누적 3D 지도(교육용 기초 시뮬레이션)")
    ax.set_xlabel("X (m)")
    ax.set_ylabel("Y (m)")
    ax.set_zlabel("Z (m)")

    ax.set_xlim(-50, 50)
    ax.set_ylim(-50, 50)
    ax.set_zlim(0, 35)

    plt.tight_layout()
    plt.show()


def main():
    buildings = make_city()
    dirs = make_lidar_directions(num_az=120, num_el=8, el_min_deg=-12, el_max_deg=12)
    path = make_vehicle_path(T=90)

    points = simulate_mapping(buildings, path, dirs, max_range=70.0)
    print("누적 점 개수:", len(points))

    plot_result(points, path, buildings)


if __name__ == "__main__":
    main()
"""
"""
① 수많은 작은 점들
   → LiDAR가 실제로 측정한 결과. LiDAR는 면(벽) 을 직접 보는 게 아님.
       예) “벽이 있다”면 “레이저가 벽에 맞은 지점 좌표 하나”
       그래서 결과는 면이 아니라 점들의 집합(점군, Point Cloud) 으로 보인다.
   점 하나 = “이 위치에서 이 방향으로 쏜 레이저가 저 거리에서 물체를 처음 만났다”

② 점들이 건물 모양을 ‘따라서’ 모여 있음
    그래서 벽, 모서리, 건물 옆면을 따라 점이 빽빽하고 허공에는 점이 거의 없음
    이게 바로 “LiDAR는 물체 표면만 찍는다” 는 핵심 특성이다.
③ 하나의 연속된 선 (굵은 라인)  → 자동차의 주행 경로 
    LiDAR 센서가 달린 자동차가 이 선을 따라 이동하면서 매 위치마다 주변을 스캔함
    즉,  차 위치 1 → 스캔 → 점 몇 천 개,  차 위치 2 → 스캔 → 점 몇 천 개,  차 위치 3 → 스캔 → 점 몇 천 개 ...
    이 점들이 전부 누적된 결과가 화면에 보이는 점이다.
④ 바닥에 그려진 네모 윤곽선 → “실제 건물 위치 참고용” (보조 시각화)
    교육용으로 “여기에 건물이 있다”는 힌트임. 
    실제 LiDAR 결과는 이 선을 모름. LiDAR는 오직 점만 안다

시간 흐름으로 다시 설명하면 (중요)
1) 처음 출발
    차 위치: 맨 왼쪽
    LiDAR가 주변을 한 번 스캔 - 점이 아주 조금만 생김
2) 조금 이동
    차가 앞으로 감. 다시 스캔 -->  기존 점 + 새로운 점
3) 계속 주행
    건물 옆을 지나감. 벽을 여러 각도에서 계속 스캔 --> 벽 모양이 점으로 점점 또렷해짐
4) 주행 종료
    점들이 충분히 쌓임. “도시의 3D 점군 지도”처럼 보임

이 그림을 통해 이해해야 할 핵심 메시지 3개
1) LiDAR는 “면”을 보지 않는다. 오로지 점(point)만 측정한다
2) 지도는 한 번에 만들어지지 않는다. 움직이면서 찍은 점들이 누적되어 지도처럼 보일 뿐.
3) 이게 바로 자율주행에서 말하는 “3D 맵의 원형”
    - 실제 HD Map
    - 실제 SLAM
    - 실제 자율주행 인식
    모두 이 개념에서 출발

LiDAR 지도는 “카메라 사진”이 아니라 “레이저로 찍은 수만 장의 거리 사진을 겹쳐 붙인 결과”다
"""
