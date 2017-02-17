import numpy as np
import matplotlib.pyplot as plt

STATES = 100

states = np.arange(STATES + 1)
state_values = np.zeros(STATES + 1)
state_values[100] = 1
policies = np.zeros(STATES + 1)
p_win = 0.25


def do_value_iteration():
    epsilon = 1e-20

    while True:
        delta = 0.0

        for state in states[1:STATES]:
            actions = np.arange(1, min(state, STATES - state) + 1)
            action_values = []

            for action in actions:
                action_value = p_win * state_values[state + action] + (1 - p_win) * state_values[state - action]
                action_values.append(action_value)

            state_value = np.max(action_values)
            delta += np.abs(state_values[state] - state_value)
            state_values[state] = state_value
        if delta < epsilon:
            break


def get_optimal_policy():
    for state in states[1:STATES]:
        actions = np.arange(1, min(state, STATES - state) + 1)
        action_values = []

        for action in actions:
            action_value = p_win * state_values[state + action] + (1 - p_win) * state_values[state - action]
            action_values.append(action_value)

        policies[state] = actions[np.argmax(action_values)]


def plot_figures():
    plt.figure(1)
    plt.title('p = ' + str(p_win))
    plt.xlabel('Capital')
    plt.ylabel('Value estimates')
    plt.plot(state_values)

    plt.figure(2)
    plt.title('p = ' + str(p_win))
    plt.scatter(states, policies)
    plt.xlabel('Capital')
    plt.ylabel('Final policy (stake)')
    axes = plt.gca()
    axes.set_xlim([1, 99])
    axes.set_ylim([0, max(policies) + 5])

    plt.show()

do_value_iteration()
get_optimal_policy()
plot_figures()

