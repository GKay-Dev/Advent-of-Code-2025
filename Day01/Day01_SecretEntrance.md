# [Day 1: Secret Entrance](https://adventofcode.com/2025/day/1)

## Problem-Solving Approach
- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse the input into a list of rotation instructions (direction + distance)

- **Part One**:
    - Start at position 50 on a circular track of length 100 (0-99).
    - Process each rotation instruction:
        - 'L' moves counter-clockwise (subtract distance)
        - 'R' moves clockwise (add distance)
    - Use modulo operation to wrap around the circular track.
    - Count how many times the pointer lands exactly on position 0.
    - Implemented using a simple loop with modulo arithmetic for efficiency.
    - **AI-based Optimized implementation**: Uses walrus operator (`:=`) in a generator expression for one-liner solution
    - Time complexity: O(n) where n is the number of instructions

- **Part Two**:
    - Similar to Part One, but count all zero crossings during movement, not just final positions.
    - For 'L' (counter-clockwise):
        - Check if starting at 0 (subtract 1 from count to avoid double-counting)
        - Count crossings using integer division: `abs((ptr - distance) // 100)`
        - Update pointer with modulo
        - Check if ending at 0 (add 1 to count)
    - For 'R' (clockwise):
        - Count crossings using integer division: `(ptr + distance) // 100`
        - Update pointer with modulo
    - This tracks all zero crossings throughout the journey, including multiple wraps around the track.
    - **AI-based Optimization**: Boolean expressions (`ptr == 0`) automatically convert to 1 (True) or 0 (False) for cleaner arithmetic

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
