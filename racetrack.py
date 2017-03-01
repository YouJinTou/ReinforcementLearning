import numpy as np
import operator as op

RACETRACK = np.array((
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
        ['X', 'X', 'X', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', '_', 'f']))
H_ACTIONS = [1, -1, 0]
V_ACTIONS = [1, -1, 0]
VELOCITY_THRESHOLD = 5


def init_policies():
    rows, cols = RACETRACK.shape
    target_policy = {}
    behavior_policy = {}
    h_t_velocity = H_ACTIONS[2]
    h_b_velocity = H_ACTIONS[0]
    v_t_velocity = V_ACTIONS[0]
    v_b_velocity = V_ACTIONS[0]
    h_zero = H_ACTIONS[2]
    v_zero = V_ACTIONS[2]

    for row in range(rows):
        for col in range(cols):
            target_policy[row, col] = (h_t_velocity, v_t_velocity) if (row != 0) else (h_zero, v_zero)
            behavior_policy[row, col] = (h_b_velocity, v_b_velocity) if (row != 0) else (h_zero, v_zero)

    return target_policy, behavior_policy


def init_q_state_action_values():
    Q = {}
    rows, cols = RACETRACK.shape

    for row in range(rows):
        for col in range(cols):
            Q[row, col] = {}

            for v_action in V_ACTIONS:
                for h_action in H_ACTIONS:
                    Q[row, col][v_action, h_action] = 0

    return Q


def init_cumulative_weights():
    C = {}
    rows, cols = RACETRACK.shape

    for row in range(rows):
        for col in range(cols):
            C[row, col] = {}

            for v_action in V_ACTIONS:
                for h_action in H_ACTIONS:
                    C[row, col][v_action, h_action] = 0

    return C


def get_random_start_pos():
    start_loc = np.where(RACETRACK == 's')
    start_col = start_loc[1][0]
    end_col = start_loc[1][len(start_loc[1]) - 1]
    state = (0, np.random.randint(start_col, end_col + 1))

    return state


def do_incremental_off_policy_every_visit_monte_carlo_evaluation():
    target_policy, behavior_policy = init_policies()
    Q = init_q_state_action_values()
    C = init_cumulative_weights()
    behavior_policy_action_prob = 0.33
    gamma = 1.0
    runs = 10000
    current_run = 0

    while current_run < runs:
        print("Run: " + str(current_run + 1))

        episode = generate_behavior_policy_episode()
        G = 0.0
        W = 1.0

        for e in reversed(episode):
            state = (e[0][0], e[0][1])
            action = e[1]
            reward = e[2]
            G += (gamma * G + reward)
            C[state][action] += W
            Q[state][action] += (W / C[state][action]) * (G - Q[state][action])
            target_policy[state] = get_max_action_in_state(Q, state)

            if target_policy[state] != action:
                break

            W *= 1.0 / behavior_policy_action_prob

        current_run += 1

    return Q, target_policy


def get_max_action_in_state(Q, state):
    best_action = None
    current_best_value = -999999

    for action in Q[state]:
        if Q[state][action] > current_best_value:
            current_best_value = Q[state][action]
            best_action = action

    return best_action


def has_finished(state):
    first_finish_row = 26
    last_finish_row = 31
    finish_col = 16

    if first_finish_row <= state[0] <= last_finish_row and state[1] >= finish_col:
        return True

    return False


def has_collided(state):
    return RACETRACK[state[0], state[1]] == 'X'


def generate_behavior_policy_episode():
    episode = []
    reward = -1
    state = get_random_start_pos()
    max_row, max_col = RACETRACK.shape
    h_velocity = 0
    v_velocity = 0

    while True:
        random_h = np.random.choice(H_ACTIONS)
        random_v = np.random.choice(V_ACTIONS)
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

        action = (v_velocity, h_velocity)
        new_state = tuple(np.add(state, action))

        if has_finished(new_state):
            break

        is_within_bounds = (state[0] + v_velocity < max_row and state[1] + h_velocity < max_col) and \
                           (state[0] + v_velocity >= 0 and state[1] + h_velocity >= 0)

        if not is_within_bounds or has_collided(new_state):
            state = get_random_start_pos()
            h_velocity = 0
            v_velocity = 0

            continue

        episode.append((state, (random_v, random_h), reward))

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


do_incremental_off_policy_every_visit_monte_carlo_evaluation()
