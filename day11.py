from typing import List, Tuple
from functools import lru_cache


def read_input(file_path: str) -> List[int]:
    """Read and parse the input file into a list of numbers."""
    with open(file_path, 'r') as f:
        return [int(x) for x in f.readline().strip().split()]


@lru_cache(maxsize=None)
def transform_stone(n: int) -> Tuple[int, ...]:
    """Transform a single stone according to the rules. Returns tuple for hashability."""
    # Rule 1: If the stone is 0, replace with 1
    if n == 0:
        return (1,)

    # Rule 2: If the stone has even digits, split it
    if len(str(n)) % 2 == 0:
        s = str(n)
        mid = len(s) // 2
        return (int(s[:mid]), int(s[mid:]))

    # Rule 3: Otherwise, multiply by 2024
    return (n * 2024,)


@lru_cache(maxsize=None)
def process_stone(stone: int, steps: int) -> int:
    """Process a single stone for a given number of steps."""
    if steps == 0:
        return 1

    # Transform the stone
    new_stones = transform_stone(stone)

    # Process each resulting stone recursively
    total = 0
    for new_stone in new_stones:
        total += process_stone(new_stone, steps - 1)

    return total


def solve_part(initial_stones: List[int], steps: int) -> int:
    """Solve for a given number of steps."""
    total_stones = 0
    for i, stone in enumerate(initial_stones, 1):
        print(f"\nProcessing stone {i} of {len(initial_stones)}: {stone}")
        stone_count = process_stone(stone, steps)
        print(f"Final count for stone {stone}: {stone_count}")
        total_stones += stone_count
    return total_stones


def main(debug: bool = False) -> None:
    """Main function to process stones with memoization."""
    # Read stones from input file
    input_file = "input/day11.txt"
    initial_stones = read_input(input_file)

    # Part 1 (25 steps)
    print(f"\nPart 1 - Processing {len(initial_stones)} stones for 25 steps...")
    part1_result = solve_part(initial_stones, 25)
    print(f"\nPart 1 - Total stones after 25 steps: {part1_result}")

    # Part 2 (75 steps)
    print(f"\nPart 2 - Processing {len(initial_stones)} stones for 75 steps...")
    part2_result = solve_part(initial_stones, 75)
    print(f"\nPart 2 - Total stones after 75 steps: {part2_result}")

    # Print cache info
    print("\nCache statistics:")
    print(f"transform_stone cache info: {transform_stone.cache_info()}")
    print(f"process_stone cache info: {process_stone.cache_info()}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 11: Plutonian Pebbles')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    main(args.debug)
