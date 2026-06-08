# 강화학습

# 강화학습은 정답이 아니라 보상으로 배운다.

# 순서
# 1. 환경(Environment) 정의: 에이전트가 활동할 무대 설정
# 2. 상태(State) 정의: 에이전트가 관찰할 수 있는 현재 상황
# 3. 행동(Action) 정의: 에이전트가 취할 수 있는 움직임
# 4. 보상(Reward) 정의: 특정 행동을 했을 때 주는 점수 (학습의 핵심)
# 5. 정책(Policy) 업데이트: 보상을 최대화하는 방향으로 행동 결정 기준을 수정

# 주요 개념
# - 에이전트(Agent): 학습의 주체 (게이머)
# - 에피소드(Episode): 시작부터 종료(목표 달성 또는 실패)까지의 한 판
# - Q-Value: 특정 상태에서 특정 행동을 했을 때 기대되는 미래 보상의 총합
# - 탐험(Exploration) vs 이용(Exploitation): 새로운 길을 가볼 것인가, 아는 길로 갈 것인가의 균형

import numpy as np
import random

np.random.seed(1)
random.seed(1)
