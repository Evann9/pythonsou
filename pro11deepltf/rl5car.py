import random
from pathlib import Path

import koreanize_matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter


state_space = np.linspace(-1.0, 1.0, 11)
action_space = [-1, 0, 1]
Q = np.zeros((len(state_space), len(action_space)))

alpha = 0.1
gamma = 0.9
epsilon = 1.0
epsilon_decay = 0.99
epsilon_min = 0.1
episodes = 500
steps_per_episode = 50


def get_state_index(position):
    return np.argmin(np.abs(state_space - position))


def get_reward(position):
    return 1 - abs(position)


def step_func(position, action):
    position += action * 0.1
    position = np.clip(position, -1.0, 1.0)
    reward = get_reward(position)
    return position, reward


def choose_action(state_idx):
    if random.random() < epsilon:
        return random.randrange(len(action_space))
    return np.argmax(Q[state_idx])


def make_policy_positions(start_position=0.8, steps=50):
    positions = [start_position]
    position = start_position

    for _ in range(steps):
        state_idx = get_state_index(position)
        action_idx = np.argmax(Q[state_idx])
        action = action_space[action_idx]
        position, _ = step_func(position, action)
        positions.append(position)

    return positions


reward_list = []

for ep in range(episodes):
    position = np.random.uniform(-1.0, 1.0)
    total_reward = 0

    for _ in range(steps_per_episode):
        state_idx = get_state_index(position)
        action_idx = choose_action(state_idx)
        action = action_space[action_idx]

        next_position, reward = step_func(position, action)
        next_state_idx = get_state_index(next_position)
        best_next_q = np.max(Q[next_state_idx])

        Q[state_idx, action_idx] += alpha * (
            reward + gamma * best_next_q - Q[state_idx, action_idx]
        )

        position = next_position
        total_reward += reward

    reward_list.append(total_reward)
    epsilon = max(epsilon_min, epsilon * epsilon_decay)

    if ep % 50 == 0:
        initial_avg = np.mean(reward_list[:50])
        final_avg = np.mean(reward_list[-50:])
        max_reward = np.max(reward_list)
        min_reward = np.min(reward_list)

        print("Performance Summary")
        print(f"- initial 50 episodes average reward : {initial_avg:.3f}")
        print(f"- final 50 episodes average reward : {final_avg:.3f}")
        print(f"- max reward : {max_reward:.3f}")
        print(f"- min reward : {min_reward:.3f}")

        if final_avg > initial_avg:
            print(f"모델이 개선됨 (+{final_avg - initial_avg:.3f})\n")
        else:
            print("모델이 개선되지 않음\n")


# Reward graph
plt.figure(figsize=(10, 5))
plt.plot(reward_list, label="Episode reward")
plt.axhline(y=0, color="gray", linestyle="--", linewidth=1)
plt.title("Reward per Episode")
plt.xlabel("episode")
plt.ylabel("reward")
plt.legend()
plt.grid(True)


# Average reward graph
window = 50
avg_rewards = []

for i in range(0, len(reward_list), window):
    chunk = reward_list[i:i + window]
    avg_rewards.append(np.mean(chunk))

plt.figure(figsize=(10, 5))
plt.plot(range(0, len(reward_list), window), avg_rewards, marker="o",
         label="average reward")
plt.title("Average Reward per 50 Episodes")
plt.xlabel("episode")
plt.ylabel("reward")
plt.legend()
plt.grid(True)


# Position distribution with the learned policy
position_counts = np.zeros(len(state_space))

for _ in range(100):
    position = np.random.uniform(-1.0, 1.0)

    for _ in range(steps_per_episode):
        state_idx = get_state_index(position)
        position_counts[state_idx] += 1

        action_idx = np.argmax(Q[state_idx])
        action = action_space[action_idx]
        position, _ = step_func(position, action)

plt.figure(figsize=(10, 3))
plt.bar(state_space, position_counts, width=0.15, color="skyblue",
        align="center")
plt.title("Position Distribution (State Frequency)")
plt.xlabel("Position (State)")
plt.ylabel("Frequency")
plt.xticks(state_space)
plt.grid(True)


# Animation: learned movement toward the center position 0
animation_positions = make_policy_positions(start_position=0.8, steps=50)

fig, ax = plt.subplots(figsize=(8, 3))
ax.set_xlim(-1.05, 1.05)
ax.set_ylim(-0.5, 0.5)
ax.axhline(0, color="black", linewidth=2)
ax.axvline(0, color="green", linestyle="--", linewidth=2, label="center")
ax.set_title("Learned Policy Animation")
ax.set_xlabel("position")
ax.set_yticks([])
ax.grid(True, axis="x")

car, = ax.plot([animation_positions[0]], [0], marker="s", markersize=18,
               color="tomato", label="car")
info_text = ax.text(-1.0, 0.32, "", fontsize=11)
ax.legend(loc="upper right")


def update_animation(frame):
    current_position = animation_positions[frame]
    car.set_data([current_position], [0])
    info_text.set_text(f"step: {frame}, position: {current_position:.2f}")
    return car, info_text


ani = FuncAnimation(
    fig,
    update_animation,
    frames=len(animation_positions),
    interval=250,
    blit=True,
    repeat=True,
)

animation_path = Path(__file__).with_name("rl5car_policy.gif")
ani.save(animation_path, writer=PillowWriter(fps=4))
print(f"Animation saved: {animation_path}")

plt.show()
