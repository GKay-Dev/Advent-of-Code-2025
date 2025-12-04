import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Common function to count accessible rolls
def count_accessible_rolls(paper_rolls_grid: list[str], remove_rolls: int = 0) -> int:
    accessible_rolls = 0
    
    # Create a mutable copy of the grid if rolls are to be removed
    if remove_rolls:
        updated_paper_rolls_grid = [list(row_str) for row_str in paper_rolls_grid]

    for row, rolls in enumerate(paper_rolls_grid):
        for pos, roll in enumerate(rolls):

            if roll != "@":
                continue
            
            if (row == 0 and (pos == 0 or pos == len(rolls)-1)) or (row == len(paper_rolls_grid)-1 and (pos == 0 or pos == len(rolls)-1)):
                # Corners are always accessible
                accessible_rolls += 1
                if remove_rolls:
                    updated_paper_rolls_grid[row][pos] = "."
                continue
            
            if row != 0 and pos != 0 and row != len(paper_rolls_grid)-1 and pos != len(rolls)-1:    # Exclude edges
                if (
                    (rolls[pos-1] == "@") +
                    (rolls[pos+1] == "@") +
                    (paper_rolls_grid[row-1][pos-1] == "@") +
                    (paper_rolls_grid[row-1][pos] == "@") +
                    (paper_rolls_grid[row-1][pos+1] == "@") +
                    (paper_rolls_grid[row+1][pos-1] == "@") +
                    (paper_rolls_grid[row+1][pos] == "@") +
                    (paper_rolls_grid[row+1][pos+1] == "@")
                    ) < 4:
                    accessible_rolls += 1
                    if remove_rolls:
                        updated_paper_rolls_grid[row][pos] = "."
                else:
                    continue
            else:
                if row == 0:
                    # Top edge
                    if (
                        (rolls[pos-1] == "@") +
                        (rolls[pos+1] == "@") +
                        (paper_rolls_grid[row+1][pos-1] == "@") +
                        (paper_rolls_grid[row+1][pos] == "@") +
                        (paper_rolls_grid[row+1][pos+1] == "@")
                        ) < 4:
                        accessible_rolls += 1
                        if remove_rolls:
                            updated_paper_rolls_grid[row][pos] = "."
                elif row == len(paper_rolls_grid)-1:
                    # Bottom edge
                    if (
                        (rolls[pos-1] == "@") +
                        (rolls[pos+1] == "@") +
                        (paper_rolls_grid[row-1][pos-1] == "@") +
                        (paper_rolls_grid[row-1][pos] == "@") +
                        (paper_rolls_grid[row-1][pos+1] == "@")
                        ) < 4:
                        accessible_rolls += 1
                        if remove_rolls:
                            updated_paper_rolls_grid[row][pos] = "."
                elif pos == 0:
                    # Left edge
                    if (
                        (rolls[pos+1] == "@") +
                        (paper_rolls_grid[row-1][pos] == "@") +
                        (paper_rolls_grid[row-1][pos+1] == "@") +
                        (paper_rolls_grid[row+1][pos] == "@") +
                        (paper_rolls_grid[row+1][pos+1] == "@")
                        ) < 4:
                        accessible_rolls += 1
                        if remove_rolls:
                            updated_paper_rolls_grid[row][pos] = "."
                else:
                    # Right edge
                    if (
                        (rolls[pos-1] == "@") +
                        (paper_rolls_grid[row-1][pos-1] == "@") +
                        (paper_rolls_grid[row-1][pos] == "@") +
                        (paper_rolls_grid[row+1][pos-1] == "@") +
                        (paper_rolls_grid[row+1][pos] == "@")
                        ) < 4:
                        accessible_rolls += 1
                        if remove_rolls:
                            updated_paper_rolls_grid[row][pos] = "."
    
    if remove_rolls:
        updated_paper_rolls_grid = ["".join(row_list) for row_list in updated_paper_rolls_grid]
        return accessible_rolls, updated_paper_rolls_grid
    return accessible_rolls


# Part One
@timer(name="Part One")
def Part_One(paper_rolls_grid) -> None:
    accessible_rolls = count_accessible_rolls(paper_rolls_grid)

    print(f"Part One - Number of rolls of paper that can be accessed by a forklift : {accessible_rolls}")


# Part Two
@timer(name="Part Two")
def Part_Two(paper_rolls_grid) -> None:
    additional_accessible_rolls, updated_paper_rolls_grid = count_accessible_rolls(paper_rolls_grid, remove_rolls=1)
    accessible_rolls = additional_accessible_rolls
    
    while additional_accessible_rolls:
        additional_accessible_rolls, updated_paper_rolls_grid = count_accessible_rolls(updated_paper_rolls_grid, remove_rolls=1)
        accessible_rolls += additional_accessible_rolls

    print(f"Part Two - Number of rolls of paper in total that can be removed by the Elves and their forklifts : {accessible_rolls}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=4, force_fetch=False)
    paper_rolls_grid = input_data.splitlines()      # Process input as needed

    print("-"*50)
    print("*** Day 4 - Printing Department ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(paper_rolls_grid)
    # Part_Two(paper_rolls_grid)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, paper_rolls_grid)