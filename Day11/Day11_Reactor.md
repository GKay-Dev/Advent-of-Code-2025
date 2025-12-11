# [Day 11: Reactor](https://adventofcode.com/2025/day/11)

## Problem-Solving Approach

- **Input Handling**:
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Each line has the format `src: dst1 dst2 ...`; parse into an adjacency list `device_paths: dict[str, list[str]]`.
    - Processing is directed only (edges from `src` to listed outputs).

- **Part One: Counting All Paths (`you` → `out`)**:
    - Goal: count every distinct path from `you` to `out`.
    - Use DFS with a `visited` set to avoid cycles.
    - Return path count directly (no need to store all paths).
    - Time: O(V + E) over reachable subgraph; Space: O(V) recursion + visited.

- **Part Two: Counting Paths Visiting Required Devices (`svr` → `out`, must visit `dac` and `fft`)**:
    - Goal: count paths that reach `out` and include both `dac` and `fft` in any order.
    - Use DFS + memoization:
        - State = `(node, mask)` where `mask` tracks which required devices have been visited (bitmask), or `(node, seen_frozenset)` in the non-bitmask variant.
        - Base case: at `out`, count only if all required have been visited.
        - Transition: for each neighbor, recurse with updated state (set the bit if current node is required).
        - Memo caches subproblem counts to avoid recomputation and exponential blow-up.
    - Time: O((V + E) × R) effectively linear in graph size, since each `(node, mask)` is computed once; Space: O(V × 2^R) for memo (small R).

## Algorithm Comparison

| Aspect | Part One | Part Two |
|--------|-----------|----------|
| Start / End | `you` → `out` | `svr` → `out` |
| Constraint | None beyond reachability | Must visit `dac` and `fft` |
| Traversal | DFS with `visited` | DFS with `visited` + memo |
| State | `(node, visited-set)` (implicit) | `(node, required-mask)` or `(node, frozenset)` |
| Output | Count of all paths | Count of paths that include all required devices |
| Complexity | O(V + E) reachable | O((V + E) × 2^R) with small R |

## Key Insights

- Avoid materializing paths; count during DFS.
- Prevent cycles with a `visited` set on the recursion stack.
- In Part Two, memoization over `(node, requirement-state)` turns the search from exponential to near-linear.
- Bitmasking is a compact, fast way to track a small fixed set of required nodes; a `frozenset` alternative is simpler to read but slightly heavier.
- Parsing once into an adjacency list keeps lookups O(1) per edge traversal.

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
