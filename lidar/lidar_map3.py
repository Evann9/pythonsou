"""
이 코드는 “도시 환경에서 자동차에 실린 LiDAR가 주행하며 3D 지도를 만드는 과정을 시뮬레이션” 이다.
장면 구성: 바닥·도로·건물·벽 등으로 단순한 도시형 3D 환경(mesh) 생성 → Open3D의 RaycastingScene에 넣음(실제 라이다 대신 광선쏘기).
차량/센서 모델: 차량 메시에 지붕 오프셋으로 LiDAR를 장착. 사각 경로를 따라 이동하도록 waypoints + 보간으로 포즈 시퀀스 생성.
스캔 시뮬레이션: 한 바퀴(360°)를 AZIMUTH_STEPS로 나누고 매 프레임 BATCH_AZ_PER_FRAME씩 부분 스캔. 수직빔(ELEVATION_DEGS) 포함.
누적 맵: 레이캐스팅으로 얻은 히트 포인트를 전역 좌표로 모아 point cloud에 누적, 주기적으로 voxel 다운샘플.
애니메이션/HUD: 주행 창에서 진행바(스핀 진행도), 궤적 라인, 최근 프레임 포인트 하이라이트를 갱신하며 렌더.
등고선: 매 스핀 종료 시 누적 맵으로 고도 격자화 → 등고선(라인셋) 생성하여 HUD처럼 갱신.
색상: 포인트는 고도 기반 색상맵(turbo). 주행 중은 연한 톤, 최종 뷰는 더 진한 톤으로 표시.
속도 조절: POSE_ADVANCE_PER_SPIN=3, step_len=1.35로 이전보다 조금 빠르게 이동.
최종 뷰: 주행이 끝나면 새로운 창을 띄워 더 진한 색상 + 약간 어두운 밝은 배경으로 최종 3D 지도와 등고선을 표시.
저장: 누적된 최종 포인트 클라우드를 urban_lidar_final_strong_colors.ply로 저장.
즉, “가상의 LiDAR 스캔 → 누적 → 간단한 SLAM 느낌의 시각적 피드백 → 등고선/고도 컬러 → 최종 보기”까지 한 번에 보여주는 자급자족형 시뮬레이터이다.


Urban LiDAR Mapping (Final view: stronger colors, slightly faster car)
- 주행 중 창은 그대로
- 최종 3D 지도 창에서만 색을 진하게(포인트/등고선) + 배경을 약간 어둡게 → 대비↑
- 차량 속도 소폭 증가: POSE_ADVANCE_PER_SPIN=3, step_len=1.35
"""

import numpy as np
import open3d as o3d
import time
from collections import deque
import matplotlib.pyplot as plt
from matplotlib import cm

# 기본 파라미터
AZIMUTH_STEPS = 240
ELEVATION_DEGS = np.linspace(-20, 10, 16)     # 지면 포함 스캔
BATCH_AZ_PER_FRAME = 24
MIN_RANGE, MAX_RANGE = 0.5, 60.0

VOXEL_GLOBAL = 0.12
REFRESH_EVERY = 2
HIGHLIGHT_FRAMES = 10

NUM_PATH_LOOPS = 2
POSE_ADVANCE_PER_SPIN = 4        # ← 살짝 더 빠르게 (기존 2)
SAVE_PLY_PATH = "lidar_urban.ply"

# HUD 진행바
HUD_BAR_LENGTH = 22.0
HUD_BAR_Z = 7.0
HUD_BAR_XY = np.array([-28.0, 28.0], dtype=np.float32)

# 등고선
CONTOUR_GRID = 0.30
CONTOUR_STEP = 0.30
CONTOUR_CMAP = "viridis"
CONTOUR_LEVELS = None

# 주행 중 사용(연한 톤)
CONTOUR_FADE_TO_WHITE_RUN = 0.55
POINT_CMAP = "turbo"
POINT_FADE_TO_WHITE_RUN = 0.25

