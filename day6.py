from enum import Enum
from typing import List, Set, Tuple


class Direction(Enum):
    UP = (0, -1)
    RIGHT = (1, 0)
    DOWN = (0, 1)
    LEFT = (-1, 0)

    def turn_right(self) -> "Direction":
        return {
            Direction.UP: Direction.RIGHT,
            Direction.RIGHT: Direction.DOWN,
            Direction.DOWN: Direction.LEFT,
            Direction.LEFT: Direction.UP,
        }[self]


def read_input(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def find_start_position(grid: List[str]) -> Tuple[int, int, Direction]:
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "^":
                return x, y, Direction.UP
            elif cell == ">":
                return x, y, Direction.RIGHT
            elif cell == "v":
                return x, y, Direction.DOWN
            elif cell == "<":
                return x, y, Direction.LEFT
    raise ValueError("No starting position found")


def is_within_grid(x: int, y: int, grid: List[str]) -> bool:
    return 0 <= y < len(grid) and 0 <= x < len(grid[0])


def simulate_guard_path(grid: List[str], debug: bool = False) -> int:
    # Find starting position and direction
    x, y, direction = find_start_position(grid)
    visited = {(x, y)}  # Set of visited positions

    if debug:
        print("\nInitial state:")
        print_grid(grid)

    step = 0
    while True:
        # Calculate next position
        dx, dy = direction.value
        next_x = x + dx
        next_y = y + dy

        # Check if we're about to leave the grid
        if not is_within_grid(next_x, next_y, grid):
            if debug:
                print(f"\nGuard left the grid at position ({x}, {y})")
            break

        # Check if there's an obstacle ahead
        if grid[next_y][next_x] == "#":
            # Turn right
            direction = direction.turn_right()
            if debug:
                print(
                    f"\nStep {step + 1}: Turned right at ({x}, {y}), now facing {direction.name}"
                )
        else:
            # Move forward
            x, y = next_x, next_y
            visited.add((x, y))
            if debug:
                print(f"\nStep {step + 1}: Moved to ({x}, {y})")

        if debug:
            print_current_state(grid, visited, x, y, direction)
        step += 1

    if debug:
        print("\nFinal visited positions:")
        print_visited_positions(grid, visited)

    return len(visited)


def print_grid(grid: List[str]):
    for row in grid:
        print(row)


def print_current_state(
    grid: List[str],
    visited: Set[Tuple[int, int]],
    guard_x: int,
    guard_y: int,
    direction: Direction,
):
    direction_chars = {
        Direction.UP: "^",
        Direction.RIGHT: ">",
        Direction.DOWN: "v",
        Direction.LEFT: "<",
    }

    for y, row in enumerate(grid):
        line = ""
        for x, cell in enumerate(row):
            if (x, y) == (guard_x, guard_y):
                line += direction_chars[direction]
            elif (x, y) in visited:
                line += "X"
            else:
                line += cell
        print(line)


def print_visited_positions(grid: List[str], visited: Set[Tuple[int, int]]):
    for y, row in enumerate(grid):
        line = ""
        for x, cell in enumerate(row):
            if (x, y) in visited:
                line += "X"
            elif cell == "#":
                line += "#"
            else:
                line += "."
        print(line)


def main(file_path: str, debug: bool = False) -> int:
    grid = read_input(file_path)
    distinct_positions = simulate_guard_path(grid, debug)
    if debug:
        print(f"\nTotal distinct positions visited: {distinct_positions}")
    return distinct_positions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Day 6: Guard Gallivant")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    result = main("input/day06.txt", args.debug)
    print(f"Final answer: {result}")  # Should be 41 for the example
