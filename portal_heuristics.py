
# Author: Ben Williams '25
# Date: November 23rd, 2023

# Does not consider the position of the portals at all
def portal_manhattan_heuristic(state, goal):
    return abs(goal[0] - state[0]) + abs(goal[1] - state[1])


def manhattan_including_portals(state, goal):
    if not state[2] or not state[3]:
        return portal_manhattan_heuristic(state, goal)

    here_to_portal_1 = abs(state[2][0] - state[0]) + abs(state[2][1] - state[1])
    here_to_portal_2 = abs(state[3][0] - state[0]) + abs(state[3][1] - state[1])

    portal_1_to_goal = abs(goal[0] - state[2][0]) + abs(goal[1] - state[2][1])
    portal_2_to_goal = abs(goal[0] - state[3][0]) + abs(goal[1] - state[3][1])

    best_distance_to_goal = min(here_to_portal_1 + portal_2_to_goal, here_to_portal_2 + portal_1_to_goal)

    return min(best_distance_to_goal * 1.25, portal_manhattan_heuristic(state, goal))






