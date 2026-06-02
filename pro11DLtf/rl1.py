# Q-learning의 구조를 이해하기 - 벨만 방정식 기반의 근사 학습

import random
import numpy as np

# 상태 공간
state_space = [0,1,2,3,4,5]

# 행동 공간
action_space = [-1, 1]

# Q-table 
# Q[state][action] : 특정 상태에서 특정 행동을 했을 때의 가치

Q = np.zeros((len(state_space), len(action_space)))
print(Q)

# 하이퍼 파라미처 설정
alpha = 0.1    # 학습률
gamma = 0.9    # 할인률
epsilon = 1.0  # 탐험 확률
epsilon_decay = 0.99  # epsilon 감소율
epsilon_min = 0.1    # 최소 탐험 확률
episodes = 500  # 전체 학습 횟수

# 보상 함수
def get_reward(state):
    return 10 if state == 4 else 0

# 학습
for episode in range(episodes):
    state = 0
    for step in range(20):
        if random.random() < epsilon:
            action_index = random.randint(0, 1)  # 탐험
        else:
            action_index = np.argmax(Q[state])   # 이용

        action = action_space[action_index]  # action_index를 실제 행동값(-1 or 1)으로 변환
    
        # 다음 상태 계산
        next_state = state + action
        if next_state < 0 or next_state > 4:
            next_state = state

        # 보상 계산
        reward = get_reward(next_state)

        # Q-table 업데이트
        old_q = Q[state, action_index]

        next_max = np.max(Q[next_state])

        # Q-learning 갱신 - 벨만 방정식 (가장 중요한 수식)
        Q[state, action_index] = old_q + alpha * (reward + gamma * next_max - old_q)

        state = next_state

        if reward == 10:
            break

    # epsilon 감소
    epsilon = max(epsilon_min, epsilon * epsilon_decay)
    # print('epsilon :', epsilon)

print(Q)