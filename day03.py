import re
from typing import List


def extract_mul_instructions(corrupted_memory: str) -> List[int]:
    # Use regex to find all valid mul instructions
    pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)"
    matches = re.findall(pattern, corrupted_memory)

    # Calculate the results of the valid instructions
    results = [int(x) * int(y) for x, y in matches]
    return results


def extract_enabled_mul_instructions(corrupted_memory: str) -> List[int]:
    # Find all mul instructions and control statements in order
    pattern = r"mul\(\s*(\d+)\s*,\s*(\d+)\s*\)|do\(\)|don\'t\(\)"
    matches = list(re.finditer(pattern, corrupted_memory))

    enabled = True  # Start with mul instructions enabled
    results = []

    for match in matches:
        instruction = match.group(0)
        if instruction == "do()":
            enabled = True
        elif instruction == "don't()":
            enabled = False
        else:
            # Extract numbers from mul instruction if enabled
            if enabled:
                nums = re.findall(r"\d+", instruction)
                if len(nums) == 2:
                    results.append(int(nums[0]) * int(nums[1]))

    return results


def read_input(file_path: str) -> str:
    with open(file_path, "r") as file:
        return file.read().strip()


if __name__ == "__main__":
    corrupted_memory = read_input("input/day3.txt")

    # Part 1
    results = extract_mul_instructions(corrupted_memory)
    total_sum = sum(results)
    print(f"Part 1 - Total sum of multiplications: {total_sum}")

    # Part 2
    enabled_results = extract_enabled_mul_instructions(corrupted_memory)
    enabled_sum = sum(enabled_results)
    print(f"Part 2 - Total sum of enabled multiplications: {enabled_sum}")
