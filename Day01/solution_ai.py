import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One: Count exact landings on position 0 using walrus operator
@timer(name="Part One")
def Part_One(rotation: list[str]) -> None:
    ptr = 50
    # One-liner: update ptr and count zeros in single expression using walrus operator
    ctr = sum(1 for r in rotation if (ptr := (ptr - int(r[1:]) if r[0] == 'L' else ptr + int(r[1:])) % 100) == 0)

    print("Part One - Actual Password to open the door:", ctr)


# Part Two: Count all zero crossings using boolean arithmetic
@timer(name="Part Two")
def Part_Two(rotation: list[str]) -> None:
    ptr = 50
    ctr = 0

    for r in rotation:
        direction, distance = r[0], int(r[1:])
        
        if direction == 'L':
            # Boolean expressions convert to 0/1 for arithmetic
            ctr += abs((ptr - distance) // 100) - (ptr == 0)
            ptr = (ptr - distance) % 100
            ctr += (ptr == 0)
        else:
            ctr += (ptr + distance) // 100
            ptr = (ptr + distance) % 100

    print("Part Two - Using password method 0x434C49434B, Password to open the door:", ctr)


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=1, force_fetch=False)
    rotation = input_data.split('\n')

    print("-"*50)
    print("*** Day 1 - Secret Entrance [AI Version] ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(rotation)
    # Part_Two(rotation)    

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, rotation)
