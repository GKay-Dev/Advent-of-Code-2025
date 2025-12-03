# [Day 3: Lobby](https://adventofcode.com/2025/day/3)

## Problem-Solving Approach
- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse the input into a list of battery bank strings (one per line)

- **Part One**:
    - Find the lexicographically largest 2-digit subsequence from each battery bank while preserving order
    - Algorithm:
        - Sort unique digits in descending order to find candidates
        - Find the position of the maximum digit in the original string
        - **Case 1**: If max digit is at the last position:
            - First battery (bat1) = second largest unique digit
            - Second battery (bat2) = max digit itself
        - **Case 2**: If max digit is not at the last position:
            - First battery (bat1) = max digit
            - Second battery (bat2) = largest digit that appears after max digit's position
        - This ensures order preservation while maximizing the 2-digit value
    - Example: '9275' → Find '9' at position 0, then find largest digit in '275' which is '7' → '97'
    - Example: '1214' → Max '4' at last position, so use second largest '2' first → '24'
    - Sum all output joltages from each battery bank
    - Time complexity: O(n log n) per bank due to sorting (where n is unique digit count)
    - Space complexity: O(n) for storing unique sorted digits

- **Part Two**:
    - Find the lexicographically largest 12-digit subsequence from each battery bank while preserving order
    - Uses a greedy monotonic stack algorithm:
        - Calculate drops_allowed = len(bank) - 12
        - Iterate through each digit:
            - Pop smaller digits from stack while drops are available and current digit is larger
            - Append current digit to stack
        - If loop completes (strictly decreasing case), trim stack to first 12 digits
    - This greedy approach ensures the largest possible number by:
        - Removing smaller leading digits when a larger digit appears
        - Preserving order of remaining digits
        - Stopping removals once we reach the target length
    - Example: '987654321012' with K=12 → entire string (already 12 digits)
    - Example: '12345678901234' with K=12 → '45678901234' (removes '123' to maximize)
    - Sum all output joltages from each battery bank
    - Time complexity: O(n) per bank where n is the length of the battery string
    - Space complexity: O(K) = O(12) for the stack

**Note**: The AI version (`solution_ai.py`) uses a suffix maximum approach for Part One (O(n) time) and adds an early exit optimization for Part Two when drops_allowed reaches 0.

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
