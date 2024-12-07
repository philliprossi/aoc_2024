from collections import defaultdict
from typing import Dict, List, Tuple


def read_input(file_path: str) -> Tuple[List[str], List[List[int]]]:
    with open(file_path, "r") as file:
        sections = file.read().strip().split("\n\n")
        rules = sections[0].strip().splitlines()
        updates = [
            list(map(int, update.split(",")))
            for update in sections[1].strip().splitlines()
        ]
    return rules, updates


def build_rules(rules: List[str]) -> Dict[int, set]:
    # For each page, store what pages must come after it
    must_come_after = defaultdict(set)
    for rule in rules:
        before, after = map(int, rule.split("|"))
        must_come_after[before].add(after)
    return must_come_after


def is_ordered(update: List[int], rules: Dict[int, set]) -> bool:
    positions = {num: i for i, num in enumerate(update)}

    # Check each pair of numbers in the sequence
    for i, num1 in enumerate(update):
        # If this number has rules about what must come after it
        if num1 in rules:
            # Check that all numbers that must come after it are indeed after it
            for must_be_after in rules[num1]:
                if must_be_after in positions and positions[must_be_after] <= i:
                    return False
    return True


def find_middle_page(update: List[int]) -> int:
    # Return the middle number in its original position
    return update[len(update) // 2]


def reorder_update(update: List[int], rules: Dict[int, set]) -> List[int]:
    # Create a graph of dependencies
    graph = {num: set() for num in update}
    for num in update:
        if num in rules:
            for must_come_after in rules[num]:
                if must_come_after in graph:
                    graph[must_come_after].add(num)

    # Topological sort
    result = []
    visited = set()
    temp_visited = set()

    def visit(num):
        if num in temp_visited:
            return  # Handle cycles by skipping
        if num in visited:
            return
        temp_visited.add(num)
        for before in graph[num]:
            visit(before)
        temp_visited.remove(num)
        visited.add(num)
        result.append(num)

    for num in update:
        if num not in visited:
            visit(num)

    return result[::-1]  # Reverse to get correct order


def main(file_path: str) -> Tuple[int, int]:
    rules, updates = read_input(file_path)
    rule_dict = build_rules(rules)

    # Part 1
    total_middle_sum = 0
    invalid_updates = []

    for update in updates:
        if is_ordered(update, rule_dict):
            middle = find_middle_page(update)
            print(f"Part 1 - Valid update: {update}, middle: {middle}")
            total_middle_sum += middle
        else:
            print(f"Part 1 - Invalid update: {update}")
            invalid_updates.append(update)

    # Part 2
    reordered_sum = 0
    for update in invalid_updates:
        reordered = reorder_update(update, rule_dict)
        middle = find_middle_page(reordered)
        print(f"Part 2 - Reordered {update} to {reordered}, middle: {middle}")
        reordered_sum += middle

    return total_middle_sum, reordered_sum


if __name__ == "__main__":
    part1_result, part2_result = main("input/day5.txt")
    print(
        f"\nPart 1 - Sum of middle pages from correctly ordered updates: {part1_result}"
    )
    print(
        f"Part 2 - Sum of middle pages from reordered invalid updates: {part2_result}"
    )
