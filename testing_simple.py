from PortalMap import PortalMap
from PortalProblem import PortalProblem
from improved_search import portal_astar_search
from portal_heuristics import portal_manhattan_heuristic, manhattan_including_portals

# Author: Ben Williams - benjamin.r.williams.25@dartmouth.edu
# Date: November 23rd, 2023

mediumMap = PortalMap("./maps/mediumMap")
mediumProblem = PortalProblem(mediumMap)
# path = mediumProblem.find_solution_bfs((mediumMap.width - 2, 0), (0, 0), True)
# mediumProblem.illustrate_solution(path)
mediumProblem.find_solution_bfs((mediumMap.width - 2, 0), (0, 0), True)
portal_astar_search(mediumProblem, (mediumMap.width - 2, 0), (0, 0), portal_manhattan_heuristic, print_info=True)
path = portal_astar_search(mediumProblem, (mediumMap.width - 2, 0), (0, 0), manhattan_including_portals, print_info=True)
mediumProblem.illustrate_solution(path)



