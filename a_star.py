import heapq
import math
import copy


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0
        self.h = 0
        self.f = 0

    def __lt__(self, other):
        return self.f < other.f

def assignment_number(node, number, visual_grid, anim_frames=None):
    visual_grid[node[0]][node[1]] = number
    if anim_frames != None:
        anim_frames.append(copy.deepcopy(visual_grid))


def read_grid(file_path):
    with open(file_path, 'r') as file:
        grid = [list(map(int, line.strip().split())) for line in file]
    return grid


def get_neighbors(node, grid):
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    neighbors = []
    for direction in directions:
        row = node.position[0] + direction[0]
        col = node.position[1] + direction[1]
        if 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] == 0:
            neighbors.append((row, col))

    return neighbors


def heuristic(current, goal):
    #return abs(current[0] - goal[0]) + abs(current[1] - goal[1])
    return math.sqrt((current[0] - goal[0])**2 + (current[1] - goal[1])**2)

def reconstruction_path(current_node):
    path = []
    while current_node:
        path.append(current_node.position)
        current_node = current_node.parent

    return path[::-1]


def a_star_with_animation(grid, start, goal, anim_frames):
    open_list = []
    closed_set = set()
    visual_grid = copy.deepcopy(grid)
    assignment_number(start, 1, visual_grid)
    assignment_number(goal, 2, visual_grid, anim_frames)
    heapq.heappush(open_list, Node(start))

    while open_list:
        current_node = open_list.pop(0)


        if current_node.position == goal:
            path = reconstruction_path(current_node)
            #assignment_number(current_node.position, 4, anim_frames, visual_grid)   # zielony reconstruction gridd
            visual_grid[goal[0]][goal[1]] = 2   # niebieski meta
            # ustawia kolory i robi klatki
            for pos in path:
                assignment_number(pos, 4, visual_grid, anim_frames)
            assignment_number(start, 1, visual_grid, anim_frames)
            assignment_number(goal, 2, visual_grid, anim_frames)
            return path, visual_grid

        closed_set.add(current_node.position)
        #nie pozwala aby nadpisał się kolor startu
        if current_node.position != start:
            assignment_number(current_node.position, 7, visual_grid, anim_frames)# ustawia current note jako czerwony
        for neighbor_pos in get_neighbors(current_node, grid):

            if neighbor_pos in closed_set:
                continue
            neighbor_node = Node(neighbor_pos, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor_pos, goal)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if any(open_node.position == neighbor_node.position and open_node.f <= neighbor_node.f for open_node in open_list):
                continue
            # ustawia kolor dla NOWYCH sąsiadów, niebieski
            assignment_number(neighbor_pos, 3, visual_grid, anim_frames)

            heapq.heappush(open_list, neighbor_node)


    return []

if __name__ == "__main__":
    file_path = "C:/Users/1/Desktop/AstarPB/grid.txt"
    grid = read_grid(file_path)
    start = (len(grid) - 1, 0)
    goal = (0, len(grid[0]) - 1)
    # ten visual grid w porównaniu visual grid w pliku visualization.py jest po
    # prostu do tego aby wyświetlić w konsoli graf
    visual_grid = []
    anim_frames = []

    path = a_star_with_animation(grid, start, goal, anim_frames)
    print("zwykły grid")
    [print(line) for line in grid]
    #zamienia cyfry tak aby została sama droga od startu do mety i nadpisuje path[1](czyli wynik reconstruction_path[1])
    for row_index, row in enumerate(path[1]):
        for col_index, value in enumerate(row):
            # Wszystko inne zmieniamy na 0
            if value not in (0, 1, 2, 4, 5):
                path[1][row_index][col_index] = 0

    print("visual")
    [print(line) for line in path[1]]


    print(path)