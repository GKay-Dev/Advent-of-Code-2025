# [Day 12: Christmas Tree Farm](https://adventofcode.com/2025/day/12)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse input into two sections separated by blank lines:
        - **Shape definitions**: Index followed by colon, then visual grid where `#` = part of shape, `.` = empty
        - **Region definitions**: `WxH: q0 q1 q2 ...` format specifying width, height, and quantity of each shape needed
    - All shapes have exactly **7 cells** each (heptominoes)

- **Part One: Polyomino Packing Problem**:
    - Determine how many regions can fit all their required presents
    - Presents can be **rotated** (4 rotations) and **flipped** (2 reflections) = up to 8 orientations
    - Shapes cannot overlap (`#` cells), but empty space (`.`) in shape doesn't block other shapes
    - Grid cells don't all need to be filled - just need to place all required pieces
    - This is an **NP-hard exact cover variant** problem
    
    - **Algorithm Strategy - Multi-Phase Approach**:
        1. **Quick Rejection**: If `total_pieces × 7 > width × height`, impossible (not enough space)
        2. **Greedy Packing** (fast path): Try placing pieces in first available position
           - Multiple ordering strategies: by constraint level, by index, reverse order
           - If any greedy strategy succeeds → region fits
        3. **Backtracking with Pruning** (fallback): For cases where greedy fails
           - Use "first empty cell" strategy: always target the topmost-leftmost empty cell
           - This cell MUST be covered by some piece, reducing branching factor
           - Precompute all placements that cover each cell for O(1) lookup
           - Node limit to prevent exponential blowup on pathological cases

    - **Key Optimizations**:
        - **Orientation Precomputation**: Calculate all 8 orientations once per shape, deduplicate symmetric ones
        - **Placement Indexing**: For each shape and cell, precompute which placements cover that cell
        - **MRV Heuristic**: Sort pieces by number of possible orientations (most constrained first)
        - **Set-based Collision Detection**: O(1) overlap checking using Python sets
        - **Early Termination**: Node limits prevent infinite loops on hard instances

    - **Greedy Strategies**:
        | Strategy | Ordering | Rationale |
        |----------|----------|-----------|
        | Constraint-first | Fewer orientations first | Place difficult pieces early when grid is empty |
        | Index order | Shape index ascending | Deterministic baseline |
        | Reverse constraint | More orientations first | Sometimes flexible pieces block less |

    - **Backtracking Details**:
        - Target first empty cell (row-major order)
        - Only try placements of current piece that cover this cell
        - If no valid placement exists → backtrack immediately
        - Node limit prevents excessive computation on unsolvable cases

    - **Time Complexity**: 
        - Greedy: O(pieces × orientations × width × height) per region
        - Backtracking: O(branching_factor^depth) worst case, but pruning makes it practical
    - **Space Complexity**: O(width × height) for grid state + O(pieces × placements) for precomputation

- **Part Two**: No part two for this day

## Data Structures

| Structure | Type | Purpose |
|-----------|------|---------|
| `shapes` | `dict[int, tuple]` | Shape index → tuple of (row, col) coordinates |
| `regions` | `list[tuple]` | List of (width, height, quantities) |
| `shape_orientations` | `dict[int, list]` | Shape index → list of all unique orientations |
| `placements_covering_cell` | `dict[int, dict]` | Shape → Cell → list of placements covering that cell |
| `grid` | `set` | Currently occupied cells for backtracking |

## Algorithm Comparison

| Approach | Speed | Completeness | Use Case |
|----------|-------|--------------|----------|
| Space Check | O(1) | Necessary only | Quick rejection |
| Greedy | Fast | Incomplete | Most solvable cases |
| Backtracking | Slow | Complete | Greedy failures |
| DLX (not used) | Medium | Complete | Exact cover problems |

## Key Insights
- **Heptominoes**: All shapes are 7-cell polyominoes, making space calculations straightforward
- **Greedy Often Works**: For well-designed puzzle inputs, greedy placement usually succeeds
- **First Empty Cell**: Forcing coverage of a specific cell dramatically reduces search space
- **Orientation Deduplication**: Symmetric shapes have fewer than 8 unique orientations
- **Incomplete is OK**: For competition, getting most answers right quickly beats perfect but slow
- **Node Limits**: Practical compromise between correctness and runtime

## Solutions
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to formulate the solution (Couldn't figure it out myself for today's challenge)
