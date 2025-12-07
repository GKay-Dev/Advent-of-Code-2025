import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(tachyon_manifold) -> None:
    split_times = 0
    pos_beam = [tachyon_manifold[0].index("S")]  # current beam columns
    manifold_with_beams = [tachyon_manifold[0]]  # rows with drawn beams

    for row in tachyon_manifold[1:]:
        # Fast path: no splitters in this row
        if "^" not in row:
            new_row = "".join(["|" if pos in pos_beam else "." for pos in range(len(row))])
            manifold_with_beams.append(new_row)
            continue

        pos_splitter = [idx for idx, elem in enumerate(row) if elem == "^"]
        pos_beam = [idx for idx, elem in enumerate(manifold_with_beams[-1]) if elem == "|"]
        new_row = ""
        for idx, elem in enumerate(row):
            # Skip over positions already written (due to inserting |^|)
            if len(new_row) == idx + 1:
                continue
            if idx in pos_splitter:
                # Split only if a beam arrives at this splitter
                if manifold_with_beams[-1][idx] == "|":
                    # Insert split visual; avoid duplicating adjacent pipes
                    if new_row[-1] != "|":
                        new_row = new_row[:-1] + "|^|"
                    else:
                        new_row += "^|"
                    split_times += 1
                else:
                    new_row += "^"
            elif elem in pos_beam:
                # Continue straight beam; coalesce adjacent pipes
                if new_row[-1] != "|":
                    new_row += "|"
                else:
                    continue
            else:
                # Empty stays empty unless beam passes through
                new_row += "." if "." == manifold_with_beams[-1][idx] else "|"

        pos_beam = [idx for idx, elem in enumerate(new_row) if elem == "|"]
        manifold_with_beams.append(new_row)

    # # Persist visualization for debugging
    # with open("Day07/output.txt", "w") as f:
    #     for line in manifold_with_beams:
    #         f.write(line + "\n")

    print(f"Part One - No of times will the beam be split : {split_times}")


# Part Two
@timer(name="Part Two")
def Part_Two(tachyon_manifold) -> None:
    width = len(tachyon_manifold[0])
    current = {tachyon_manifold[0].index("S"): 1}  # col -> timeline count at this row
    completed_timelines = 0

    for row in tachyon_manifold[1:]:
        next_beams = {}

        for col, count in current.items():
            if row[col] == "^":
                # Split into left and right timelines
                for offset in (-1, 1):
                    new_col = col + offset
                    if 0 <= new_col < width:
                        next_beams[new_col] = next_beams.get(new_col, 0) + count
                    else:
                        # Off-grid splits exit sideways
                        completed_timelines += count
            else:
                # Continue straight down
                next_beams[col] = next_beams.get(col, 0) + count
        current = next_beams

    # Any remaining beams exit the bottom
    completed_timelines += sum(current.values())

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