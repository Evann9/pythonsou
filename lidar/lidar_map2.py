"""
3차원 라이다 맵 누적(3D Point Cloud Mapping)의 축소판 예제

핵심만 담고 있다 : SLAM의 복잡한 수학(루프 클로저, 최적화, 그래프 등)은 생략하고, “스캔 → 좌표 변환 → 합치기” 라는 본질만 보여준다.
색상으로 스캔 구분 : 빨강(첫 스캔), 초록(두 번째), 파랑(세 번째)으로 “로봇이 이동하면서 쌓이는 맵”을 직관적으로 볼 수 있다.
좌표축 시각화 : X, Y, Z 축이 보이기 때문에 “로봇이 어디로 이동했는가”를 한눈에 파악할 수 있다.
ICP(정합)의 기본 개념 시연 : '두 스캔이 어긋나면 어떻게 맞추나?'를 눈으로 확인 가능 → ‘지도 정렬’의 개념을 쉽게 체득할 수 있다.
실행 결과 3차원으로 확인 : 마우스로 회전/확대하면서 3D 맵이 진짜 누적되는 걸 볼 수 있다.

초보자에게 어렵게 느껴질 수 부분  --------
잠재적 난관	                    설명	                                    개선 팁
4x4 변환행렬                    회전+이동을 한 번에 표현하는 행렬개념 생소       주석에 “왼쪽 3×3 = 회전, 오른쪽 3×1 = 이동” 명시
ICP 결과의 의미                 fitness나 RMSE의 수치가 무엇을 의미하는지 모름	"1.0이면 거의 완벽 정합, 0.0이면 불일치" 식으로 설명
포인트 클라우드가 뭔가요?         ‘점 구름’ 개념이 처음엔 추상적                 "라이다가 주변 물체를 점으로 찍은 것"이라고 비유
draw_geometries 창 조작법       회전/줌/이동이 마우스로 된다는 걸 모름          실행 후 "마우스 왼쪽 = 회전, 휠 = 줌" 안내 메시지 추가
"""

import open3d as o3d
import numpy as np

# 유틸 함수
def jitter(pcd, sigma=0.005):
    # (선택) 스캔 현실감을 위해 점에 작은 가우시안 노이즈 추가
    pts = np.asarray(pcd.points)                           # PointCloud의 (N,3) 좌표 배열에 접근
    pts += np.random.normal(scale=sigma, size=pts.shape)   # 각 점에 노이즈 더하기
    pcd.points = o3d.utility.Vector3dVector(pts)           # 다시 Open3D 형식으로 되돌리기
    return pcd

def make_axes(size=0.8, transform=None):
    # 3D 좌표축 메쉬(X=red,Y=green,Z=blue). 위치/자세(포즈) 시각화용
    ax = o3d.geometry.TriangleMesh.create_coordinate_frame(size=size)
    if transform is not None:
        ax.transform(transform)     # 주어진 4x4 변환행렬로 좌표축을 이동/회전
    return ax

def voxel(pcd, vs=0.03):
    # Voxel 그리드 다운샘플: 중복/밀집을 줄여 연산 가속 + 노이즈 완화 효과
    return pcd.voxel_down_sample(voxel_size=vs)

def rotz(theta_rad):
    # Z축 회전(3D) 4x4 동차변환행렬 생성: 상단 3x3이 회전, 마지막 열(3x1)이 평행이동 자리
    c, s = np.cos(theta_rad), np.sin(theta_rad)
    T = np.eye(4)
    T[:3, :3] = np.array([[c, -s, 0],
                          [s,  c, 0],
                          [0,  0, 1]])
    return T

def trans(tx, ty, tz=0):
    # 평행이동(3D) 4x4 동차변환행렬 생성: 회전은 항등, 마지막 열이 (tx,ty,tz)
    T = np.eye(4)
    T[:3, 3] = [tx, ty, tz]
    return T


# 1) 겹치는 두 스캔 (ICP 데모용)
print("[1] 기준 스캔(pcd1) 생성")
mesh_box = o3d.geometry.TriangleMesh.create_box(width=1.6, height=1.0, depth=1.2)
pcd1 = mesh_box.sample_points_poisson_disk(number_of_points=2000)  # 메쉬 표면에서 3D 점 샘플링
pcd1.paint_uniform_color([1, 0, 0])  # 빨강: 기준 스캔으로 인지하기 쉽게 색상 지정
pcd1 = voxel(pcd1, 0.02)             # 다운샘플: 계산량 절감 + 매칭 안정성 향상
# pcd1 = jitter(pcd1, sigma=0.003)   # (옵션) 약간의 노이즈를 넣어 현실감/ICP 난이도 조절

