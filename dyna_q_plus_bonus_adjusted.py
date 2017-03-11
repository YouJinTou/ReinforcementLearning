import matplotlib.pyplot as plt
import numpy as np

ALPHA = 0.1
EPSILON = 0.1
GAMMA = 0.95
PLANNING_STEPS = 5


class World:

    def __init__(self, height, width, start, end, obstacles):
        self.UP = 0
        self.DOWN = 1
        self.LEFT = 2
        self.RIGHT = 3
        self.ACTIONS = [self.UP, self.DOWN, self.LEFT, self.RIGHT]

        self.height = height
        self.width = width
        self.start_state = start
        self.end_state = end
        self.obstacles = obstacles
        self.q_values = np.zeros((self.height, self.width, len(self.ACTIONS)))

    def get_action(self, state):
        is_greedy = np.random.random() > EPSILON
        action = np.argmax(self.q_values[state[0], state[1], :]) if is_greedy else np.random.choice(self.ACTIONS)

        return action

    def take_action(self, state, action):
        row, col = state

        if action == self.UP:
            row = max(row - 1, 0)
        elif action == self.DOWN:
            row = min(row + 1, self.height - 1)
        elif action == self.LEFT:
            col = max(col - 1, 0)
        elif action == self.RIGHT:
            col = min(col + 1, self.width - 1)

        if [row, col] in self.obstacles:
            row, col = state

        if [row, col] == self.end_state:
            reward = 1
        else:
            reward = 0

        return reward, [row, col]

    def add_obstacle(self, obstacle):
        new_obstacles = [[obstacle]]

        for old_obstacle in self.obstacles:
            new_obstacles.append(old_obstacle)

        self.obstacles = new_obstacles

    def remove_obstacle(self, obstacle):
        new_obstacles = []

        for old_obstacle in self.obstacles:
            if old_obstacle != obstacle:
                new_obstacles.append(old_obstacle)

        self.obstacles = new_obstacles

    def reset_q_values(self):
        self.q_values = np.zeros((self.height, self.width, len(self.ACTIONS)))


class ActionSelectionModel:

    def __init__(self, world):
        self.KAPPA = 0.0001

        self.world = world
        self.map = dict()
        self.global_time = 0

    def update(self, current_state, action, reward, next_state):
        self.global_time += 1

        if tuple(current_state) not in self.map.keys():
            self.map[tuple(current_state)] = dict()

            for default_action in self.world.ACTIONS:
                self.map[tuple(current_state)][default_action] = [0, current_state, 0]

        self.map[tuple(current_state)][action] = [reward, next_state, self.global_time]

    def draw_sample(self):
        state_index = np.random.choice(range(0, len(self.map.keys())))
        state = list(self.map)[state_index]
        best_action = None
        current_best_reward = -9999
        associated_reward = None
        associated_new_state = None
        associated_state = None

        for action_index in self.map[state]:
            action_key = list(self.map[state])[action_index]
            reward, new_state, time = self.map[state][action_key]
            adjusted_reward = reward + self.KAPPA * np.sqrt(self.global_time - time)

            if current_best_reward < adjusted_reward:
                associated_state = state
                best_action = action_index
                current_best_reward = adjusted_reward
                associated_reward = reward
                associated_new_state = new_state

        return list(associated_state), best_action, associated_reward, associated_new_state


class OrdinaryModel:

    def __init__(self, world):
        self.KAPPA = 0.0001

        self.world = world
        self.map = dict()
        self.global_time = 0

    def update(self, current_state, action, reward, next_state):
        self.global_time += 1

        if tuple(current_state) not in self.map.keys():
            self.map[tuple(current_state)] = dict()

            for default_action in self.world.ACTIONS:
                self.map[tuple(current_state)][default_action] = [0, current_state, 0]

        self.map[tuple(current_state)][action] = [reward, next_state, self.global_time]

    def draw_sample(self):
        state_index = np.random.choice(range(0, len(self.map.keys())))
        state = list(self.map)[state_index]
        action_index = np.random.choice(range(0, len(self.map[state].keys())))
        action = list(self.map[state])[action_index]
        reward, new_state, time = self.map[state][action]

        return list(state), action, reward, new_state


def traverse_world(world):
    models = [ActionSelectionModel(world), OrdinaryModel(world)]
    add_shortcut_at_step = 12500

    for model in models:
        current_state = world.start_state
        cumulative_reward = 0
        cumulative_rewards = []
        steps = 0
        max_steps = 25000
        current_steps = 0

        while steps < max_steps:
            if current_state == world.end_state:
                print(current_steps)
                current_state = world.start_state
                current_steps = 0

            action = world.get_action(current_state)
            reward, new_state = world.take_action(current_state, action)
            cumulative_reward += reward
            world.q_values[current_state[0], current_state[1], action] += \
                ALPHA * (reward + GAMMA * np.max(world.q_values[new_state[0], new_state[1], :])) - \
                world.q_values[current_state[0], current_state[1], action]

            model.update(current_state, action, reward, new_state)

            for step in range(0, PLANNING_STEPS):
                drawn_state, drawn_action, drawn_reward, drawn_new_state = model.draw_sample()
                world.q_values[drawn_state[0], drawn_state[1], drawn_action] += \
                    ALPHA * (drawn_reward + GAMMA * np.max(world.q_values[drawn_new_state[0], drawn_new_state[1], :])) - \
                    world.q_values[drawn_state[0], drawn_state[1], drawn_action]

            current_state = new_state
            steps += 1
            current_steps += 1
            cumulative_rewards.append(cumulative_reward)

            if steps == add_shortcut_at_step:
                world.remove_obstacle([3, 8])

        world.add_obstacle([3, 8])
        world.reset_q_values()

        plot_cumulative_rewards(cumulative_rewards, model)


def plot_cumulative_rewards(cumulative_rewards, model):
    x = np.arange(len(cumulative_rewards))
    y = cumulative_rewards
    plt.figure()
    plt.plot(x, y)
    plt.title(model)
    plt.xlabel('Time steps')
    plt.ylabel('Cumulative rewards')
    plt.show()

dyna_world = World(6, 9, [2, 0], [0, 8], [[1, 2], [2, 2], [3, 2], [4, 5], [0, 7], [1, 7], [2, 7]])
shortcut_world = World(6, 9, [5, 3], [0, 8], [[3, 1], [3, 2], [3, 3], [3, 4], [3, 5], [3, 6], [3, 7], [3, 8]])

traverse_world(shortcut_world)
