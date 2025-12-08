# [Day 8: Playground](https://adventofcode.com/2025/day/8)

## Problem-Solving Approach

- **Input Handling**:
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse each line into integer 3D coordinates `(x, y, z)`.
    - Compute pairwise distances once per run (optionally reused).

- **Part One: 1000 Closest Pair Connections**:
    - Compute all pairwise **squared** Euclidean distances (sqrt not needed for ordering).
    - Sort pairs by distance ascending.
    - Process the first **1000 pairs in order** (count pairs, not successful unions).
    - Maintain connectivity with Union-Find (path compression + union by rank).
    - After processing pairs, collect component sizes and multiply the three largest.

- **Part Two: Connect Until Single Circuit**:
    - Reuse the sorted distance list.
    - Iterate pairs shortest-first; union when endpoints are in different components.
    - Track the last successful union; stop when only one component remains.
    - Output the product of the **X coordinates** of the last two boxes connected.

## Algorithm Comparison

| Aspect | `solution.py` | `solution_ai.py` |
| --- | --- | --- |
| Union-Find style | Procedural functions (`find`, `union`) | `UnionFind` class with `__slots__` |
| Distance metric | Squared Euclidean (uses sqrt in that file; can omit) | Squared Euclidean (no sqrt) |
| Pair selection (Part 1) | First 1000 pairs, even if already connected | Same |
| Stop condition (Part 2) | When 1 circuit remains; track last union | Same |
| Distance reuse | Recomputed per part | Precomputed once, reused |

## Key Insights
- **Squared distances suffice** for ordering; avoid `sqrt` for speed.
- **Process pairs, not unions** in Part One (failed unions still count toward 1000).
- **Path compression + union by rank** keeps near O(α(n)) per operation.
- Precomputing and **reusing the sorted distance list** halves the work across parts.
- The **last successful union** determines the X-coordinate product for Part Two.

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
