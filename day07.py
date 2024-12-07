import time
from itertools import product
from typing import List, Set, Tuple


def read_input(file_path: str) -> List[Tuple[int, List[int]]]:
    equations = []
    with open(file_path, "r") as file:
        for line in file:
            test_value, numbers = line.strip().split(": ")
            numbers = [int(n) for n in numbers.split()]
            equations.append((int(test_value), numbers))
    return equations


def evaluate_expression(numbers: List[int], operators: List[str]) -> int:
    """Evaluate expression left-to-right."""
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == "+":
            result += numbers[i + 1]
        else:  # op == '*'
            result *= numbers[i + 1]
    return result


def find_valid_equations(
    equations: List[Tuple[int, List[int]]], debug: bool = False
) -> Set[int]:
    """Find equations that can be satisfied with some combination of operators."""
    valid_test_values = set()
    operators = ["+", "*"]

    for test_value, numbers in equations:
        # Number of operators needed is one less than number of operands
        num_operators = len(numbers) - 1

        # Try all possible combinations of operators
        found_valid = False
        for ops in product(operators, repeat=num_operators):
            result = evaluate_expression(numbers, ops)
            if result == test_value:
                if debug:
                    op_str = (
                        " ".join(f"{n}{op}" for n, op in zip(numbers[:-1], ops))
                        + f" {numbers[-1]}"
                    )
                    print(f"Found valid equation: {test_value} = {op_str} = {result}")
                valid_test_values.add(test_value)
                found_valid = True

        if debug and not found_valid:
            print(f"No valid operators found for test value: {test_value}")

    return valid_test_values


def main(file_path: str, debug: bool = False) -> int:
    # Read input
    start_time = time.time()
    equations = read_input(file_path)
    read_time = time.time() - start_time

    if debug:
        print(f"\nRead {len(equations)} equations in {read_time:.4f} seconds")
        print("\nProcessing equations...")

    # Find valid equations
    process_start = time.time()
    valid_values = find_valid_equations(equations, debug)
    process_time = time.time() - process_start

    # Calculate result
    result = sum(valid_values)

    if debug:
        print(
            f"\nFound {len(valid_values)} valid equations in {process_time:.4f} seconds"
        )
        print(f"Valid test values: {sorted(valid_values)}")
        print(f"Total time: {time.time() - start_time:.4f} seconds")

    return result


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Day 7: Bridge Repair")
    parser.add_argument("--debug", action="store_true", help="Enable debug output")
    args = parser.parse_args()

    result = main("input/day07.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should be 3749 for the example
