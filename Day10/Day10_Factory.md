# [Day 10: Factory](https://adventofcode.com/2025/day/10)

## Problem-Solving Approach

- **Input Handling**: 
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse each machine line containing: indicator lights `[.##.]`, button configs `(1,3)`, and joltage requirements `{3,5,4,7}`
    - Use generator function to yield parsed components (target state, buttons list, joltages list)

- **Part One: Minimum Button Presses for Indicator Lights**:
    - Each button toggles specific lights (XOR operation in binary field GF(2))
    - Problem: Find minimum button presses where each button pressed 0 or 1 times
    - Approach: **Gaussian Elimination over GF(2)**
    - Build augmented matrix `[A|b]` where:
        - Each row = equation for one light
        - Each column = one button (coefficient 1 if button affects this light)
        - Last column = target state (1 if light should be on, 0 if off)
    - Perform row reduction to **Reduced Row Echelon Form (RREF)** using XOR operations
    - Identify pivot columns (determined variables) and free columns (free variables)
    - Check for inconsistency (impossible configuration)
    - **Key optimization**: Try all `2^k` combinations of free variables (k = number of free variables)
    - For each combination, back-substitute to find pivot variables
    - Track minimum sum of button presses across all valid solutions
    - Time complexity: O(lights × buttons²) for Gaussian elimination + O(2^free_vars) for search
    - Space complexity: O(lights × buttons) for matrix
    - **Why this works**: Button presses in GF(2) are commutative and idempotent (pressing twice = not pressing)

- **Part Two: Minimum Button Presses for Joltage Counters**:
    - Each button adds 1 to specific counters (integer arithmetic, not XOR)
    - Problem: Find minimum button presses where buttons can be pressed any non-negative integer times
    - This is an **Integer Linear Programming (ILP)** problem: minimize `sum(x)` subject to `Ax = b`, `x ≥ 0`
    - Approach: **Gaussian Elimination over Rationals + Recursive Search**
    - Build augmented matrix using `Fraction` for exact arithmetic (avoid floating-point errors)
    - Perform Gaussian elimination to RREF over rationals
    - Express pivot variables as: `pivot = constant - sum(coeff × free_var)`
    - **Key challenge**: Unlike Part 1, free variables can take any non-negative integer value
    - Calculate tight upper bounds for each free variable:
        - Start with `max(joltages)` as initial bound
        - For constraints where `coeff > 0`, bound by `constant / coeff`
        - Only apply bound if no other free variables have negative coefficients
        - Expand bound if too restrictive (0 → `max(joltages)`)
    - **Recursive search with aggressive pruning**:
        - Prune if current sum already exceeds best found solution
        - Try values 0 to upper_bound for each free variable
        - For each combination, compute pivot variables and validate (non-negative integers)
        - Track minimum total button presses
    - Time complexity: O(counters × buttons²) for elimination + O(product of upper_bounds) for search
    - Space complexity: O(counters × buttons) for matrix
    - **Critical optimization**: Upper bounds dramatically reduce search space (e.g., from millions to hundreds)

## Algorithm Comparison

| Aspect | Part One | Part Two |
|--------|----------|----------|
| **Mathematical Field** | GF(2) (binary/XOR) | Rationals/Integers |
| **Button Press Range** | {0, 1} only | {0, 1, 2, ..., ∞} |
| **Problem Type** | System of linear equations over GF(2) | Integer Linear Programming (ILP) |
| **Matrix Operations** | XOR (^) for elimination | Subtraction/division for elimination |
| **Free Variable Search** | O(2^k) - all binary combinations | O(product of bounds) - bounded integers |
| **Data Type** | int (0 or 1) | Fraction (exact arithmetic) |
| **Validation** | Always valid after back-substitution | Must check non-negative integer constraint |
| **Key Challenge** | Finding free variables | Calculating tight bounds for search space |

## Key Insights
- **GF(2) vs Integers**: Part 1 uses binary field (toggle logic), Part 2 uses integer arithmetic (additive counters)
- **Exact Arithmetic**: Using `Fraction` instead of float prevents rounding errors in rational calculations
- **Free Variables**: Variables not determined by pivot equations; can take any value in valid range
- **Pivot Variables**: Uniquely determined by free variables through back-substitution
- **Upper Bound Tightening**: Critical for Part 2 performance; reduces search space by orders of magnitude
- **Inconsistency Detection**: Row with all zeros except last column means no solution exists
- **Pruning Strategy**: Stop exploring paths where partial sum already exceeds best known solution
- **Coefficient Sign Matters**: Negative coefficients in constraints mean other free vars can compensate, so bounds must be looser
- **Generator Pattern**: Using `yield` for parsing allows memory-efficient iteration over machines
- **RREF Form**: Makes it easy to identify free variables (columns without pivot 1's)

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