print("[2] 두 번째 스캔의 '진짜' 자세(pcd2_true) 만들기 (겹치도록 작은 변환)")
# pcd2_true: 실제로는 pcd1과 거의 겹치는 위치/자세(포즈)에 있다고 가정 (작은 이동+작은 회전)
T_small = trans(0.08, -0.05, 0.0) @ rotz(np.deg2rad(4.0))  # '@'는 행렬 곱. 회전→이동 순서로 합성
pcd2_true = o3d.geometry.PointCloud(pcd1)  # pcd1 복사(원본 보존)
pcd2_true = pcd2_true.transform(T_small)   # '정답'에 해당하는 변환을 적용한 스캔(현실의 ground truth 역할)
pcd2_true.paint_uniform_color([0, 1, 0])   # 초록: 두 번째 스캔
pcd2_true = voxel(pcd2_true, 0.02)
# pcd2_true = jitter(pcd2_true, sigma=0.003)

print("[3] 일부러 틀린 초기 추정(pcd2_wrong) 생성 (ICP 시작점)")
# pcd2_wrong: 우리가 가진 초기 포즈 추정(오차가 있는 상태). ICP가 이 오차를 보정할 것.
T_init_guess = trans(0.05, 0.02, 0.0) @ rotz(np.deg2rad(2.0))  # '약간' 틀린 초기치
pcd2_wrong = o3d.geometry.PointCloud(pcd1)       # pcd1 복사 후
pcd2_wrong = pcd2_wrong.transform(T_init_guess)  # 잘못된 초기 포즈 적용(의도적 오차)
pcd2_wrong.paint_uniform_color([0, 0.8, 0])      # 약간 다른 초록: '정합 전' 상태 구분용
pcd2_wrong = voxel(pcd2_wrong, 0.02)


# 2) ICP 정합 (pcd2_wrong → pcd1)
print("[4] ICP 실행: pcd2_wrong 을 pcd1에 정합 (point-to-point)")
# ICP 핵심 아이디어:
    #  - 소스(source)와 타깃(target)의 가장 가까운 점쌍을 반복적으로 대응시킴
    #  - 그 대응쌍들 사이의 거리를 최소화하는 R(회전), t(이동)를 추정
    #  - 수렴할 때까지 반복 → 오차(평균제곱근) 감소
max_corr_dist = 0.08  # 최근접점 대응 허용반경(작을수록 엄격, 데이터 겹침/노이즈에 따라 조정)
reg = o3d.pipelines.registration.registration_icp(
    source=pcd2_wrong,               # 보정할 스캔(현재 어긋남)
    target=pcd1,                     # 기준 스캔(정답 좌표계)
    max_correspondence_distance=max_corr_dist,
    estimation_method=o3d.pipelines.registration.TransformationEstimationPointToPoint(),  # 점-대-점
    criteria=o3d.pipelines.registration.ICPConvergenceCriteria(max_iteration=60)          # 반복 한도
)
print(" - ICP fitness:", reg.fitness, "| inlier RMSE:", reg.inlier_rmse)
#  * fitness: 유효 대응쌍 비율(1.0에 가까울수록 겹침이 좋음)
#  * inlier RMSE: 대응쌍 거리의 제곱평균근(작을수록 정합 품질이 좋음)
print(" - Estimated T:\n", reg.transformation)    # 추정된 4x4(회전+이동) 확인

pcd2_icp = o3d.geometry.PointCloud(pcd2_wrong)    # 정합 결과를 적용할 복사본
pcd2_icp.transform(reg.transformation)            # ICP가 추정한 보정 변환 적용
pcd2_icp.paint_uniform_color([0, 1, 0])           # 최종 초록(정답 포즈에 근접 기대)


# 3) 멀리 떨어진 세 번째 스캔(누적 예시)
print("[5] 세 번째 스캔(pcd3): 알고 있는 변환으로 멀리 이동시켜 누적")
# 실제 맵핑에서는 로봇이 크게 이동한 곳의 스캔을 '알고 있는 포즈'(예: odom/IMU/SLAM 추정)로 전역 좌표계에 배치
mesh_cyl = o3d.geometry.TriangleMesh.create_cylinder(radius=0.35, height=1.4)
pcd3 = mesh_cyl.sample_points_poisson_disk(number_of_points=1500)
pcd3.paint_uniform_color([0, 0, 1])      # 파랑: 세 번째 스캔
T_far = trans(5.0, 5.0, 0.0)             # 큰 평행이동: 멀리 떨어진 위치(ICP 없이 '정답 포즈' 가정)
pcd3.transform(T_far)
pcd3 = voxel(pcd3, 0.02)

