from collections import deque

from PortalMap import PortalMap
import time

# Author: Ben Williams - benjamin.r.williams.25@dartmouth.edu
# Date: November 22nd, 2023


class PortalProblem:
    # Parameters: portal_map is a PortalMap object, start and goal are (x, y) tuples
    def __init__(self, portal_map):
        self.portal_map = portal_map

    # BFS search to find a solution. Slow, but good for comparison
    # Takes a start and goal (x, y) tuple as parameter
    def find_solution_bfs(self, start, goal, print_info=False):
        # Setup
        start_state = (start[0], start[1], None, None)
        backchain = {start_state: None}
        queue = deque()
        goal_found = False

        # Need to differentiate as the goal state will contain more than just the (x, y) coordinates
        goal_state = None
        nodes_searched = 0

        # The BFS
        queue.append(start_state)
        while len(queue) > 0:
            curr_state = queue.popleft()
            nodes_searched += 1

            if self.is_goal_state(curr_state, goal):
                goal_found = True
                goal_state = curr_state
                break

            for successor in self.get_successors(curr_state):
                if successor in backchain.keys():
                    continue
                backchain[successor] = curr_state
                queue.append(successor)

        if not goal_found:
            print(f"No solution found after {nodes_searched} nodes searched")
            return None

        # Now backchain
        path = []
        curr_state = goal_state
        while curr_state:
            path.append(curr_state)
            curr_state = backchain[curr_state]
        path.reverse()

        if print_info:
            print(f"Solution found with {nodes_searched} nodes searched")

        return path

    # Given a state (x, y, portal 1, portal 2), get all possible successors
    def get_successors(self, state):
        valid_states = []

        # Consider moving
        for x_mov in range(-1, 2):
            for y_mov in range(-1, 2):
                if abs(x_mov) + abs(y_mov) != 1:
                    continue
                possible_loc = (state[0] + x_mov, state[1] + y_mov)
                # Is a floor space
                if self.portal_map.is_floor(possible_loc):
                    new_state = (possible_loc[0], possible_loc[1], state[2], state[3])
                    valid_states.append(new_state)
                    continue

        # Consider going through a portal if we can
        if state[2] and state[3]:

            if self.portal_map.can_move_through_portal((state[0], state[1]), state[2]):
                new_loc = self.portal_map.get_portal_destination(state[3])
                valid_states.append((new_loc[0], new_loc[1], state[2], state[3]))

            if self.portal_map.can_move_through_portal((state[0], state[1]), state[3]):
                new_loc = self.portal_map.get_portal_destination(state[2])
                valid_states.append((new_loc[0], new_loc[1], state[2], state[3]))

        # Consider making new portals
        possible_portal_walls = self.portal_map.get_portalable_walls((state[0], state[1]))
        for portalable_wall in possible_portal_walls:
            # Ignore walls we have already portaled
            if portalable_wall == state[2] or portalable_wall == state[3]:
                continue

            # Fill empty portal slots first
            if not state[2]:
                valid_states.append((state[0], state[1], portalable_wall, state[3]))
                continue
            if not state[3]:
                valid_states.append((state[0], state[1], state[2], portalable_wall))
                continue

            valid_states.append((state[0], state[1], state[2], portalable_wall))
            valid_states.append((state[0], state[1], portalable_wall, state[3]))

        return valid_states

    # Prints out a series of mazes
    def illustrate_solution(self, solution):
        print(f"Started at {(solution[0][0], solution[0][1])}")
        self.portal_map.illustrate_map_state(solution[0])
        time.sleep(1)
        for i in range(1, len(solution)):
            print(f'State: {solution[i]}')
            print(self.__determine_move(solution[i - 1], solution[i]))
            self.portal_map.illustrate_map_state(solution[i])
            time.sleep(1)


    @staticmethod
    # Returns a string of the move made between the two states
    def __determine_move(state1, state2):
        # Moved sideways
        if state1[0] != state2[0]:
            if state1[0] == state2[0] - 1:
                return "Robot moved right"
            elif state1[0] == state2[0] + 1:
                return "Robot moved left"
            else:
                return 'Robot went through a portal'

        # Moved up or down
        if state1[1] != state2[1]:
            if state1[1] == state2[1] - 1:
                return "Robot moved down"
            elif state1[1] == state2[1] + 1:
                return "Robot moved up"
            else:
                return "Robot went through a portal"

        # Placed a portal
        directions = {"l": "left", "r": "right", "u": "up", "d": "down"}

        if state1[2] != state2[2]:
            string = f"Robot placed its first portal at {(state2[2][0], state2[2][1])} facing {directions[state2[2][2]]}"
            return string

        if state1[3] != state2[3]:
            string = f"Robot placed its second portal at {(state2[3][0], state2[3][1])} facing {directions[state2[2][2]]}"
            return string

    @staticmethod
    def is_goal_state(state, goal):
        return state[0] == goal[0] and state[1] == goal[1]


# Some tests on simple maps to make sure the basics are working
if __name__ == "__main__":
    # pmap = PortalMap("./maps/smallMap")
    # portal_prob = PortalProblem(pmap)
    # print(portal_prob.get_successors((6, 1, None, None)))
    # print(portal_prob.get_successors((6, 1, (3, 1, 'r'), None)))
    # print(portal_prob.get_successors((6, 1, (3, 1, 'r'), (6, 0, 'd'))))
    # print(portal_prob.find_solution_bfs((6, 1), (0, 1)))

    # pmap2 = PortalMap("./maps/portalsRequiredSmall")
    # portal_prob2 = PortalProblem(pmap2)
    # path = portal_prob2.find_solution_bfs((6, 3), (0, 1), print_info=True)
    # portal_prob2.illustrate_solution(path)

    pmap3 = PortalMap("./maps/longSkip")
    portal_prob3 = PortalProblem(pmap3)
    path = portal_prob3.find_solution_bfs((pmap3.width - 1, 0), (0, 0), True)
    portal_prob3.illustrate_solution(path)

    # print(portal_prob.find_solution_bfs((6, 1), (0, 1)))



