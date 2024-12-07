def read_grid(filename):
    with open(filename) as f:
        return [list(line.strip()) for line in f]


def check_diagonal(grid, r, c, dr, dc):
    rows, cols = len(grid), len(grid[0])
    # Check if all three positions are within bounds
    for i in range(3):
        new_r = r + i * dr
        new_c = c + i * dc
        if not (0 <= new_r < rows and 0 <= new_c < cols):
            return False

    # Get the three characters in the diagonal
    chars = [grid[r][c], grid[r + dr][c + dc], grid[r + 2 * dr][c + 2 * dc]]
    return "".join(chars) in ["MAS", "SAM"]


def count_xmas_patterns(grid):
    count = 0
    rows, cols = len(grid), len(grid[0])

    for r in range(1, rows - 1):
        for c in range(1, cols - 1):
            # Check center A
            if grid[r][c] != "A":
                continue

            # Check both diagonals (forward and backward for each)
            # For each diagonal, we need to check both MAS and SAM
            diagonals = [
                # top-left to bottom-right
                (r - 1, c - 1, 1, 1),
                # top-right to bottom-left
                (r - 1, c + 1, 1, -1),
            ]

            if check_diagonal(
                grid, diagonals[0][0], diagonals[0][1], diagonals[0][2], diagonals[0][3]
            ) and check_diagonal(
                grid, diagonals[1][0], diagonals[1][1], diagonals[1][2], diagonals[1][3]
            ):
                count += 1

    return count


def main():
    grid = read_grid("input/day4.txt")
    result = count_xmas_patterns(grid)
    print(f"Number of X-MAS patterns: {result}")


if __name__ == "__main__":
    main()
