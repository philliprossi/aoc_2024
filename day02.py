from typing import List, Sequence


def is_safe_report(levels: Sequence[int]) -> bool:
    # Check if there are any duplicates
    if len(set(levels)) != len(levels):
        return False

    # Get differences between adjacent numbers
    diffs = [levels[i + 1] - levels[i] for i in range(len(levels) - 1)]

    # Check if all differences are in the same direction
    if not (all(d > 0 for d in diffs) or all(d < 0 for d in diffs)):
        return False

    # Check if differences are between 1 and 3 inclusive
    return all(1 <= abs(d) <= 3 for d in diffs)


def is_safe_with_dampener(levels: Sequence[int]) -> bool:
    # First check if it's already safe
    if is_safe_report(levels):
        return True

    # Try removing each number one at a time
    for i in range(len(levels)):
        dampened_levels = levels[:i] + levels[i + 1 :]
        if is_safe_report(dampened_levels):
            return True

    return False


def read_input(file_path: str) -> List[List[int]]:
    reports = []
    with open(file_path, "r") as file:
        for line in file:
            levels = list(map(int, line.strip().split()))
            reports.append(levels)
    return reports


def count_safe_reports(reports: List[List[int]], use_dampener: bool = False) -> int:
    check_func = is_safe_with_dampener if use_dampener else is_safe_report
    return sum(1 for report in reports if check_func(report))


if __name__ == "__main__":
    reports = read_input("input/day2.txt")

    # Part 1
    safe_count = count_safe_reports(reports)
    print(f"Part 1 - Number of safe reports: {safe_count}")

    # Part 2
    safe_count_dampened = count_safe_reports(reports, use_dampener=True)
    print(f"Part 2 - Number of safe reports with dampener: {safe_count_dampened}")
