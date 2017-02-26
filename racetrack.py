import numpy as np
import operator as op

racetrack = np.array((
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', 's', 's', 's', 's', 's', 's', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
    ))
h_actions = [1, -1, 0]
v_actions = [1, -1, 0]
VELOCITY_THRESHOLD = 5


def init_policies():
    rows, cols = racetrack.shape
    target_policy = {}
    behavior_policy = {}
    h_t_velocity = h_actions[2]
    h_b_velocity = h_actions[0]
    v_t_velocity = v_actions[0]
    v_b_velocity = v_actions[0]
    h_zero = h_actions[2]
    v_zero = v_actions[2]

    for row in range(rows):
        for col in range(cols):
            target_policy[row, col] = [h_t_velocity, v_t_velocity] if (row != rows - 1) else [h_zero, v_zero]
            behavior_policy[row, col] = [h_b_velocity, v_b_velocity] if (row != rows - 1) else [h_zero, v_zero]

    return target_policy, behavior_policy


def get_random_start_pos():
    num_rows, num_cols = racetrack.shape
    start_loc = np.where(racetrack == 's')
    start_col = start_loc[1][0]
    end_col = start_loc[1][len(start_loc[1]) - 1]
    state = (num_rows - 1, np.random.randint(start_col, end_col + 1))

    return state


def do_incremental_off_policy_every_visit_monte_carlo_evaluation():
    target_policy, behavior_policy = init_policies()
    Q = init_q_state_action_values()
    C = init_cumulative_weights()

    while True:
        episode = generate_behavior_policy_episode(behavior_policy)


def init_q_state_action_values():
    Q = {}
    rows, cols = racetrack.shape

    for row in range(rows):
        for col in range(cols):
            Q[row, col] = 0

    return Q


def init_cumulative_weights():
    C = {}
    rows, cols = racetrack.shape

    for row in range(rows):
        for col in range(cols):
            C[row, col] = 0

    return C


def generate_behavior_policy_episode(behavior_policy):
    episode = []
    current_racetrack = racetrack
    reward = -1
    state = get_random_start_pos()
    max_row, max_col = racetrack.shape

    while True:
        if has_collided(state):
            state = get_random_start_pos()

        h_action = np.random.choice(h_actions)
        v_action = np.random.choice(v_actions)
        action = [h_action, v_action]
        new_state_value = np.add(behavior_policy[state], action)
        is_valid_action = all_are_less_than_velocity_threshold(new_state_value) and \
            all_are_greater_equal_to_zero(new_state_value) and not \
            (0 == new_state_value[0] == new_state_value[1])
        is_within_bounds = (state[0] + -v_action < max_row and state[1] + -h_action < max_col) and \
            (state[0] + -v_action >= 0 and state[1] + -h_action >= 0)

        if not is_valid_action or not is_within_bounds:
            continue

        episode.append((state, action, reward))

        print_current_racetrack(state, current_racetrack)

        if has_finished(state):
            break

        behavior_policy[state] = new_state_value
        state = tuple(map(op.add, state, -new_state_value))

    return episode


def all_are_greater_equal_to_zero(state_values):
    for i in state_values:
        if i < 0:
            return False

    return True


def all_are_less_than_velocity_threshold(state_values):
    for i in state_values:
        if i >= VELOCITY_THRESHOLD:
            return False
        
    return True


def print_current_racetrack(state, current_racetrack):
    start_row = 31

    if state[0] != start_row:
        current_racetrack[state] = 'O'

    print(current_racetrack)


def has_finished(state):
    return racetrack[state[0], state[1]] == 'f'


def has_collided(state):
    return racetrack[state[0], state[1]] == 'X'


do_incremental_off_policy_every_visit_monte_carlo_evaluation()
