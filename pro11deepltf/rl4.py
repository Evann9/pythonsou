# DQN : Q-learning을 딥러닝 신경망으로 확장한 강화학습 알고리즘
# Q-table 대신 신경망을 사용
# 구조
"""
환경 Environment
-> 
현재 상태 state
-> 
행동별 Q 값 예측
->
행동 action 선택
-> 
환경에 action 실행
-> 
reward, next_state, done (경험)
->
ReplayBuffer에 저장
-> 
랜덤하게 샘플링
->
Target Network로 target을 갱신
-> 
Q-Network 학습  (현재 상태를 입력 받아 각 행동의 Q 값을 갱신)

학생이 환경에서 문제를 경험함 -> 문제은행에 저장 -> 
문제은행에서 랜덤으로 문제를 꺼냄 -> 정답지를 보고 목표값 계산 -> 
학생 신경망을 갱신
"""
# 카트 애니메이션 생성
import matplotlib.pyplot as plt
from matplotlib import animation
import IPython.display as ipd
from tensorflow import keras
import numpy as np
import gym

# Fix for NumPy 2.0 compatibility with legacy gym
if not hasattr(np, 'bool8'):
    np.bool8 = np.bool_
if not hasattr(np, 'typeDict'):
    np.typeDict = np.sctypeDict

env = gym.make("CartPole-v1")
model = keras.models.load_model("cartpole_model.keras")
print(model)

state_dim = env.observation_space.shape[0]
num_actions = env.action_space.n

# 궤적 수집
flat_states = []
episodic_labels = []

# Handle different gym API versions for reset
res = env.reset()
state = res[0] if isinstance(res, tuple) else res

done = False
ep_num = 0

while not done:
  flat_states.append(state.copy())
  episodic_labels.append(ep_num)

  state_input = np.reshape(state, [1, state_dim])
  q_values = model.predict(state_input, verbose=0)
  action = np.argmax(q_values[0])

  # Step returns (obs, reward, done, info) or (obs, reward, terminated, truncated, info)
  step_results = env.step(action)
  if len(step_results) == 4:
    next_state, reward, done, info = step_results
  else:
    next_state, reward, terminated, truncated, info = step_results
    done = terminated or truncated

  state = next_state

env.close()
print(f"Successfully collected {len(flat_states)} states.")
