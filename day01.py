def calculate_total_distance(left_list, right_list):
    # Sort both lists
    left_list.sort()
    right_list.sort()
    total_distance = 0
    # Calculate the total distance
    for left, right in zip(left_list, right_list):
        total_distance += abs(left - right)

    return total_distance


def calculate_similarity_score(left_list, right_list):
    # Count occurrences in right list
    right_counts = {}
    for num in right_list:
        right_counts[num] = right_counts.get(num, 0) + 1

    # Calculate similarity score
    total_score = 0
    for num in left_list:
        total_score += num * right_counts.get(num, 0)

    return total_score


def read_input(file_path):
    left_list = []
    right_list = []

    with open(file_path, "r") as file:
        for line in file:
            left, right = map(int, line.split())
            left_list.append(left)
            right_list.append(right)

    return left_list, right_list


# Example usage
if __name__ == "__main__":
    left_list, right_list = read_input("input/day1.txt")

    # Part 1
    total_distance = calculate_total_distance(left_list, right_list)
    print(f"Part 1 - Total distance: {total_distance}")

    # Part 2
    similarity_score = calculate_similarity_score(left_list, right_list)
    print(f"Part 2 - Similarity score: {similarity_score}")
