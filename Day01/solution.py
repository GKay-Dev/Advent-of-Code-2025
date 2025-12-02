import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from aoc_utils import get_input

# Get input (fetches from web if not cached, or use `save_to_file=False` to never save)
input = get_input(day=1, force_fetch=False)
rotation = input.split('\n')


# Part One
ptr = 50
ctr = 0

for r in rotation:
    direction, distance = r[0], int(r[1:])
    ptr = (ptr - distance if direction == 'L' else ptr + distance) % 100
    
    if ptr == 0:
        ctr += 1

print("Actual Password to open the door:", ctr)


# Part Two
ptr = 50
ctr = 0

for r in rotation:
    direction, distance = r[0], int(r[1:])

    if direction == 'L':
        if ptr == 0:
            ctr -= 1
        ctr += abs((ptr - distance) // 100)
        ptr = (ptr - distance) % 100
        if ptr == 0:
            ctr += 1
    else:
        ctr += (ptr + distance) // 100
        ptr = (ptr + distance) % 100

print("Using password method 0x434C49434B, Password to open the door:", ctr)
