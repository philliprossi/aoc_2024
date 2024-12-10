from typing import List, Set, Tuple, Dict
from collections import deque, defaultdict


def read_input(file_path: str) -> List[List[int]]:
    """Read and parse the input file into a 2D grid of heights."""
    with open(file_path, 'r') as f:
        return [[int(c) if c != '.' else -1 for c in line.strip()] for line in f]


def find_trailheads(grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Find all positions with height 0 (trailheads)."""
    trailheads = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 0:
                trailheads.append((i, j))
    return trailheads


def get_neighbors(pos: Tuple[int, int], grid: List[List[int]]) -> List[Tuple[int, int]]:
    """Get valid neighboring positions (up, down, left, right)."""
    i, j = pos
    rows, cols = len(grid), len(grid[0])
    neighbors = []

    # Check all four directions: up, down, left, right
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < rows and 0 <= nj < cols and grid[ni][nj] != -1:  # Skip impassable tiles
            neighbors.append((ni, nj))

    return neighbors


def count_distinct_paths(start: Tuple[int, int], grid: List[List[int]], debug: bool = False) -> Dict[Tuple[int, int], int]:
    """Count distinct paths from start to each height-9 position."""
    rows, cols = len(grid), len(grid[0])
    paths_to_nine = defaultdict(int)  # {nine_pos: count}
    visited = set()
    queue = deque([(start, {start})])  # (position, path)

    while queue:
        pos, path = queue.popleft()
        i, j = pos
        current_height = grid[i][j]

        if current_height == 9:
            paths_to_nine[pos] += 1
            if debug:
                print(f"Found path to 9 at {pos}:")
                print_path(grid, path)
            continue

        # Try all neighbors
        for next_pos in get_neighbors(pos, grid):
            ni, nj = next_pos
            next_height = grid[ni][nj]

            # Check if this is a valid step (height increases by exactly 1)
            if next_height == current_height + 1 and next_pos not in path:
                new_path = path | {next_pos}
                queue.append((next_pos, new_path))

    return paths_to_nine


def print_path(grid: List[List[int]], path: Set[Tuple[int, int]]) -> None:
    """Print the grid with the path marked."""
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if (i, j) in path:
                val = grid[i][j]
                if val == -1:
                    print(f"\033[92m.\033[0m", end='')  # Green for path
                else:
                    print(f"\033[92m{val}\033[0m", end='')  # Green for path
            else:
                if grid[i][j] == -1:
                    print('.', end='')
                else:
                    print(grid[i][j], end='')
        print()
    print()


def print_grid(grid: List[List[int]]) -> None:
    """Print the grid."""
    for row in grid:
        for val in row:
            if val == -1:
                print('.', end='')
            else:
                print(val, end='')
        print()
    print()


def solve_part2(grid: List[List[int]], debug: bool = False) -> int:
    """Find the sum of ratings for all trailheads."""
    if debug:
        print("Input grid:")
        print_grid(grid)

    trailheads = find_trailheads(grid)
    if debug:
        print(f"Found {len(trailheads)} trailheads: {trailheads}\n")

    total_rating = 0
    for i, trailhead in enumerate(trailheads):
        paths = count_distinct_paths(trailhead, grid, debug)
        rating = sum(paths.values())  # Total number of distinct paths to all 9s
        if debug:
            print(f"Trailhead {i+1} at {trailhead} has rating {rating}")
            print(f"Paths to each 9: {dict(paths)}\n")
        total_rating += rating

    return total_rating


def main(file_path: str, debug: bool = False) -> int:
    """Main function to solve the puzzle."""
    import time
    start_time = time.time()

    # Parse input
    grid = read_input(file_path)

    # Solve part 2
    result = solve_part2(grid, debug)

    end_time = time.time()
    print(f"\nSum of trailhead ratings: {result}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 10: Hoof It - Part 2')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day10.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should match example outputs
