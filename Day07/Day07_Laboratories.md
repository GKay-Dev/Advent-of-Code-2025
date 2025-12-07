# [Day 7: Laboratories](https://adventofcode.com/2025/day/7)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse input into a tachyon manifold: grid of rows with `S` (start), `^` (splitter), and `.` (empty space)
    - Process row-by-row downward from the starting position

- **Part One: Counting Beam Splits**:
    - Tachyon beam enters at position `S` and moves downward through each row
    - When beam encounters empty space `.`, it continues straight down in same column
    - When beam encounters splitter `^`, it splits into two beams: one going left, one going right
    - Track all active beam positions after each row
    - Count total number of splits that occur
    - Time complexity: O(height × active_beams)
    - Space complexity: O(active_beams)
    - **Original Approach (`solution.py`)**:
        - Build complete visual representation of beam paths (storing every row)
        - Use fast path optimization for rows without splitters
        - For rows with splitters: reconstruct character-by-character with pipe symbols
        - Store entire manifold with beams drawn (unnecessary overhead)
        - If required, persist visualization to `output.txt` for debugging (code block is commented)
        - **Drawback**: String manipulation overhead; O(width × height) memory for visualization
    - **AI-based Optimization (`solution_ai.py`)**:
        - Track only active beam positions using a **set** (no visualization needed)
        - For each row, iterate through current beam positions:
          - If position has splitter `^`, add both left (col-1) and right (col+1) to next set
          - Otherwise, continue straight (add col to next set)
        - Filter out off-grid positions (col < 0 or col >= width)
        - **Improvement**: Eliminated string building and grid storage; O(active_beams) space instead of O(w×h)
        - Set operations provide O(1) lookups vs O(n) list searches

- **Part Two: Counting Quantum Timelines**:
    - Single tachyon particle uses many-worlds interpretation: splits into multiple timelines at each splitter
    - Each timeline independently follows the beam logic (left or right path at splitter)
    - When multiple timelines reach same column, their counts accumulate
    - Count total number of distinct timelines that exit the manifold
    - Time complexity: O(height × unique_columns)
    - Space complexity: O(unique_columns)
    - **Original Approach (`solution.py`)**:
        - Use dictionary: column → timeline count at current row
        - For each row, process each active column and its timeline count
        - At splitter: multiply timeline count to both left and right columns
        - Track off-grid exits explicitly by adding to `completed_timelines` variable
        - After all rows, add remaining timelines to total
    - **AI-based Optimization (`solution_ai.py`)**:
        - Same core algorithm but **simplified logic flow**
        - Removed explicit off-grid tracking (off-grid beams naturally excluded from next dictionary)
        - Cleaner boundary checks: only add to `next_beams` if 0 ≤ col < width
        - Sum all remaining timelines at end (no separate completed_timelines variable)
        - **Improvement**: Simplified conditional logic; off-grid beams eliminated naturally instead of explicit tracking

## Algorithm Comparison

| Aspect | Part One Original | Part One Optimized | Part Two (Both) |
|--------|-------------------|-------------------|-----------------|
| **Primary Data Structure** | List + String | Set | Dictionary |
| **Tracking** | Beam positions + Full visualization | Beam positions only | Column → Timeline count |
| **Memory Usage** | O(width × height) | O(active_beams) | O(unique_columns) |
| **String Operations** | Heavy (building each row) | None | None |
| **Off-grid Handling** | Implicit in filtering | Implicit in filtering | Explicit (original) vs Implicit (optimized) |
| **Split Counting** | Explicit counter | Explicit counter | Implicit in count multiplication |

## Key Insights
- **Visualization is Optional**: Tracking only active positions eliminates memory overhead without losing correctness
- **Set vs List**: Set provides O(1) lookups; list requires O(n) searches—critical for frequent membership tests
- **Many-Worlds Multiplication**: Timeline counts multiply at splitters; same column + different timelines = sum counts
- **Boundary Conditions**: Off-grid beams naturally excluded by range checks; no explicit tracking needed
- **Directional Consistency**: Beams always move downward (simpler than multi-directional traversal problems)
- **Dictionary Aggregation**: Multiple timelines reaching same column naturally aggregate via `dict.get(col, 0) + count`
- **Row-by-Row Processing**: No need to store entire grid; process one row at a time for memory efficiency

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
