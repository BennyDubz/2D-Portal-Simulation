from heapq import heappush, heappop

# Author: Ben Williams - benjamin.r.williams.25@dartmouth.edu
# Date: November 23rd, 2023

# Using Astar search and more importantly heuristics to try to solve the portal problem faster
# Some Astar stuff taken from my Maze-solving project


class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        self.state = state
        # Heuristic cost
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # heuristic + actual cost
        return self.heuristic + self.transition_cost

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()


# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


# Uses Astar search with a given heuristic to solve the portal problem
# Takes (x, y) tuples for start and goal locations
# Heuristic needs to take the portal state (x, y, portal 1, portal 2) and goal (x, y) as parameters
def portal_astar_search(portal_problem, start, goal, heuristic_fn, print_info=False):
    start_state = (start[0], start[1], None, None)

    start_node = AstarNode(start_state, heuristic_fn(start_state, goal))
    pqueue = []
    heappush(pqueue, start_node)
    nodes_visited = 0

    # Does not account for heuristic
    visited_cost = {start_state: 0}

    while len(pqueue) > 0:
        current_node = heappop(pqueue)

        # Do not consider nodes that already have a better path to them than the current one
        if visited_cost[current_node.state] + heuristic_fn(current_node.state, goal) < current_node.priority():
            continue

        nodes_visited += 1

        if portal_problem.is_goal_state(current_node.state, goal):
            path = backchain(current_node)
            if print_info:
                print(f"Solution found with {nodes_visited} nodes visited with the {heuristic_fn.__name__} heuristic")
            return path

        for state in portal_problem.get_successors(current_node.state):
            new_visited_cost = visited_cost[current_node.state] + 1
            # If we have not seen it yet, then add the node to the pqueue
            if state not in visited_cost.keys():
                # Figure out the cost, wrap it into a node, and add it to the pqueue
                new_node = AstarNode(state, heuristic_fn(state, goal), current_node, new_visited_cost)
                # Find the cost between this node and the next
                visited_cost[state] = new_visited_cost
                heappush(pqueue, new_node)
            # If we have seen it, only add it if the cost is better
            else:
                if new_visited_cost + 1 < visited_cost[state]:
                    new_node = AstarNode(state, heuristic_fn(state, goal), current_node, new_visited_cost)
                    visited_cost[state] = new_visited_cost
                    heappush(pqueue, new_node)

    # No solution found
    if print_info:
        print(f"No solution found after examining {nodes_visited} nodes")

    return None


