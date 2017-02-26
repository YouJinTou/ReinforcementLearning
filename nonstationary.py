import numpy as np
import matplotlib.pyplot as plt


class Bandit:
    def __init__(self, alpha_constant):
        self.alpha_constant = alpha_constant
        self.epsilon = 0.1
        self.k = 10
        self.q_star_values = np.random.rand(self.k)
        self.q_est_values = np.random.rand(self.k)
        self.action_counts = np.ones(self.k)

    def get_action(self):
        if np.random.random() > self.epsilon:
            action = np.argmax(self.q_est_values)
            return action
        else:
            action = np.random.randint(len(self.q_est_values))
            return action

    def get_reward(self, action):
        # noise = np.random.random()
        reward = self.q_star_values[action]
        return reward

    def update_values(self, action, reward):
        self.q_star_values[action] += np.random.uniform(-0.5, 0.5)
        alpha = 0.1 if self.alpha_constant else 1 / self.action_counts[action]
        self.action_counts[action] += 1
        self.q_est_values[action] += alpha * (reward - self.q_est_values[action])


def run_trial(bandit, steps):
    history = []
    for epoch in range(steps):
        action = bandit.get_action()
        reward = bandit.get_reward(action)x
        bandit.update_values(action, reward)
        history.append(reward)
    return np.array(history)

runs = 2000
steps_per_run = 1000
rewards_with_fixed_alpha = np.zeros(steps_per_run)
rewards_with_varying_alpha = np.zeros(steps_per_run)

for run in range(runs):
    fixed_bandit = Bandit(True)
    rewards_with_fixed_alpha += run_trial(fixed_bandit, steps_per_run)
    varying_bandit = Bandit(False)
    rewards_with_varying_alpha += run_trial(varying_bandit, steps_per_run)

rewards_with_fixed_alpha /= np.float(runs)
rewards_with_varying_alpha /= np.float(runs)

plt.plot(rewards_with_fixed_alpha, label="alpha = 0.1")
plt.plot(rewards_with_varying_alpha, label="alpha = 1 / n")
plt.legend()
plt.show()
