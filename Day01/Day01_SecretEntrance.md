# [Day 1: Secret Entrance](https://adventofcode.com/2025/day/1)

## Problem-Solving Approach
- **Read the input file**: Parse the provided input into a list of rotation instructions (direction + distance).

- **Part One**:
    - Start at position 50 on a circular track of length 100 (0-99).
    - Process each rotation instruction:
        - 'L' moves counter-clockwise (subtract distance)
        - 'R' moves clockwise (add distance)
    - Use modulo operation to wrap around the circular track.
    - Count how many times the pointer lands exactly on position 0.
    - Implemented using a simple loop with modulo arithmetic for efficiency.

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