# 최종 뷰용(진한 톤)
CONTOUR_FADE_TO_WHITE_FINAL = 0.15
POINT_FADE_TO_WHITE_FINAL = 0.05
FINAL_BG_COLOR = np.array([0.97, 0.97, 0.985])  # 약간 더 어두운 밝은 회색 배경 → 대비↑

# 센서 오프셋
SENSOR_OFFSET = np.array([0.0, 0.0, 1.6], dtype=np.float64)
SENSOR_YAW_OFFSET_DEG = 0.0

AZIMUTH_STEPS = max(1, int(AZIMUTH_STEPS))
BATCH_AZ_PER_FRAME = max(1, int(BATCH_AZ_PER_FRAME))
REFRESH_EVERY = max(1, int(REFRESH_EVERY))


# 장면(도시형, 주행 창은 밝은 톤 유지)
def make_scene_geoms():
    geoms = []
    floor = o3d.geometry.TriangleMesh.create_box(width=160, height=160, depth=0.2)
    floor.translate([-80, -80, -0.2])
    floor.paint_uniform_color([0.98, 0.98, 0.985]); geoms.append(floor)

    for (x, y, w, h) in [
        (-20, -40, 120, 10),
        (-20,  10, 120, 10),
        (-40, -20, 10, 80),
        ( 10, -20, 10, 80),
    ]:
        road = o3d.geometry.TriangleMesh.create_box(w, h, 0.05)
        road.translate([x, y, 0.0])
        road.paint_uniform_color([0.95, 0.95, 0.95])
        geoms.append(road)

    for (x, y, w, h, z, col) in [
        (-30, -5,  8, 14, 8,  (0.88, 0.89, 0.92)),
        ( 25,  0,  6, 18,10,  (0.90, 0.91, 0.94)),
        (-10, 28, 12,  7, 9,  (0.92, 0.90, 0.95)),
        ( 52, -8,  5, 22,12,  (0.89, 0.92, 0.95)),
    ]:
        b = o3d.geometry.TriangleMesh.create_box(w, h, z)
        b.translate([x, y, 0.0]); b.paint_uniform_color(col); geoms.append(b)

    for (x, y, r, z) in [(8, -30, 0.8, 6.0), (-48, 8, 1.2, 7.0), (35, 38, 0.7, 5.5)]:
        c = o3d.geometry.TriangleMesh.create_cylinder(r, z)
        c.translate([x, y, 0.0]); c.paint_uniform_color([0.91, 0.93, 0.96]); geoms.append(c)

    wall = o3d.geometry.TriangleMesh.create_box(0.4, 40.0, 5.0)
    wall.translate([70, -15, 0.0]); wall.paint_uniform_color([0.90, 0.93, 0.97]); geoms.append(wall)
    return geoms

def build_raycast_scene(geoms_legacy):
    scene = o3d.t.geometry.RaycastingScene()
    for g in geoms_legacy:
        tg = o3d.t.geometry.TriangleMesh.from_legacy(g)
        scene.add_triangles(tg)
    return scene


# 차량/수학 유틸
def make_car_mesh():
    car = o3d.geometry.TriangleMesh.create_box(3.6, 1.8, 1.3)
    car.translate([-1.8, -0.9, 0.0])
    car.paint_uniform_color([0.25, 0.27, 0.30])
    return car

def deg2rad(d): return d * np.pi / 180.0
def yaw_to_rotmat(yaw):
    c, s = np.cos(yaw), np.sin(yaw)
    return np.array([[ c, -s, 0.0],[ s,  c, 0.0],[0.0, 0.0, 1.0]], dtype=np.float64)
def make_T(R, t):
    T = np.eye(4, dtype=np.float64); T[:3,:3] = R; T[:3,3] = t; return T

def make_waypoints():
    return np.asarray([(-40,-30),(20,-30),(20,30),(-40,30),(-40,-30)], dtype=np.float32)

