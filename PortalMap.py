import sys


# Author: Ben Williams - benjamin.r.williams.25@dartmouth.edu
# Date: November 22nd, 2023

class PortalMap:
    def __init__(self, map_file_loc):
        # Will be built into a 2D grid
        self.map = []
        try:
            with open(map_file_loc, "r") as f:
                for line in f:
                    line = line.strip()

                    # Ignore blank lines
                    if len(line) == 0:
                        continue

                    locations = line.split(" ")

                    self.map.append(locations)

                # Use the lines to store the map
                self.width = len(self.map[0])
                self.height = len(self.map)

        except FileNotFoundError:
            print("Map file not found", sys.stderr)

    # Looks up, down, left, and right, to see if there are any portalable walls
    # Cannot portal through walls
    def get_portalable_walls(self, robot_loc):
        portalable_walls = []
        x = robot_loc[0]
        y = robot_loc[1]

        # Look up
        for upward_loc in range(y - 1, -1, -1):
            if "d" in self.map[upward_loc][x]:
                portalable_walls.append((x, upward_loc, "d"))
                break
            # We are looking at a wall
            elif "#" in self.map[upward_loc][x]:
                break

        # Look down
        for downward_loc in range(y + 1, self.height):
            if "u" in self.map[downward_loc][x]:
                portalable_walls.append((x, downward_loc, "u"))
                break
            elif "#" in self.map[downward_loc][x]:
                break

        # Look left
        for leftward_loc in range(x - 1, -1, -1):
            if "r" in self.map[y][leftward_loc]:
                portalable_walls.append((leftward_loc, y, "r"))
                break
            elif "#" in self.map[y][leftward_loc]:
                break

        # Look right
        for rightward_loc in range(x + 1, self.width):
            if "l" in self.map[y][rightward_loc]:
                portalable_walls.append((rightward_loc, y, "l"))
                break
            elif "#" in self.map[y][rightward_loc]:
                break

        return portalable_walls

    # Put a portal on the wall on the appropriate side of the wall with respect to the robot's location
    def portal_wall(self, robot_loc, wall_loc):
        # Portaled from the left side
        if wall_loc[0] > robot_loc[0]:
            self.map[wall_loc[1]][wall_loc[0]] = "L" + self.map[wall_loc[1]][wall_loc[0]][1:]

        # Portaled from the right side
        if wall_loc[0] < robot_loc[0]:
            self.map[wall_loc[1]][wall_loc[0]] = self.map[wall_loc[1]][wall_loc[0]][0] + "R" + \
                                                 self.map[wall_loc[1]][wall_loc[0]][2:]

        # Portaled from above
        if wall_loc[1] > robot_loc[1]:
            self.map[wall_loc[1]][wall_loc[0]] = self.map[wall_loc[1]][wall_loc[0]][0:2] + "U" + \
                                                 self.map[wall_loc[1]][wall_loc[0]][3]

        # Portaled from below
        if wall_loc[1] < robot_loc[1]:
            self.map[wall_loc[1]][wall_loc[0]] = self.map[wall_loc[1]][wall_loc[0]][0:3] + "D"

    # Removes all portals from a wall
    def unportal_wall(self, wall_loc):
        self.map[wall_loc[1]][wall_loc[0]] = self.map[wall_loc[1]][wall_loc[0]].lower()

    # Returns True if the location is a floor space, False otherwise
    def is_floor(self, loc):
        if not 0 <= loc[0] < self.width:
            return False
        if not 0 <= loc[1] < self.height:
            return False

        return self.map[loc[1]][loc[0]] == "____"

    @staticmethod
    # If you can move through a portal, returns True. False otherwise.
    def can_move_through_portal(robot_loc, portal_info):
        # Quick check to make sure we are adjacent
        if abs(robot_loc[0] - portal_info[0]) + abs(robot_loc[1] - portal_info[1]) > 1:
            return False

        # Grab the specific parts of the portal's info
        portal_loc = (portal_info[0], portal_info[1])
        portal_orientation = portal_info[2]

        if (robot_loc[0] + 1, robot_loc[1]) == portal_loc:
            return portal_orientation == "l"

        if (robot_loc[0] - 1, robot_loc[1]) == portal_loc:
            return portal_orientation == "r"

        if (robot_loc[0], robot_loc[1] + 1) == portal_loc:
            return portal_orientation == "u"

        if (robot_loc[0], robot_loc[1] - 1) == portal_loc:
            return portal_orientation == "d"

        return False

    # Takes a triple (x, y, dir) as parameter, and returns the space that the portal would put you on
    # dir needs to be in {"l", "r", "u", "d"}
    def get_portal_destination(self, portal_loc):
        if portal_loc[2] in self.map[portal_loc[1]][portal_loc[0]]:
            if portal_loc[2] == "l":
                return portal_loc[0] - 1, portal_loc[1]
            if portal_loc[2] == "r":
                return portal_loc[0] + 1, portal_loc[1]
            if portal_loc[2] == "u":
                return portal_loc[0], portal_loc[1] - 1
            if portal_loc[2] == "d":
                return portal_loc[0], portal_loc[1] + 1

    # Prints out an illustration of the map as ascii art
    def illustrate_map_state(self, state):
        map_string = ""
        for row in range(self.height):
            for col in range(self.width):
                # Check for the robot
                if (col, row) == (state[0], state[1]):
                    map_string += "<{}> "
                    continue
                # Check for the first portal
                if state[2]:
                    if (col, row) == (state[2][0], state[2][1]):
                        for char in self.map[row][col]:
                            if char == state[2][2]:
                                map_string += char.upper()
                            else:
                                map_string += char
                        map_string += " "
                        continue
                # Check for the second portal
                if state[3]:
                    if (col, row) == (state[3][0], state[3][1]):
                        for char in self.map[row][col]:
                            if char == state[3][2]:
                                map_string += char.upper()
                            else:
                                map_string += char
                        map_string += " "
                        continue
                # Otherwise, just put down the location's normal information
                map_string += self.map[row][col] + " "
            map_string += "\n"

        print(map_string)


# Some tests
if __name__ == "__main__":
    small_map = PortalMap("./maps/smallMap")

    p_loc_1 = small_map.get_portalable_walls((6, 1))
    for p_wall in p_loc_1:
        small_map.portal_wall((6, 1), (p_wall[0], p_wall[1]))
    print(p_loc_1)

    small_map.illustrate_map_state((6, 1))
    print(small_map.can_move_through_portal((6, 1), p_loc_1[0]))
    print(small_map.can_move_through_portal((6, 1), p_loc_1[1]))
    print(small_map.get_portal_destination(p_loc_1[0]))
    print(small_map.get_portal_destination(p_loc_1[1]))

    small_map.illustrate_map_state((6, 1))

