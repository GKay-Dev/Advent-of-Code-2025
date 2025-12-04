# [Day 4: Printing Department](https://adventofcode.com/2025/day/4)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse input into a 2D grid where `@` represents paper rolls and `.` represents empty space

- **Part One**:
    - Determine which paper rolls can be accessed by forklifts
    - A roll is accessible if it has **fewer than 4 adjacent rolls** in the 8 surrounding positions
    - Handle corners as special case (always accessible)
    - Separate logic for edges (top, bottom, left, right) with explicit boundary checks
    - Different counting logic for interior cells vs edge cells
    - Manually count adjacent `@` symbols based on position type
    - Time complexity: O(rows × cols)
    - Space complexity: O(1)
    - **AI-based Optimization**:
        - Unified algorithm for all positions using direction offsets `[-1, 0, 1]`
        - Single `count_adjacent_rolls()` function checks all 8 directions
        - Bounds checking handles edges and corners automatically
        - Convert strings to 2D list once for easier manipulation
        - Time complexity: O(rows × cols × 8) = O(rows × cols)
        - Space complexity: O(rows × cols) for grid conversion

- **Part Two**:
    - Simulate the removal process: once accessible rolls are removed, more may become accessible
    - Reuse `count_accessible_rolls()` with `remove_rolls` flag
    - Create mutable grid copy when removal is needed
    - Apply same edge/corner logic as Part One for each iteration
    - Convert back to strings after each removal pass
    - Loop until no more accessible rolls found
    - Time complexity: O(iterations × rows × cols) with overhead from string conversions
    - **AI-based Optimization**:
        - Convert to mutable 2D list once at start
        - Use `find_accessible_rolls()` to get all positions in one pass
        - Remove all accessible rolls simultaneously (batch removal)
        - Keep grid as list throughout, no repeated conversions
        - Continue until no accessible rolls remain
        - Time complexity: O(iterations × rows × cols) with better constant factors
        - Space complexity: O(rows × cols) for the mutable grid

## Key Insights
- **Original approach** handles corners/edges explicitly, leading to more code but clear separation
- **AI-optimized approach** uses uniform bounds checking, reducing code from ~120 lines to ~60 lines
- Direction offsets `[-1, 0, 1]` eliminate special cases for edges and corners
- Batch removal in Part Two is more efficient than iterating with conversions
- Greedy approach works because removing rolls can only make more accessible (never fewer)

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
