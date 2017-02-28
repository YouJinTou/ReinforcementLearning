import numpy as np
import operator as op

racetrack = np.array((
        ['X', 'X', 'X', 's', 's', 's', 's', 's', 's', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'X', 'X', 'X', 'X', 'X', 'X', 'X'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f'],

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
    start_loc = np.where(racetrack == 's')
    start_col = start_loc[1][0]
    end_col = start_loc[1][len(start_loc[1]) - 1]
    state = (0, np.random.randint(start_col, end_col + 1))

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
    h_velocity = 0
    v_velocity = 0

    while True:
        random_h = np.random.choice(h_actions)
        random_v = np.random.choice(v_actions)
        h_velocity += random_h
        v_velocity += random_v

        if h_velocity < 0 or v_velocity < 0 or (0 == h_velocity == v_velocity):
            h_velocity -= random_h
            v_velocity -= random_v

            continue

        if h_velocity >= VELOCITY_THRESHOLD:
            h_velocity -= 1

        if v_velocity >= VELOCITY_THRESHOLD:
            v_velocity -= 1

        if has_finished(state):
            break

        is_within_bounds = (state[0] + v_velocity < max_row and state[1] + h_velocity < max_col) and \
                           (state[0] + v_velocity >= 0 and state[1] + h_velocity >= 0)

        if not is_within_bounds:
            h_velocity -= random_h
            v_velocity -= random_v

            continue

        action = [v_velocity, h_velocity]
        new_state = np.add(state, action)

        if has_collided(new_state):
            state = get_random_start_pos()
            h_velocity = 0
            v_velocity = 0

            continue

        episode.append((state, action, reward))

        #print_current_racetrack(new_state, current_racetrack)

        state = new_state

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
    start_row = 0

    if state[0] != start_row:
        current_racetrack[state[0], state[1]] = 'O'

    print(current_racetrack)


def has_finished(state):
    first_finish_row = 26
    last_finish_row = 31
    finish_line = 16

    if first_finish_row <= state[0] <= last_finish_row and state[1] >= finish_line:
        return True

    return False


def has_collided(state):
    return racetrack[state[0], state[1]] == 'X'


do_incremental_off_policy_every_visit_monte_carlo_evaluation()
