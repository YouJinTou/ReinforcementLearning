import numpy as np
from math import *

CREDIT = 10
MOVE_COST = 2
MAX_TOTAL_CARS = 20
MAX_MOVE_CARS = 5
GAMMA = 0.9
REQUESTS_FIRST_LOC = 3
REQUESTS_SECOND_LOC = 4
RETURNS_FIRST_LOC = 3
RETURNS_SECOND_LOC = 2
POISSON_MAX = 9

actions = np.arange(-MAX_MOVE_CARS, MAX_MOVE_CARS + 1)
policy = np.zeros((MAX_TOTAL_CARS + 1, MAX_TOTAL_CARS + 1))
state_values = np.zeros((MAX_TOTAL_CARS + 1, MAX_TOTAL_CARS + 1))
states = []


def init_states():
    for i in range(0, MAX_TOTAL_CARS + 1):
        for j in range(0, MAX_TOTAL_CARS + 1):
            states.append([i, j])


def policy_converged():
    new_state_values = np.zeros((MAX_TOTAL_CARS + 1, MAX_TOTAL_CARS + 1))
    for f_loc, s_loc in states:
        new_state_values[f_loc, s_loc] = get_state_value([f_loc, s_loc], policy[f_loc, s_loc])
    state_values[:] = new_state_values
    convergence = np.sum(np.abs(state_values, new_state_values))
    epsilon = 1e-4
    return True if (convergence < epsilon) else False


def improve_policy():
    new_policy = np.zeros((MAX_TOTAL_CARS + 1, MAX_TOTAL_CARS + 1))
    for f_loc, s_loc in states:
        values = []
        for action in actions:
            values.append(get_state_value([f_loc, s_loc], action))
        best_action = np.argmax(values)
        new_policy[f_loc, s_loc] = actions[best_action]
    return new_policy


def poisson(x, lam):
    return (pow(lam, x) * exp(-lam)) / factorial(x)


def get_state_value(state, action):
    revenue = action * (-MOVE_COST)
    for request_first in range(0, POISSON_MAX):
        for request_second in range(0, POISSON_MAX):
            first_loc_cars_after_move = state[0] - action
            second_loc_cars_after_move = state[1] + action

            reward = (request_first + request_second) * CREDIT
            p = poisson(request_first, REQUESTS_FIRST_LOC) * poisson(request_second, REQUESTS_SECOND_LOC)

            for return_first in range(0, POISSON_MAX):
                for return_second in range(0, POISSON_MAX):
                    first_loc_cars_after_move = min(first_loc_cars_after_move + return_first, MAX_TOTAL_CARS)
                    second_loc_cars_after_move = min(second_loc_cars_after_move + return_second, MAX_TOTAL_CARS)

                    p *= poisson(return_first, RETURNS_FIRST_LOC) * poisson(return_second, RETURNS_SECOND_LOC)
                    revenue += \
                        (p * (reward + GAMMA * state_values[first_loc_cars_after_move, second_loc_cars_after_move]))
    return revenue


def find_optimal_policy():
    should_improve = False
    while True:
        if should_improve:
            converged = policy_converged()
            if converged:
                break

        new_policy = improve_policy()
        policy_stable = (np.sum(policy != new_policy) == 0)
        global policy
        policy = new_policy

        if not policy_stable:
            should_improve = True


init_states()
find_optimal_policy()
