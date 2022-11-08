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
from typing import NamedTuple, List, IO, Tuple


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


class BFSMazeSolver:
    """
    Class represents solver for BFS algorithm
    """

    LEFT: Point = Point(-1, 0)
    RIGHT: Point = Point(1, 0)
    UP: Point = Point(0, -1)
    DOWN: Point = Point(0, 1)
    STEPS: Tuple = (LEFT, RIGHT, UP, DOWN)

    def __init__(
        self, maze: List[List[str]], star_point_char: str, end_point_char: str
    ):
        self.maze: List[List[str]] = maze
        self.start_point: Point = find_point(self.maze, star_point_char)
        self.end_point: Point = find_point(self.maze, end_point_char)
        self.step_count: int = 0

    def solve(self):
        """
        Solve the maze
        """
        points = deque()
        points.append(self.start_point)

        while points:
            current_point = points.popleft()
            if current_point == self.end_point:
                break
            points.extend(self.make_steps(current_point))

        if maze[self.end_point.y][self.end_point.x] == "F":
            raise ValueError("Maze doesn't have solution!")

        self.find_shortest_path()

    def make_steps(self, current_point: Point) -> List[Point]:
        """
        Look arround and make steps in four directions
        """
        current_step = int(maze[current_point.y][current_point.x])
        next_points = []

        for step in self.STEPS:
            if self.can_make_step(
                current_point, current_point.x + step.x, current_point.y + step.y
            ):
                self.maze[current_point.y + step.y][current_point.x + step.x] = (
                    current_step + 1
                )
                next_points.append(
                    Point(current_point.x + step.x, current_point.y + step.y)
                )

        return next_points

    def can_make_step(self, current_point: Point, x: int, y: int) -> bool:
        """
        Check if can make step
        """
        return self.is_safe(current_point, x, y) and (
            self.maze[y][x] == " " or self.maze[y][x] == "F"
        )

    def is_safe(self, current_point: Point, x: int, y: int) -> bool:
        """
        Check if index is not out of the range
        """
        return 0 <= x < len(self.maze[current_point.y]) and 0 <= y < len(self.maze)

    def find_shortest_path(self):
        """
        Go back to the start and count the steps
        """
        current_point = self.end_point
        current_step = int(self.maze[self.end_point.y][self.end_point.x])
        while current_step:
            for step in self.STEPS:
                if (
                    self.is_safe(
                        current_point,
                        current_point.x + step.x,
                        current_point.y + step.y,
                    )
                    and isinstance(
                        self.maze[current_point.y + step.y][current_point.x + step.x],
                        int,
                    )
                    and self.maze[current_point.y + step.y][current_point.x + step.x]
                    == current_step - 1
                ):
                    maze[current_point.y + step.y][current_point.x + step.x] = (
                        "|" if step.y else "-"
                    )
                    current_point = Point(
                        current_point.x + step.x, current_point.y + step.y
                    )
                    break
            self.step_count += 1
            current_step -= 1
        self.maze[self.end_point.y][self.end_point.x] = "F"

    def print_solution(self, _print_maze: bool = False) -> None:
        """
        Print final solution
        """
        print(f"SOLUTION:\nStep count: {self.step_count}\nused method: bfs")
        if _print_maze:
            print_maze(self.maze)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="MazeSolver", description="Program finds the shortest solution for maze"
    )
    parser.add_argument("maze_file", type=argparse.FileType("r"))
    parser.add_argument("-p", "--print-maze", action="store_true", dest="print_maze")
    args = parser.parse_args()
    maze = read_maze(args.maze_file)

    solver = BFSMazeSolver(maze, "0", "F")
    solver.solve()
    solver.print_solution(args.print_maze)
