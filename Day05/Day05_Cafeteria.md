# [Day 5: Cafeteria](https://adventofcode.com/2025/day/5)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse input into two sections: fresh ID ranges and available IDs to check

- **Part One**:
    - Determine which available ingredient IDs fall within fresh ID ranges
    - Preprocess ranges by parsing and merging overlapping/adjacent ranges
    - For each available ID, check if it exists in any fresh range
    - Linear iteration through ranges for each ID
    - Time complexity: O(m × n) where m = available IDs, n = merged ranges
    - Space complexity: O(n) for storing merged ranges
    - **AI-based Optimization**:
        - Implement binary search for range lookup instead of linear iteration
        - Ranges are already sorted after merging, enabling O(log n) searches
        - Use `is_id_fresh()` with binary search to find matching range
        - Replace loop with `sum()` and generator expression for cleaner code
        - Time complexity: O(m × log n) - significant speedup for large datasets
        - Space complexity: O(n) for merged ranges

- **Part Two**:
    - Count total number of ingredient IDs considered fresh across all ranges
    - Simply sum the size of each merged range: (end - start + 1)
    - No need to check individual IDs
    - Time complexity: O(n) where n = number of merged ranges
    - Space complexity: O(n) for storing ranges
    - Both implementations use same efficient approach with cleaner syntax

## Key Insights
- **Range Merging**: Critical optimization - merges overlapping ranges to reduce lookups from potentially millions to dozens
- **Binary Search**: Elevates Part One from O(m × n) to O(m × log n), making huge ID ranges tractable
- **Adjacent Range Merging**: Condition `start <= merged_ranges[-1][1] + 1` catches both overlapping and adjacent ranges
- **Part Two Simplification**: Once ranges are merged, counting is trivial - no individual ID checks needed
- **Greedy Merging**: Process ranges in sorted order and always merge with last range if possible

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
