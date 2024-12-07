from typing import List


def read_input(file_path: str) -> List[str]:
    with open(file_path, "r") as file:
        return [line.strip() for line in file]


def find_xmas(grid: List[str]) -> int:
    rows = len(grid)
    cols = len(grid[0])
    count = 0

    # All possible directions: right, down-right, down, down-left, left, up-left, up, up-right
    directions = [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)]

    def check_direction(row: int, col: int, dx: int, dy: int) -> bool:
        """Check if 'XMAS' exists starting from (row, col) in direction (dx, dy)"""
        if not (0 <= row + 3 * dx < rows and 0 <= col + 3 * dy < cols):
            return False

        return (
            grid[row][col] == "X"
            and grid[row + dx][col + dy] == "M"
            and grid[row + 2 * dx][col + 2 * dy] == "A"
            and grid[row + 3 * dx][col + 3 * dy] == "S"
        )

    # Check each starting position
    for i in range(rows):
        for j in range(cols):
            # Try all directions from this position
            for dx, dy in directions:
                if check_direction(i, j, dx, dy):
                    count += 1

    return count


if __name__ == "__main__":
    grid = read_input("input/day4.txt")
    xmas_count = find_xmas(grid)
    print(f"Number of XMAS occurrences: {xmas_count}")
