def parse_input(map_lines):
    """Parse the input map into a dictionary of frequencies and their antenna positions."""
    antennas = {}
    for y, line in enumerate(map_lines):
        for x, char in enumerate(line):
            if char.isalnum():  # Only consider letters and numbers as antennas
                if char not in antennas:
                    antennas[char] = []
                antennas[char].append((x, y))
    return antennas

def manhattan_distance(p1, p2):
    """Calculate Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_antinodes(antennas, map_width, map_height, debug=False):
    """Find all antinode positions based on antenna pairs."""
    antinodes = set()

    # For each frequency
    for freq, positions in antennas.items():
        if debug:
            print(f"\nProcessing frequency {freq} with positions {positions}")

        # For each pair of antennas with the same frequency
        for i, pos1 in enumerate(positions):
            for j, pos2 in enumerate(positions[i + 1:], i + 1):
                x1, y1 = pos1
                x2, y2 = pos2

                if debug:
                    print(f"  Checking pair at {pos1} and {pos2}")

                # Calculate the vector from antenna 1 to antenna 2
                dx = x2 - x1
                dy = y2 - y1

                # Calculate the distance between antennas
                dist = manhattan_distance(pos1, pos2)

                # Try extending the line in both directions
                for direction in [-1, 1]:
                    # Calculate potential antinode position at twice the distance
                    antinode_x = x2 + direction * dx
                    antinode_y = y2 + direction * dy

                    # Check if antinode is within map bounds
                    if 0 <= antinode_x < map_width and 0 <= antinode_y < map_height:
                        point = (antinode_x, antinode_y)

                        # Calculate distances to both antennas
                        d1 = manhattan_distance(point, pos1)
                        d2 = manhattan_distance(point, pos2)

                        # Check if one distance is twice the other
                        if d1 == 2 * d2 or d2 == 2 * d1:
                            if debug:
                                print(f"    Found antinode at {point} (distances: {d1}, {d2})")
                            antinodes.add(point)

                    # Also try from the first antenna
                    antinode_x = x1 - direction * dx
                    antinode_y = y1 - direction * dy

                    # Check if antinode is within map bounds
                    if 0 <= antinode_x < map_width and 0 <= antinode_y < map_height:
                        point = (antinode_x, antinode_y)

                        # Calculate distances to both antennas
                        d1 = manhattan_distance(point, pos1)
                        d2 = manhattan_distance(point, pos2)

                        # Check if one distance is twice the other
                        if d1 == 2 * d2 or d2 == 2 * d1:
                            if debug:
                                print(f"    Found antinode at {point} (distances: {d1}, {d2})")
                            antinodes.add(point)

    return antinodes

def print_map_with_antinodes(map_lines, antinodes):
    """Print the map showing original antennas and antinodes."""
    print("\nMap with antinodes (#):")
    for y, line in enumerate(map_lines):
        row = ""
        for x, char in enumerate(line):
            if (x, y) in antinodes:
                if char == '.':
                    row += '#'
                else:
                    row += char  # Keep original antenna if it's at an antinode position
            else:
                row += char
        print(row)

def count_unique_antinodes(map_lines, debug=False):
    """Count unique antinode positions within the map bounds."""
    # Get map dimensions
    height = len(map_lines)
    width = len(map_lines[0])

    # Parse input
    antennas = parse_input(map_lines)
    if debug:
        print(f"Found antennas: {antennas}")

    # Find antinodes
    antinodes = find_antinodes(antennas, width, height, debug)
    if debug:
        print(f"\nFound {len(antinodes)} unique antinode positions:")
        print_map_with_antinodes(map_lines, antinodes)

    return len(antinodes)

def main(file_path: str, debug: bool = False):
    """Main function to process input and return result."""
    with open(file_path, "r") as file:
        map_lines = [line.strip() for line in file]

    distinct_positions = count_unique_antinodes(map_lines, debug)
    print(f"\nTotal unique locations with antinodes: {distinct_positions}")
    return distinct_positions

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 8: Resonant Collinearity')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day08.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should be 14 for the example
