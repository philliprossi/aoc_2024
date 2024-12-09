def parse_input(file_path):
    """Parse input file into a disk map."""
    with open(file_path, 'r') as f:
        return f.readline().strip()

def parse_disk_map(disk_map):
    """Parse disk map into alternating file and free space lengths."""
    return [int(x) for x in disk_map]

def create_block_map(lengths):
    """Create a block map showing file IDs and free space."""
    blocks = []
    file_id = 0
    for i, length in enumerate(lengths):
        if i % 2 == 0:  # File block
            blocks.extend([file_id] * length)
            file_id += 1
        else:  # Free space block
            blocks.extend(['.'] * length)
    return blocks

def print_block_map(blocks):
    """Print the block map in a readable format."""
    print(''.join(str(x) for x in blocks))

def find_rightmost_block(blocks):
    """Find the rightmost single block that can be moved."""
    for i in range(len(blocks) - 1, -1, -1):
        if blocks[i] != '.':
            return i
    return None

def find_leftmost_space(blocks, end_pos):
    """Find the leftmost free space before end_pos."""
    for i in range(end_pos):
        if blocks[i] == '.':
            return i
    return None

def compact_disk(blocks, debug=False):
    """Compact the disk by moving one block at a time from right to left."""
    if debug:
        print("\nInitial state:")
        print_block_map(blocks)

    while True:
        # Find rightmost block
        rightmost = find_rightmost_block(blocks)
        if rightmost is None:
            break

        # Find leftmost space
        leftmost = find_leftmost_space(blocks, rightmost)
        if leftmost is None:
            break

        # Move the block
        blocks[leftmost] = blocks[rightmost]
        blocks[rightmost] = '.'

        if debug:
            print_block_map(blocks)

    return blocks

def calculate_checksum(blocks):
    """Calculate the filesystem checksum."""
    checksum = 0
    for pos, block in enumerate(blocks):
        if block != '.':
            checksum += pos * block
    return checksum

def solve_part1(disk_map, debug=False):
    """Solve part 1 of the puzzle."""
    # Parse the disk map into lengths
    lengths = parse_disk_map(disk_map)
    if debug:
        print(f"Lengths: {lengths}")

    # Create block map
    blocks = create_block_map(lengths)
    if debug:
        print("\nInitial block map:")
        print_block_map(blocks)

    # Compact the disk
    compacted_blocks = compact_disk(blocks, debug)

    # Calculate checksum
    checksum = calculate_checksum(compacted_blocks)
    if debug:
        print(f"\nFinal checksum: {checksum}")

    return checksum

def main(file_path: str, debug: bool = False):
    """Main function to solve the puzzle."""
    import time
    start_time = time.time()

    # Parse input
    disk_map = parse_input(file_path)

    # Solve part 1
    result = solve_part1(disk_map, debug)

    end_time = time.time()
    print(f"\nFilesystem checksum: {result}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 9: Disk Fragmenter')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day09.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should be 1928 for the example
