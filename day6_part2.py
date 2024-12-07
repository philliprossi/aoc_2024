import time
from collections import defaultdict
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


def read_input(file_path: str) -> List[List[str]]:
    with open(file_path, "r") as file:
        return [list(line.strip()) for line in file]


def find_start_position(grid: List[List[str]]) -> Tuple[int, int, Direction]:
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


def find_empty_positions(
    grid: List[List[str]], start_x: int, start_y: int
) -> Set[Tuple[int, int]]:
    empty = set()
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell == "." and (x, y) != (start_x, start_y):
                empty.add((x, y))
    return empty


def simulate_guard_path_with_loop_detection(
    grid: List[List[str]],
    start_x: int,
    start_y: int,
    start_direction: Direction,
    obstruction_pos: Tuple[int, int],
    max_steps: int,
) -> bool:
    x, y = start_x, start_y
    direction = start_direction

    # Use a dictionary to store visit counts for each state
    # A state is (position, direction)
    visits = defaultdict(int)
    state = (x, y, direction)
    visits[state] = 1

    steps = 0
    rows, cols = len(grid), len(grid[0])

    while steps < max_steps:
        # Calculate next position
        dx, dy = direction.value
        next_x, next_y = x + dx, y + dy

        # Check if we're about to leave the grid
        if not (0 <= next_y < rows and 0 <= next_x < cols):
            return False

        # Check if there's an obstacle ahead
        is_obstacle = grid[next_y][next_x] == "#" or (next_x, next_y) == obstruction_pos

        if is_obstacle:
            # Turn right
            direction = direction.turn_right()
        else:
            # Move forward
            x, y = next_x, next_y

        # Update state and check for loop
        state = (x, y, direction)
        visits[state] += 1

        # If we've seen this state twice, we've found a loop
        if visits[state] > 1:
            return True

        steps += 1

    return False


def find_loop_positions(grid: List[List[str]], debug: bool = False) -> int:
    start_x, start_y, start_direction = find_start_position(grid)
    empty_positions = find_empty_positions(grid, start_x, start_y)
    valid_count = 0

    # Calculate maximum possible steps based on grid size
    max_steps = len(grid) * len(grid[0]) * 4
    total_positions = len(empty_positions)

    if debug:
        print(f"Grid size: {len(grid)}x{len(grid[0])}")
        print(f"Testing {total_positions} possible positions...")
        start_time = time.time()
        last_update = start_time

    # Try placing an obstruction at each empty position
    for i, pos in enumerate(empty_positions, 1):
        if simulate_guard_path_with_loop_detection(
            grid, start_x, start_y, start_direction, pos, max_steps
        ):
            valid_count += 1

        # Print progress every second in debug mode
        if debug and time.time() - last_update >= 1.0:
            elapsed = time.time() - start_time
            progress = i / total_positions
            eta = (elapsed / progress) * (1 - progress) if progress > 0 else 0
            print(
                f"Progress: {i}/{total_positions} ({progress:.1%}), Valid found: {valid_count}, ETA: {eta:.1f}s"
            )
            last_update = time.time()

    if debug:
        print(
            f"\nFound {valid_count} valid positions in {time.time() - start_time:.1f} seconds"
        )

    return valid_count


def main(file_path: str, debug: bool = False) -> int:
    grid = read_input(file_path)
    return find_loop_positions(grid, debug)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Day 6: Guard Gallivant - Part 2")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    start_time = time.time()
    result = main("input/day06.txt", args.debug)
    elapsed = time.time() - start_time

    print(f"Final answer: {result}")
    print(f"Total time: {elapsed:.2f} seconds")
