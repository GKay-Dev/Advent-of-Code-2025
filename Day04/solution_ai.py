import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def count_adjacent_rolls(grid: list[list[str]], row: int, col: int) -> int:
    """Count adjacent '@' characters in all 8 directions."""
    count = 0
    rows, cols = len(grid), len(grid[0])
    
    # Check all 8 adjacent positions
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            
            nr, nc = row + dr, col + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "@":
                count += 1
    
    return count


def find_accessible_rolls(grid: list[list[str]]) -> list[tuple[int, int]]:
    """Find all rolls that are accessible (have fewer than 4 adjacent rolls)."""
    accessible = []
    
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@" and count_adjacent_rolls(grid, row, col) < 4:
                accessible.append((row, col))
    
    return accessible


def grid_from_strings(strings: list[str]) -> list[list[str]]:
    """Convert list of strings to 2D list for easier manipulation."""
    return [list(s) for s in strings]


# Part One
@timer(name="Part One")
def Part_One(paper_rolls_grid: list[str]) -> None:
    grid = grid_from_strings(paper_rolls_grid)
    accessible_count = len(find_accessible_rolls(grid))
    
    print(f"Part One - Number of rolls of paper that can be accessed by a forklift : {accessible_count}")


# Part Two
@timer(name="Part Two")
def Part_Two(paper_rolls_grid: list[str]) -> None:
    grid = grid_from_strings(paper_rolls_grid)
    total_removed = 0
    
    # Iteratively remove accessible rolls until none remain
    while True:
        accessible = find_accessible_rolls(grid)
        
        if not accessible:
            break
        
        for row, col in accessible:
            grid[row][col] = "."
        
        total_removed += len(accessible)
    
    print(f"Part Two - Number of rolls of paper in total that can be removed by the Elves and their forklifts : {total_removed}")


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