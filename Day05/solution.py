import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Preprocess fresh ID ranges into a list of tuples and merge overlapping ranges for efficiency
def preprocess_ranges(fresh_ids_range):
    ranges = []
    
    for id_range in fresh_ids_range:
        start, end = map(int, id_range.split("-"))
        ranges.append((start, end))
    
    ranges.sort()
    merged_ranges = []

    for start, end in ranges:
        if merged_ranges and start <= merged_ranges[-1][1] + 1:
            merged_ranges[-1] = (merged_ranges[-1][0], max(merged_ranges[-1][1], end))
        else:
            merged_ranges.append((start, end))
    
    return merged_ranges


# Part One
@timer(name="Part One")
def Part_One(fresh_ids_range, available_ids) -> None:
    fresh_ids_available = 0
    merged_ranges = preprocess_ranges(fresh_ids_range)

    for id in available_ids:
        for start, end in merged_ranges:
            if start <= id <= end:
                fresh_ids_available += 1
                break

    print(f"Part One - Number of available ingredient IDs that are fresh : {fresh_ids_available}")


# Part Two
@timer(name="Part Two")
def Part_Two(fresh_ids_range, available_ids=None) -> None:
    fresh_ids_available = 0
    merged_ranges = preprocess_ranges(fresh_ids_range)
    
    for start, end in merged_ranges:
        fresh_ids_available += (end - start + 1)
    
    print(f"Part Two - Number of ingredient IDs that are considered to be fresh according to the fresh ingredient ID ranges : {fresh_ids_available}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=5, force_fetch=False)

    # Process input as needed
    fresh_ids_range, available_ids = input_data.split("\n\n")
    fresh_ids_range = fresh_ids_range.splitlines()
    available_ids = list(map(int, available_ids.splitlines()))

    print("-"*50)
    print("*** Day 5 - Cafeteria ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(fresh_ids_range, available_ids)
    # Part_Two(fresh_ids_range)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, fresh_ids_range, available_ids)