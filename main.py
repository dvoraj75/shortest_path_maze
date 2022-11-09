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


def read_maze(maze_file: IO[str]) -> List[List[str]]:
    """
    Read file with the maze and covert it to 2d array
    """
    return [[c for c in line if c != "\n"] for line in maze_file]


class Point(NamedTuple):
    """
    Simple class representing point in maze
    """

    x: int
    y: int


class Maze:
    """
    Class representing 2d maze
    """

    def __init__(
        self,
        maze: List[List[str]],
        start_point_char: str = "0",
        end_point_char: str = "F",
        wall: str = "#",
        free_space: str = " ",
    ):
        self.maze: List[List[str]] = maze
        self.start_point_char: str = start_point_char
        self.end_point_char: str = end_point_char
        self.wall: str = wall
        self.free_space: str = free_space
        self.start_point: Point = self.find_point(self.start_point_char)
        self.end_point: Point = self.find_point(self.end_point_char)
        self.x_size = len(self.maze[0])
        self.y_size = len(self.maze)

        self.check_maze()

    def check_maze(self):
        """
        Check if maze is rectangular
        """
        first_line = len(self.maze[0])
        for line in self.maze:
            if len(line) != first_line:
                raise ValueError("Maze is not rectangle!")

    def print_maze(self):
        """
        Print maze 2d array
        """
        for line in self.maze:
            for char in line:
                print(
                    char
                    if char
                    in ("-", "|", self.start_point_char, self.end_point_char, self.wall)
                    else " ",
                    end="",
                )
            print()

    def find_point(self, char: str) -> Point:
        """
        Find character 'char' in the maze. Using for finding start and end point
        """
        for y_coord, line in enumerate(self.maze):
            try:
                return Point(line.index(char), y_coord)
            except ValueError:
                pass
        raise ValueError(f"Maze doesn't have point with '{char}' character")

    def get_value(self, x: int, y: int) -> str:
        """
        Get value from x, y coords
        """
        return self.maze[y][x]

    def set_value(self, x: int, y: int, value: str):
        """
        Set value to x, y coords
        """
        self.maze[y][x] = value


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
        self,
        maze: Maze,
    ):
        self.maze: Maze = maze
        self.step_count: int = 0

    def solve(self):
        """
        Solve the maze
        """
        points = deque()
        points.append(self.maze.start_point)

        while points:
            current_point = points.popleft()
            if current_point == self.maze.end_point:
                break
            points.extend(self.make_steps(current_point))

        if (
            self.maze.get_value(self.maze.end_point.x, self.maze.end_point.y)
            == self.maze.end_point_char
        ):
            raise ValueError("Maze doesn't have solution!")

        self.find_shortest_path()

    def make_steps(self, current_point: Point) -> List[Point]:
        """
        Look arround and make steps in four directions
        """
        current_step = int(self.maze.get_value(current_point.x, current_point.y))
        next_points = []

        for step in self.STEPS:
            if self.can_make_step(current_point.x + step.x, current_point.y + step.y):
                self.maze.set_value(
                    current_point.x + step.x,
                    current_point.y + step.y,
                    str(current_step + 1),
                )
                next_points.append(
                    Point(current_point.x + step.x, current_point.y + step.y)
                )
        return next_points

    def can_make_step(self, x: int, y: int) -> bool:
        """
        Check if can make step
        """
        return self.is_safe(x, y) and (
            self.maze.get_value(x, y) == self.maze.free_space
            or self.maze.get_value(x, y) == self.maze.end_point_char
        )

    def is_safe(self, x: int, y: int) -> bool:
        """
        Check if index is not out of the range
        """
        return 0 <= x < self.maze.x_size and 0 <= y < self.maze.y_size

    def find_shortest_path(self):
        """
        Go back to the start and count the steps
        """
        current_point = self.maze.end_point
        current_step = int(
            self.maze.get_value(self.maze.end_point.x, self.maze.end_point.y)
        )
        while current_step:
            for step in self.STEPS:
                if (
                    self.is_safe(
                        current_point.x + step.x,
                        current_point.y + step.y,
                    )
                    and self.maze.get_value(
                        current_point.x + step.x, current_point.y + step.y
                    ).isdigit()
                    and int(
                        self.maze.get_value(
                            current_point.x + step.x, current_point.y + step.y
                        )
                    )
                    == current_step - 1
                ):
                    self.maze.set_value(
                        current_point.x + step.x,
                        current_point.y + step.y,
                        "|" if step.y else "-",
                    )
                    current_point = Point(
                        current_point.x + step.x, current_point.y + step.y
                    )
                    break
            self.step_count += 1
            current_step -= 1
        # reset start/end point
        self.maze.set_value(
            self.maze.start_point.x, self.maze.start_point.y, self.maze.start_point_char
        )
        self.maze.set_value(
            self.maze.end_point.x, self.maze.end_point.y, self.maze.end_point_char
        )

    def print_solution(self, _print_maze: bool = False):
        """
        Print final solution
        """
        print(f"SOLUTION:\nStep count: {self.step_count}\nused method: bfs")
        if _print_maze:
            self.maze.print_maze()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="MazeSolver", description="Program finds the shortest solution for maze"
    )
    parser.add_argument("maze_file", type=argparse.FileType("r"))
    parser.add_argument("-p", "--print-maze", action="store_true", dest="print_maze")
    args = parser.parse_args()

    solver = BFSMazeSolver(Maze(read_maze(args.maze_file)))
    solver.solve()
    solver.print_solution(args.print_maze)
