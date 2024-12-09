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

def find_file_boundaries(blocks):
    """Find the boundaries of each file in the blocks."""
    file_boundaries = {}  # {file_id: (start, length)}
    current_file = None
    start = None
    length = 0

    for i, block in enumerate(blocks):
        if block != '.':  # File block
            if current_file != block:  # Start of new file
                if current_file is not None:
                    file_boundaries[current_file] = (start, length)
                current_file = block
                start = i
                length = 1
            else:  # Continue current file
                length += 1
        elif current_file is not None:  # End of file
            file_boundaries[current_file] = (start, length)
            current_file = None
            length = 0

    # Handle last file if it extends to the end
    if current_file is not None:
        file_boundaries[current_file] = (start, length)

    return file_boundaries

def find_leftmost_space(blocks, start_pos, needed_length):
    """Find the leftmost contiguous space that can fit a file of given length."""
    i = 0
    while i < start_pos:
        if blocks[i] == '.':
            # Check if there's enough contiguous space
            space_length = 0
            for j in range(i, start_pos):
                if blocks[j] == '.':
                    space_length += 1
                else:
                    break
            if space_length >= needed_length:
                return i
            i += space_length
        else:
            i += 1
    return None

def compact_disk(blocks, debug=False):
    """Compact the disk by moving whole files from right to left."""
    if debug:
        print("\nInitial state:")
        print_block_map(blocks)

    # Find file boundaries
    file_boundaries = find_file_boundaries(blocks)

    # Process files in order of decreasing file ID
    for file_id in sorted(file_boundaries.keys(), reverse=True):
        start, length = file_boundaries[file_id]

        # Find leftmost space that can fit this file
        leftmost = find_leftmost_space(blocks, start, length)
        if leftmost is not None:
            # Move the file
            file_data = blocks[start:start + length]
            blocks[leftmost:leftmost + length] = file_data
            blocks[start:start + length] = ['.'] * length

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

def solve_part2(disk_map, debug=False):
    """Solve part 2 of the puzzle."""
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

    # Solve part 2
    result = solve_part2(disk_map, debug)

    end_time = time.time()
    print(f"\nFilesystem checksum: {result}")
    print(f"Time taken: {end_time - start_time:.2f} seconds")
    return result

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description='Day 9: Disk Fragmenter - Part 2')
    parser.add_argument('--debug', action='store_true', help='Enable debug output')
    args = parser.parse_args()

    result = main("input/day09.txt", args.debug)
    print(f"\nFinal answer: {result}")  # Should be 2858 for the example
