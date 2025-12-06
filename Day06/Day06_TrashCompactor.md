# [Day 6: Trash Compactor](https://adventofcode.com/2025/day/6)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse input into a math worksheet with 5 rows: 4 operand rows and 1 operator row
    - Split lines by whitespace for Part One, preserve exact spacing for Part Two

- **Part One**:
    - Read problems left-to-right horizontally (standard reading direction)
    - Each column represents one complete problem
    - Numbers are stacked vertically in each column (read top-to-bottom)
    - Split each line by whitespace to get problem columns
    - For each column index, extract all operands from rows 0 to (n-1)
    - Apply the operator from the last row to calculate the result
    - Sum all problem results to get the grand total
    - Time complexity: O(problems × operands_per_problem)
    - Space complexity: O(problems × rows) for split data structure
    - **AI-based Optimization**:
        - Pre-split all lines once instead of repeatedly
        - Use list comprehension to extract operands in one pass
        - Directly accumulate results without intermediate variables
        - Eliminate redundant calculations
        - Same time complexity but cleaner, more Pythonic code

- **Part Two**:
    - Read problems right-to-left (cephalopod reading direction)
    - Each vertical column (read top-to-bottom) forms a complete number
    - Problems are separated by columns of spaces (including operator row)
    - Parse operator row structure to identify problem boundaries
    - Build `operations_list` by tracking spacing between operators
    - For each problem section:
        - Extract substring based on operator spacing
        - Read columns right-to-left within that section
        - Each column's digits (top-to-bottom) form one number
    - Calculate result using collected operands and operator
    - Sum all problem results to get the grand total
    - Time complexity: O(total_width × operand_rows)
    - Space complexity: O(problems) for operations list
    - **AI-based Optimization**:
        - Simplified operator row parsing logic
        - Direct substring extraction using calculated positions
        - Eliminated redundant string operations and `.strip()` calls
        - More efficient position tracking with single variable
        - Cleaner column iteration with range parameters
        - Same algorithmic complexity but improved readability

## Key Insights
- **Reading Direction Matters**: Part One reads left-to-right, Part Two reads right-to-left
- **Spacing Is Critical**: In Part Two, exact spacing determines which columns belong to which problem
- **Vertical Number Formation**: Each column (read top-to-bottom) forms a complete number, not individual digits
- **Operator Row Structure**: The spacing in the operator row reveals problem boundaries in Part Two
- **Problem Separation**: Full columns of spaces (including operator row) separate distinct problems
- **Split vs Preserve**: Part One can use `.split()` to ignore alignment; Part Two must preserve exact character positions
- **Position Tracking**: Maintaining current position in the string is essential for correct substring extraction in Part Two

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
