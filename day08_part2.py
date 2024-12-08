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

def is_collinear(p1, p2, p3):
    """Check if three points are collinear."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3

    # Calculate slopes
    if x2 - x1 == 0:  # Vertical line
        return x3 == x1
    if y2 - y1 == 0:  # Horizontal line
        return y3 == y1

    # Check if slopes are equal
    slope1 = (y2 - y1) / (x2 - x1)
    if x3 - x1 == 0:
        return False
    slope2 = (y3 - y1) / (x3 - x1)
    return abs(slope1 - slope2) < 1e-10

def find_antinodes(antennas, map_width, map_height, debug=False):
    """Find all antinode positions based on antenna pairs."""
    antinodes = set()

    # For each frequency
    for freq, positions in antennas.items():
        if debug:
            print(f"\nProcessing frequency {freq} with positions {positions}")

        # Skip frequencies with only one antenna
        if len(positions) < 2:
            continue

        # Add all antenna positions as antinodes (except single antennas)
        antinodes.update(positions)

        # For each pair of antennas with the same frequency
        for i, pos1 in enumerate(positions):
            for j, pos2 in enumerate(positions[i + 1:], i + 1):
                if debug:
                    print(f"  Checking pair at {pos1} and {pos2}")

                # For each point in the grid
                for x in range(map_width):
                    for y in range(map_height):
                        point = (x, y)
                        # Check if point is collinear with the antenna pair
                        if is_collinear(pos1, pos2, point):
                            if debug:
                                print(f"    Found antinode at {point} (collinear)")
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
    parser = argparse.ArgumentParser(description='Day 8: Resonant Collinearity - Part 2')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day08.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should be 9 for the T example, 34 for the full example