def interpolate_along_path(wps, step_len=1.35):  # ← 살짝 빠르게(기존 1.2)
    poses = []
    for i in range(len(wps)-1):
        p0, p1 = wps[i], wps[i+1]; seg = p1-p0; L = np.linalg.norm(seg)
        if L < 1e-6: continue
        n = max(1, int(np.ceil(L/step_len))); yaw = np.arctan2(seg[1], seg[0])
        for k in range(n):
            a = k/n; xy = p0*(1-a)+p1*a; poses.append((xy[0], xy[1], yaw))
    poses.append((wps[-1,0], wps[-1,1], poses[-1][2] if poses else 0.0))
    return poses

# 레이 생성/캐스팅
def rays_for_az_batch_world(az_deg_batch, elev_degs, T_ws):
    if az_deg_batch is None or len(az_deg_batch)==0:
        empty = np.zeros((0,6), dtype=np.float32)
        return o3d.core.Tensor(empty, dtype=o3d.core.Dtype.Float32)
    elev = deg2rad(elev_degs).astype(np.float32)
    R = T_ws[:3,:3].astype(np.float32); O = T_ws[:3,3].astype(np.float32)
    origins, dirs = [], []
    for az_deg in az_deg_batch:
        az = deg2rad(az_deg + SENSOR_YAW_OFFSET_DEG).astype(np.float32)
        base = np.array([np.cos(az), np.sin(az), 0.0], dtype=np.float32)
        d = np.stack([base[0]*np.cos(elev), base[1]*np.cos(elev), np.sin(elev)], axis=1).astype(np.float32)
        d = (R @ d.T).T; d /= np.clip(np.linalg.norm(d, axis=1, keepdims=True), 1e-9, None)
        origins.append(np.repeat(O[None,:], d.shape[0], axis=0)); dirs.append(d)
    Oall = np.vstack(origins).astype(np.float32)
    Dall = np.vstack(dirs).astype(np.float32)
    rays = np.hstack([Oall, Dall]).astype(np.float32)
    return o3d.core.Tensor(rays, dtype=o3d.core.Dtype.Float32)

def cast_points(scene, rays_tensor):
    if rays_tensor.shape[0]==0:
        return np.zeros((0,3), dtype=np.float32)
    ans = scene.cast_rays(rays_tensor)
    t = ans["t_hit"].numpy()
    valid = np.isfinite(t) & (t>=MIN_RANGE) & (t<=MAX_RANGE)
    rays = rays_tensor.numpy()
    P = rays[:,:3] + t[:,None]*rays[:,3:6]
    return P[valid].astype(np.float32)

# HUD/궤적
def make_progress_lines():
    border = o3d.geometry.LineSet(); fill = o3d.geometry.LineSet()
    p0 = np.array([HUD_BAR_XY[0], HUD_BAR_XY[1], HUD_BAR_Z], dtype=np.float32)
    p1 = p0 + np.array([HUD_BAR_LENGTH,0,0], dtype=np.float32)
    border.points = o3d.utility.Vector3dVector(np.vstack([p0,p1]))
    border.lines  = o3d.utility.Vector2iVector([[0,1]])
    border.colors = o3d.utility.Vector3dVector([[0.75,0.75,0.78]])
    fill.points = o3d.utility.Vector3dVector(np.vstack([p0,p0]))
    fill.lines  = o3d.utility.Vector2iVector([[0,1]])
    fill.colors = o3d.utility.Vector3dVector([[0.95,0.70,0.35]])
    return border, fill

def update_progress_lines(border, fill, progress01):
    progress01 = float(np.clip(progress01, 0.0, 1.0))
    p0 = np.asarray(border.points)[0]; p1 = np.asarray(border.points)[1]
    p_fill = p0 + (p1-p0)*progress01
    fill.points = o3d.utility.Vector3dVector(np.vstack([p0,p_fill]))

def make_traj_lines():
    ls = o3d.geometry.LineSet()
    p0 = np.array([0,0,0], dtype=np.float32); p1 = p0 + np.array([1e-6,0,0], dtype=np.float32)
    ls.points = o3d.utility.Vector3dVector(np.vstack([p0,p1]))
    ls.lines  = o3d.utility.Vector2iVector([[0,1]])
    ls.colors = o3d.utility.Vector3dVector([[0.5,0.6,0.95]])
    return ls