# 4) 좌표축(전역/스캔 위치) 만들기
print("[6] 전역/스캔별 좌표축 추가")
axes_global = make_axes(size=0.6)                        # 전역(월드) 좌표계 원점
axes_scan1  = make_axes(size=0.4, transform=np.eye(4))   # 스캔1 위치(원점)
axes_scan2  = make_axes(size=0.4, transform=T_small)     # 스캔2 '진짜' 포즈(ground truth)
axes_scan3  = make_axes(size=0.5, transform=T_far)       # 스캔3 포즈(멀리 떨어진 곳)

# 5) 시각화 (정합 전 / 정합 후)
print("[7] (정합 전) pcd1(빨강) + pcd2_wrong(초록, 어긋남) + 축")
# 여기서는 '왜 ICP가 필요한지'를 보여줌: 같은 물체인데 초기 포즈 오차로 겹치지 않음
o3d.visualization.draw_geometries(
    [axes_global, axes_scan1, axes_scan2, pcd1, pcd2_wrong],
    window_name="Before ICP (Red=pcd1, Green=pcd2_wrong)",
    width=900, height=700
)

print("[8] (정합 후) pcd1(빨강) + pcd2_icp(초록, 정합됨) + 스캔3(파랑) 누적 + 축")
# ICP로 pcd2_wrong → pcd1에 정렬 완료(pcd2_icp). 여기에 pcd3(멀리)까지 누적해 '확장된 지도' 느낌 제공
map_pcd = pcd1 + pcd2_icp + pcd3        # 단순 누적: 동일 전역 좌표계에 점군을 더함
o3d.visualization.draw_geometries(
    [axes_global, axes_scan1, axes_scan2, axes_scan3, map_pcd],
    window_name="After ICP + Accumulated Map (Red+Green+Blue)",
    width=1000, height=750
)

print("완료: ESC로 창을 닫으세요.")


"""
실행 결과 중에서 
- Estimated T:
 [[ 9.99390827e-01  3.48994967e-02 -7.84691322e-18 -5.06675313e-02]
 [-3.48994967e-02  9.99390827e-01  1.84043319e-17 -1.82428417e-02]
 [-3.15469727e-19 -2.80649675e-17  1.00000000e+00  8.18759197e-16]
 [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]

출력된 행렬은 ICP가 계산한 '두 포인트 클라우드 간의 3차원 좌표 변환(Transformation)', 
즉 source(pcd2_wrong)를 target(pcd1)과 최대한 겹치게 만드는 4×4 동차변환행렬 (Homogeneous Transformation Matrix)임.

1. 행렬의 구조
[ R | t ]
[ 0 | 1 ]
즉,
구성	                 의미
R (3×3)	                회전행렬 (Rotation) — 두 좌표계의 방향 차이
t (3×1)             	이동벡터 (Translation) — 두 좌표계의 위치 차이
마지막 행 [0 0 0 1]	     동차좌표 계산을 위한 형식적 항목

2. 실제 출력값 해석
[[ 0.999390827  0.034899497  0.0   -0.0506675313]
 [-0.034899497  0.999390827  0.0   -0.0182428417]
 [ 0.0          0.0          1.0    0.0           ]
 [ 0.0          0.0          0.0    1.0           ]]

(지수 표기 e-02, e-17 등은 아주 작은 수 = 0에 가까움)
이를 나눠보면  회전 행렬 R:
[[ 0.999390827  0.034899497  0.0 ]
 [-0.034899497  0.999390827  0.0 ]
 [ 0.0          0.0          1.0 ]]
이건 Z축을 중심으로 약 2° 회전한 행렬이다. (→ cos(2°)=0.99939, sin(2°)=0.0349)
즉, ICP가 “회전 차이를 약 2도 정도로 보정했다”고 본 것임.

이동 벡터 t: [-0.0506675313, -0.0182428417, 8.18e-16]
    → X축 방향으로 약 −0.05m,
    → Y축 방향으로 약 −0.018m 이동하라는 의미.
즉, '소스 점군을 왼쪽으로 약 5cm, 아래로 약 2cm 이동시켜라.'

3. 의미 요약
항목	    값	                        의미
회전	    약 2° (Z축 기준)	         두 스캔의 방향 차이
평행이동	(−0.05, −0.018, ≈0) m	    두 스캔의 위치 차이
목적	    pcd2_wrong → pcd1에 최대한 정렬

5. 현실적으로 말하면 '로봇이 실제보다 약간 기울어진 방향(2°)으로, 
약 5cm 옆에 있었다”는 오차를 ICP가 자동으로 찾아서 보정한 것이다.
"""