import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(tachyon_manifold) -> None:
    """Count beam splits by tracking beam positions row by row."""
    split_times = 0
    pos_beam = {tachyon_manifold[0].index("S")}  # Use set for O(1) lookup
    
    for row in tachyon_manifold[1:]:
        new_beam = set()
        
        for col in pos_beam:
            if col < len(row) and row[col] == "^":
                # Split: beam goes left and right
                split_times += 1
                new_beam.add(col - 1)
                new_beam.add(col + 1)
            else:
                # Continue straight down
                new_beam.add(col)
        
        # Filter out off-grid positions
        pos_beam = {col for col in new_beam if 0 <= col < len(row)}
    
    print(f"Part One - No of times will the beam be split : {split_times}")


# Part Two
@timer(name="Part Two")
def Part_Two(tachyon_manifold) -> None:
    """Count distinct timelines using many-worlds interpretation."""
    width = len(tachyon_manifold[0])
    # Map: column -> count of timelines at that column
    current = {tachyon_manifold[0].index("S"): 1}
    
    for row in tachyon_manifold[1:]:
        next_beams = {}
        
        for col, count in current.items():
            if row[col] == "^":
                # Split: multiply timelines going left and right
                left, right = col - 1, col + 1
                
                if 0 <= left < width:
                    next_beams[left] = next_beams.get(left, 0) + count
                if 0 <= right < width:
                    next_beams[right] = next_beams.get(right, 0) + count
            else:
                # Continue straight
                next_beams[col] = next_beams.get(col, 0) + count
        
        current = next_beams
    
    # Sum all remaining timelines
    completed_timelines = sum(current.values())
    print(f"Part Two - Total number of different timelines would a single tachyon particle end up on : {completed_timelines}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=7, force_fetch=False)

    # Process input as needed
    tachyon_manifold = input_data.splitlines()

    print("-"*50)
    print("*** Day 7 - Laboratories ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(tachyon_manifold)
    # Part_Two(tachyon_manifold)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, tachyon_manifold)