def push_traj_point(ls, pt, color=(0.5,0.6,0.95)):
    pts = np.asarray(ls.points); lines = np.asarray(ls.lines); cols = np.asarray(ls.colors)
    idx = len(pts)
    pts = np.vstack([pts, pt.reshape(1,3)])
    cols = np.vstack([cols, np.array(color).reshape(1,3)])
    lines = np.vstack([lines, np.array([[idx-1, idx]], dtype=np.int32)])
    ls.points = o3d.utility.Vector3dVector(pts)
    ls.lines  = o3d.utility.Vector2iVector(lines)
    ls.colors = o3d.utility.Vector3dVector(cols)


# 등고선 + 컬러 유틸
def pointcloud_to_heightmap(pcd: o3d.geometry.PointCloud, grid=0.3, agg="max"):
    pts = np.asarray(pcd.points)
    if pts.size == 0:
        return None, None, None
    xmin, ymin = pts[:,0].min(), pts[:,1].min()
    xmax, ymax = pts[:,0].max(), pts[:,1].max()
    nx = int(np.ceil((xmax-xmin)/grid))+1
    ny = int(np.ceil((ymax-ymin)/grid))+1
    ix = np.clip(((pts[:,0]-xmin)/grid).astype(int), 0, nx-1)
    iy = np.clip(((pts[:,1]-ymin)/grid).astype(int), 0, ny-1)
    H = np.full((ny, nx), np.nan, dtype=np.float32)
    if agg=="max":
        for x,y,z in zip(ix,iy,pts[:,2]):
            if np.isnan(H[y,x]) or z>H[y,x]: H[y,x] = z
    else:
        acc = np.zeros((ny,nx),dtype=np.float64); cnt = np.zeros((ny,nx),dtype=np.int32)
        for x,y,z in zip(ix,iy,pts[:,2]): acc[y,x]+=z; cnt[y,x]+=1
        mask = cnt>0; H[mask] = (acc[mask]/cnt[mask]).astype(np.float32)
    xs = xmin + np.arange(nx, dtype=np.float32)*grid
    ys = ymin + np.arange(ny, dtype=np.float32)*grid
    return H, xs, ys

def _fade_to_white(color_rgb, fade):
    return (1.0 - fade) * color_rgb + fade * np.array([1.0, 1.0, 1.0], dtype=np.float32)

def contours_to_linesets(H, xs, ys, levels, cmap_name="viridis", fade=0.5):
    if H is None: return []
    X, Y = np.meshgrid(xs, ys)
    HM = np.ma.array(H, mask=np.isnan(H))
    cs = plt.contour(X, Y, HM, levels=levels)
    cmap = cm.get_cmap(cmap_name, len(levels))
    line_sets = []
    for i, lev in enumerate(levels):
        segs = cs.allsegs[i]
        base_color = np.array(cmap(i)[:3], dtype=np.float32)
        color = _fade_to_white(base_color, fade)
        for seg in segs:
            if len(seg) < 2: continue
            P = np.c_[seg, np.full((len(seg),), lev, dtype=np.float32)]
            ls = o3d.geometry.LineSet()
            ls.points = o3d.utility.Vector3dVector(P)
            lines = np.c_[np.arange(len(P)-1), np.arange(1,len(P))].astype(np.int32)
            ls.lines = o3d.utility.Vector2iVector(lines)
            ls.colors = o3d.utility.Vector3dVector(np.repeat(color[None,:], len(lines), axis=0))
            line_sets.append(ls)
    plt.close()
    return line_sets

def build_contours_from_pcd(pcd, grid=CONTOUR_GRID, levels=None, step=CONTOUR_STEP,
                            cmap=CONTOUR_CMAP, fade=0.5):
    pts = np.asarray(pcd.points)
    if pts.size == 0: return []
    zmin, zmax = float(pts[:,2].min()), float(pts[:,2].max())
    if levels is None:
        if not np.isfinite([zmin,zmax]).all() or zmax-zmin < 1e-6:
            return []
        z0 = np.floor(zmin/step)*step
        z1 = np.ceil(zmax/step)*step
        levels = np.arange(z0, z1+1e-6, step)
    H, xs, ys = pointcloud_to_heightmap(pcd, grid=grid, agg="max")
    return contours_to_linesets(H, xs, ys, levels, cmap_name=cmap, fade=fade)

