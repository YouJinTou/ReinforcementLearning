import numpy as np
import random
import matplotlib.pyplot as plt

WORLD = np.array(([
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
    ['.', '.', '.', '_', '_', '_', '__', '__', '_', '.'],
]))
ACTIONS = [
    (-1, +0),  # Up
    (-1, +1),  # Up-right
    (+0, +1),  # Right
    (+1, +1),  # Down-right
    (+1, +0),  # Down
    (+1, -1),  # Down-left
    (+0, -1),  # Left
    (-1, -1),  # Up-left
    (+0, +0)   # Stay
]
EPSILON = 0.1
ALPHA = 0.5
GAMMA = 1
REWARD = -1
START_STATE = (3, 0)
TERMINAL_STATE = (3, 7)


def init_action_values():
    action_values = {}
    rows, cols = WORLD.shape

    for row in range(rows):
        for col in range(cols):
            action_values[row, col] = {}

            for action in ACTIONS:
                new_state = np.add((row, col), action)
                is_within_boundaries = 0 <= new_state[0] < rows and 0 <= new_state[1] < cols

                if is_within_boundaries:
                    action_values[row, col][action] = 0

    return action_values


def do_sarsa(episodes):
    Q = init_action_values()
    episode_steps = []
    current_steps = 0

    for episode in range(episodes):
        state = START_STATE
        action = get_action(Q, state)

        while state != TERMINAL_STATE:
            new_state = get_new_state(state, action)
            new_action = get_action(Q, new_state)
            Q[state][action] += ALPHA * (REWARD + GAMMA * Q[new_state][new_action] - Q[state][action])
            state = new_state
            action = new_action
            current_steps += 1

        episode_steps.append(current_steps)

        print(current_steps)

    episode_steps = episode_steps[::-1]

    return episode_steps


def get_action(Q, state):
    is_greedy = np.random.random() > EPSILON
    action = max(Q[state], key=lambda a: Q[state][a]) if is_greedy else random.choice(list(Q[state]))

    return action


def get_new_state(state, action):
    no_wind = WORLD[state] == '.'
    wind_is_one = WORLD[state] == '_'

    if no_wind:
        new_state = tuple(np.add(state, action))
    elif wind_is_one:
        wind_of_one = (-1, 0)
        new_state = tuple(np.add(state, np.add(action, wind_of_one)))
    else:
        wind_of_two = (-2, 0)
        new_state = tuple(np.add(state, np.add(action, wind_of_two)))

    is_beyond_boundary = new_state[0] < 0

    if is_beyond_boundary:
        new_state = (0, new_state[1])

    return new_state


def plot_episode_steps(episode_steps):
    x = episode_steps
    y = np.arange(len(episode_steps))
    plt.figure()
    plt.plot(x, y)
    plt.xlabel('Time steps')
    plt.ylabel('Episodes')
    plt.show()


plot_episode_steps(do_sarsa(170))
