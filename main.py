"""
There's a maze defined as a text file, with the dimensions X * Y (it can be any maze of any size)
 made of the following
characters:
X - wall
" " (space) - road
0 - starting point
F - finish
Write a program in Python which is able to find the shortest path through the maze from the point
marked with the "0"
character and finishing at the point marked with "F".
Print out the shortest path found as the result, on the screen.
"""

import argparse
from collections import deque
from typing import NamedTuple, List, IO


class Solution(NamedTuple):
    """
    Simple class representing found solution
    """

    maze: List[List[str]]
    steps: int
    method: str


class Point(NamedTuple):
    """
    Simple class representing point in maze
    """

    x: int
    y: int


def read_maze(maze_file: IO[str]) -> List[List[str]]:
    """
    Read file with the maze and covert it to 2d array
    """
    return [[c for c in line if c != "\n"] for line in maze_file]


def print_maze(maze: List[List[str]]) -> None:
    """
    Prin maze 2d array
    """
    for line in maze:
        for char in line:
            if char in ("-", "|", "0", "F", "#"):
                print(char, end="")
            else:
                print(" ", end="")
        print()


def find_point(maze: List[List[str]], char: str) -> Point:
    """
    Find character 'char' in the maze. Using for finding start and end point
    """
    for y_coord, line in enumerate(maze):
        try:
            return Point(line.index(char), y_coord)
        except ValueError:
            pass
    raise ValueError(f"Maze doesnt have point with '{char}' character")


def solve_with_bfs(maze: List[List[str]]) -> Solution:
    """
    Find shortes path in the maze with Breadth-first search algorithm
    """
    start_point = find_point(maze, "0")
    end_point = find_point(maze, "F")
    points = deque()
    points.append(start_point)

    while points:
        current_point = points.popleft()
        if current_point == end_point:
            break
        points.extend(make_steps(maze, current_point))

    step_count = find_shortest_path(maze, end_point)
    return Solution(maze=maze, steps=step_count, method="bfs")


def can_make_step(
    maze: List[List[str]], x: int, y: int, maze_len_x: int, maze_len_y: int
) -> bool:
    """
    Check if can make step
    """
    return is_safe(x, y, maze_len_x, maze_len_y) and (
        maze[y][x] == " " or maze[y][x] == "F"
    )


def is_safe(x: int, y: int, x_len: int, y_len: int) -> bool:
    """
    Check if index is not out of the range
    """
    return 0 <= x < x_len and 0 <= y < y_len


def make_steps(maze: List[List[str]], current_point: Point) -> List[Point]:
    """
    Look arround and make steps in four directions
    """
    current_step = int(maze[current_point.y][current_point.x])
    next_points = []

    # step left
    if can_make_step(
        maze,
        current_point.x - 1,
        current_point.y,
        len(maze[current_point.y]),
        len(maze),
    ):
        maze[current_point.y][current_point.x - 1] = current_step + 1
        next_points.append(Point(current_point.x - 1, current_point.y))

    # step right
    if can_make_step(
        maze,
        current_point.x + 1,
        current_point.y,
        len(maze[current_point.y]),
        len(maze),
    ):
        maze[current_point.y][current_point.x + 1] = current_step + 1
        next_points.append(Point(current_point.x + 1, current_point.y))

    # step up
    if can_make_step(
        maze,
        current_point.x,
        current_point.y - 1,
        len(maze[current_point.y]),
        len(maze),
    ):
        maze[current_point.y - 1][current_point.x] = current_step + 1
        next_points.append(Point(current_point.x, current_point.y - 1))

    # step down
    if can_make_step(
        maze,
        current_point.x,
        current_point.y + 1,
        len(maze[current_point.y]),
        len(maze),
    ):
        maze[current_point.y + 1][current_point.x] = current_step + 1
        next_points.append(Point(current_point.x, current_point.y + 1))

    return next_points


def find_shortest_path(maze: List[List[str]], end_point: Point) -> int:
    """
    Go back to the start and count the steps
    """
    current_point = end_point
    step_counter = 0
    current_step = int(maze[end_point.y][end_point.x])
    while current_step:
        # step left
        if (
            current_point.x
            and isinstance(maze[current_point.y][current_point.x - 1], int)
            and maze[current_point.y][current_point.x - 1] == current_step - 1
        ):
            maze[current_point.y][current_point.x - 1] = "-"
            current_point = Point(current_point.x - 1, current_point.y)

        # step right
        elif (
            current_point.x < len(maze[current_point.y]) - 1
            and isinstance(maze[current_point.y][current_point.x + 1], int)
            and maze[current_point.y][current_point.x + 1] == current_step - 1
        ):
            maze[current_point.y][current_point.x + 1] = "-"
            current_point = Point(current_point.x + 1, current_point.y)
        # step up
        elif (
            current_point.y
            and isinstance(maze[current_point.y - 1][current_point.x], int)
            and maze[current_point.y - 1][current_point.x] == current_step - 1
        ):
            maze[current_point.y - 1][current_point.x] = "|"
            current_point = Point(current_point.x, current_point.y - 1)
        # step down
        elif (
            current_point.y < len(maze) - 1
            and isinstance(maze[current_point.y + 1][current_point.x], int)
            and maze[current_point.y + 1][current_point.x] == current_step - 1
        ):
            maze[current_point.y + 1][current_point.x] = "|"
            current_point = Point(current_point.x, current_point.y + 1)
        step_counter += 1
        current_step -= 1
    maze[end_point.y][end_point.x] = "F"
    return step_counter


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="MazeSolver", description="Program finds the shortest solution for maze"
    )
    parser.add_argument("maze_file", type=argparse.FileType("r"))
    parser.add_argument("--print-maze", action="store_true", dest="print_maze")
    args = parser.parse_args()
    maze = read_maze(args.maze_file)

    solution = solve_with_bfs(maze)

    if solution:
        print(f"Solution:\nTotal steps: {solution.steps}\nmethod: {solution.method}")
        if args.print_maze:
            print_maze(solution.maze)