def colorize_by_height(pcd: o3d.geometry.PointCloud, vmin=None, vmax=None,
                       cmap_name=POINT_CMAP, fade=0.25):
    pts = np.asarray(pcd.points)
    if pts.size == 0:
        return pcd
    z = pts[:,2]
    if vmin is None: vmin = float(np.min(z))
    if vmax is None: vmax = float(np.max(z))
    vmax = vmin + max(1e-6, (vmax - vmin))
    t = np.clip((z - vmin)/(vmax - vmin), 0.0, 1.0)
    colors = cm.get_cmap(cmap_name)(t)[:,:3].astype(np.float32)
    colors = (1.0 - fade) * colors + fade * 1.0   # 흰색과 블렌딩(페이드가 작을수록 진함)
    pcd.colors = o3d.utility.Vector3dVector(colors)
    return pcd


# 메인
def main():
    geoms = make_scene_geoms()
    scene = build_raycast_scene(geoms)

    car = make_car_mesh()
    car_last_T = np.eye(4, dtype=np.float64)

    poses = interpolate_along_path(make_waypoints(), step_len=1.35)
    i_pose = 0
    path_loops_done = 0

    map_pcd = o3d.geometry.PointCloud()
    map_pcd.points = o3d.utility.Vector3dVector(np.array([[1e-9,1e-9,1e-9]], dtype=np.float32))

    flash_pcd = o3d.geometry.PointCloud()
    flash_pcd.points = o3d.utility.Vector3dVector(np.zeros((0,3), dtype=np.float32))
    flash_pcd.colors = o3d.utility.Vector3dVector(np.zeros((0,3), dtype=np.float32))
    flash_queue = deque()

    hud_border, hud_fill = make_progress_lines()
    traj = make_traj_lines()

    contour_lines = []

    # 주행 창(색감/배경 유지)
    vis = o3d.visualization.Visualizer()
    vis.create_window("Urban LiDAR (Run)", 1400, 900)
    for g in geoms: vis.add_geometry(g)
    vis.add_geometry(car); vis.add_geometry(map_pcd)
    vis.add_geometry(flash_pcd); vis.add_geometry(hud_border)
    vis.add_geometry(hud_fill); vis.add_geometry(traj)

    az_all = np.linspace(0, 360, AZIMUTH_STEPS, endpoint=False)
    spin_idx, frame = 0, 0
    pending_pts = []

    running = True
    while running:
        if not vis.poll_events(): break

        x,y,yaw = poses[i_pose]
        T_wc = make_T(yaw_to_rotmat(yaw), np.array([x,y,0.0], dtype=np.float64))
        T_ws = T_wc.copy(); T_ws[:3,3] += (T_wc[:3,:3] @ SENSOR_OFFSET)

        car.transform(np.linalg.inv(car_last_T)); car.transform(T_wc); car_last_T = T_wc.copy()

        push_traj_point(traj, np.array([x,y,0.2], dtype=np.float32))
        vis.update_geometry(traj)

        b0 = spin_idx * BATCH_AZ_PER_FRAME
        if b0 >= AZIMUTH_STEPS:
            spin_idx = 0

            if pending_pts:
                old = np.asarray(map_pcd.points)
                map_pcd.points = o3d.utility.Vector3dVector(np.vstack([old] + pending_pts))
                pending_pts.clear()

            if VOXEL_GLOBAL > 0:
                tmp = map_pcd.voxel_down_sample(VOXEL_GLOBAL)
                map_pcd.points = tmp.points
            # 주행 중은 연한 톤
            colorize_by_height(map_pcd, fade=POINT_FADE_TO_WHITE_RUN)
            vis.update_geometry(map_pcd)

            # 등고선(연한 톤)
            for ls in contour_lines:
                vis.remove_geometry(ls, reset_bounding_box=False)
            contour_lines.clear()
            new_lines = build_contours_from_pcd(
                map_pcd, grid=CONTOUR_GRID,
                levels=CONTOUR_LEVELS, step=CONTOUR_STEP,
                cmap=CONTOUR_CMAP, fade=CONTOUR_FADE_TO_WHITE_RUN
            )
            for ls in new_lines: vis.add_geometry(ls)
            contour_lines = new_lines
            vis.update_renderer()

            i_pose += POSE_ADVANCE_PER_SPIN
            if i_pose >= len(poses):
                i_pose = i_pose % len(poses)
                path_loops_done += 1
                print(f"[path loop] {path_loops_done}/{NUM_PATH_LOOPS}")
                if path_loops_done >= NUM_PATH_LOOPS:
                    running = False
            continue

        b1 = min(b0 + BATCH_AZ_PER_FRAME, AZIMUTH_STEPS)
        az_batch = az_all[b0:b1]
        if az_batch.size == 0:
            spin_idx += 1; frame += 1
            continue

        rays = rays_for_az_batch_world(az_batch, ELEVATION_DEGS, T_ws)
        pts = cast_points(scene, rays)
        if pts.size > 0:
            pending_pts.append(pts)
            flash_queue.append((frame, pts))

        progress01 = float(b1)/float(AZIMUTH_STEPS)
        update_progress_lines(hud_border, hud_fill, progress01)

        if frame % REFRESH_EVERY == 0:
            while flash_queue and (frame - flash_queue[0][0] > HIGHLIGHT_FRAMES):
                flash_queue.popleft()
            if flash_queue:
                flash_pts = np.vstack([p for _,p in flash_queue]).astype(np.float32)
                flash_pcd.points = o3d.utility.Vector3dVector(flash_pts)
                flash_pcd.colors = o3d.utility.Vector3dVector(
                    np.repeat(np.array([1.0, 0.9, 0.6]).reshape(1,3), flash_pts.shape[0], axis=0)
                )
            else:
                flash_pcd.points = o3d.utility.Vector3dVector(np.zeros((0,3), dtype=np.float32))
                flash_pcd.colors = o3d.utility.Vector3dVector(np.zeros((0,3), dtype=np.float32))

            vis.update_geometry(flash_pcd)
            vis.update_geometry(hud_border)
            vis.update_geometry(hud_fill)
            vis.update_geometry(car)
            vis.update_renderer()

        spin_idx += 1
        frame += 1

    # === 종료 처리: 강한 색감으로 최종 맵 준비 ===
    if pending_pts:
        old = np.asarray(map_pcd.points)
        map_pcd.points = o3d.utility.Vector3dVector(np.vstack([old] + pending_pts))
    if VOXEL_GLOBAL > 0:
        tmp = map_pcd.voxel_down_sample(VOXEL_GLOBAL)
        map_pcd.points = tmp.points
    # 최종 뷰는 진한 톤
    colorize_by_height(map_pcd, fade=POINT_FADE_TO_WHITE_FINAL)
    o3d.io.write_point_cloud(SAVE_PLY_PATH, map_pcd, print_progress=True)
    print(f"[Saved] {SAVE_PLY_PATH} | total points={len(map_pcd.points):,}")

    vis.destroy_window()

    # ===== 최종 표시: 더 진한 색 + 약간 어두운 밝은 배경 =====
    final_contours = build_contours_from_pcd(
        map_pcd, grid=CONTOUR_GRID,
        levels=CONTOUR_LEVELS, step=CONTOUR_STEP,
        cmap=CONTOUR_CMAP, fade=CONTOUR_FADE_TO_WHITE_FINAL
    )

    vis2 = o3d.visualization.Visualizer()
    vis2.create_window("Final Urban 3D Map (Stronger Colors)", 1400, 900)
    opt2 = vis2.get_render_option()
    opt2.background_color = FINAL_BG_COLOR
    vis2.add_geometry(map_pcd)
    for ls in final_contours:
        vis2.add_geometry(ls)
    keep = True
    while keep:
        keep = vis2.poll_events()
        vis2.update_renderer()
    vis2.destroy_window()

if __name__ == "__main__":
    main()
