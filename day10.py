from typing import List, Set, Tuple
from collections import deque


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


def find_reachable_nines(start: Tuple[int, int], grid: List[List[int]], debug: bool = False) -> Set[Tuple[int, int]]:
    """Find all height-9 positions reachable from the start position via valid hiking trails."""
    rows, cols = len(grid), len(grid[0])
    visited = set()
    reachable_nines = set()
    queue = deque([(start, {start})])  # (position, path)

    while queue:
        pos, path = queue.popleft()
        i, j = pos
        current_height = grid[i][j]

        if current_height == 9:
            reachable_nines.add(pos)
            if debug:
                print(f"Found path to 9 at {pos}:")
                print_path(grid, path)
            continue

        if pos in visited:
            continue

        visited.add(pos)

        # Try all neighbors
        for next_pos in get_neighbors(pos, grid):
            ni, nj = next_pos
            next_height = grid[ni][nj]

            # Check if this is a valid step (height increases by exactly 1)
            if next_height == current_height + 1 and next_pos not in path:
                new_path = path | {next_pos}
                queue.append((next_pos, new_path))

    return reachable_nines


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


def solve_part1(grid: List[List[int]], debug: bool = False) -> int:
    """Find the sum of scores for all trailheads."""
    if debug:
        print("Input grid:")
        print_grid(grid)

    trailheads = find_trailheads(grid)
    if debug:
        print(f"Found {len(trailheads)} trailheads: {trailheads}\n")

    total_score = 0
    for i, trailhead in enumerate(trailheads):
        reachable = find_reachable_nines(trailhead, grid, debug)
        score = len(reachable)
        if debug:
            print(f"Trailhead {i+1} at {trailhead} has score {score}")
            print(f"Can reach {len(reachable)} nines: {reachable}\n")
        total_score += score

    return total_score


def main(file_path: str, debug: bool = False) -> int:
    """Main function to solve the puzzle."""
    grid = read_input(file_path)
    result = solve_part1(grid, debug)
    print(f"\nSum of trailhead scores: {result}")
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 10: Hoof It')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day10.txt", args.debug)
    print(f"\nFinal answer: {result}")
