# [Day 2: Gift Shop](https://adventofcode.com/2025/day/2)

## Problem-Solving Approach
- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse the input into comma-separated ID ranges (format: "start-end")

- **Part One**:
    - Parse each range into `range_start` and `range_end`
    - Skip ranges where both bounds have odd length or start with '0'
    - Adjust bounds to nearest even-length numbers:
        - If `range_start` has odd length, round up to next even-length number
        - If `range_end` has odd length, round down to previous even-length number
    - Split each bound into two halves
    - Adjust the first half of `range_start` upward if it's less than second half
    - Adjust the first half of `range_end` downward if it's greater than second half
    - Sum all numbers formed by repeating each base value twice: `base * 2` → `basebase`
    - **Optimization**:
        - Use mathematical formula: `repeated_number = base * (10^half_len + 1)`
        - Example: For 4-digit number `1212 = 12 * 101 = 12 * (10^2 + 1)`
        - Calculate base range using ceiling/floor division instead of string manipulation
        - Use arithmetic series sum: `sum = count * (min_base + max_base) / 2 * multiplier`
        - Eliminates string concatenation overhead
        - Time complexity: O(1) per length instead of O(n) per base value

- **Part Two**
    - Parse each range into `range_start` and `range_end`
    - Track seen IDs to avoid duplicates (e.g., 1111 can be 1*4 or 11*2)
    - Process each digit length in the range separately
    - For each length, try all divisors (block sizes):
        - Only check if block size divides length evenly
        - Example: 6-digit number can have blocks of size 1, 2, or 3
    - For each valid block size:
        - Generate all possible base patterns (from `10^(block-1)` to `10^block - 1`)
        - Repeat each base the required number of times
        - Check if resulting number falls within the range
        - Add to sum if valid and not already counted
    - Early exit when repeated number exceeds upper bound
    - **Optimization**:
        - Pre-calculate multiplier using mathematical formula instead of string repetition
        - Formula: `multiplier = sum(10^(block*i) for i in range(reps))`
        - Example: For block=2, reps=3: `121212 = 12 * 10101 = 12 * (10^4 + 10^2 + 1)`
        - Calculate tighter base range bounds using ceiling/floor division
        - Convert repeated number using multiplication: `repeated_num = base * multiplier`
        - Keep set for duplicate tracking (necessary for correctness)
        - Time complexity: O(d * b * n) where d is digit lengths, b is block sizes, n is bases per block
