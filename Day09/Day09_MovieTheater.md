# [Day 9: Movie Theater](https://adventofcode.com/2025/day/9)

## Problem-Solving Approach

- **Input Handling**:
    - Fetch input from Advent of Code website using session token stored in `.env` file
    - Cache input to `input.txt` for subsequent runs (optional with `save_to_file` parameter)
    - Parse each line into a coordinate pair `(x, y)` representing red tile locations
    - Red tiles form a closed loop where consecutive tiles are connected by green tiles

- **Part One: Largest Rectangle with Red Corners**:
    - Compute all pairwise rectangles using combinations of red tile pairs
    - For each pair of red tiles, treat them as opposite corners of a rectangle
    - Calculate area as `(|x1 - x2| + 1) × (|y1 - y2| + 1)`
    - Track and return the largest area found
    - Time complexity: O(n²) where n is number of red tiles
    - Space complexity: O(1) (only tracking maximum area)
    - **Approach**: Simple brute force enumeration of all possible rectangles

- **Part Two: Largest Rectangle with Red Corners (Red/Green Tiles Only)**:
    - Red tiles form a rectilinear polygon boundary with green tiles connecting them
    - All tiles inside the polygon are also green
    - Rectangle must contain **only** red and green tiles (no other colors allowed)
    - **Key Constraint**: No polygon edge can cross through the rectangle interior
    
    - **Algorithm Steps**:
        1. **Build Polygon Structure**: Create edges between consecutive red tiles; separate into horizontal and vertical edges
        2. **Index for Quick Lookup**: Store edges in dictionaries keyed by coordinate (y for horizontal, x for vertical) for O(1) boundary checks
        3. **Sort Tile Pairs by Area**: Process pairs in descending area order to enable early termination
        4. **For Each Candidate Rectangle**:
            - Verify the two non-red corners are inside/on the polygon boundary (using ray casting + boundary check)
            - Ensure no polygon edge passes through the rectangle interior (would indicate non-green tiles present)
        5. **Early Termination**: Break when area falls below current best (due to sorted order)
    
    - **Point-in-Polygon Detection**:
        - **Ray Casting Algorithm**: Cast a ray from point going right; count vertical edge crossings
        - **Boundary Check**: Direct lookup using indexed horizontal/vertical edges (O(1) vs O(n))
        - Odd crossings → point inside; even → outside; on boundary → included
    
    - **Edge Intersection Check**:
        - **Vertical edges**: If edge's x-coordinate is strictly between rectangle's x-bounds AND y-ranges overlap → crosses interior
        - **Horizontal edges**: If edge's y-coordinate is strictly between rectangle's y-bounds AND x-ranges overlap → crosses interior
        - Ensures entire rectangle is within the polygon boundary
    
    - Time complexity: O(n² × m) where n = red tiles, m = edges (typically ≈ n)
    - Space complexity: O(n) for edge storage and dictionaries
    
    - **Original Approach (solution.py)**:
        - Linear scan of all tile pairs without sorting
        - No early termination; always checks all pairs
        - Linear edge lookups in lists (O(n) per check)
        - **Drawback**: Full O(n²) execution regardless of input; slower boundary checks
    
    - **AI-based Optimization (solution_ai.py)**:
        - **Sort pairs by area descending** → enables early termination when area < current best
        - **Dictionary indexing** for O(1) boundary lookups instead of O(n) list searches
        - **Pre-compute edge structure** once, reuse throughout
        - **Short-circuit validation**: Check both conditions but order them logically
        - **Improvement**: Typical speedup of **3-5x** on large inputs; some inputs may achieve **10x+** speedup with early termination

## Algorithm Comparison

| Aspect | Part One | Part Two Original | Part Two Optimized |
|--------|----------|-------------------|-------------------|
| **Data Structure** | Combinations iterator | Lists of edges | Dictionaries + Lists |
| **Lookup Speed** | N/A | O(n) per lookup | O(1) per lookup |
| **Pair Processing** | All pairs checked | Linear order | Sorted descending by area |
| **Early Termination** | None | None | Yes (area < best) |
| **Memory Usage** | O(1) | O(n) | O(n) |
| **Ray Casting** | N/A | O(n) crossings | O(n) crossings |
| **Typical Speedup** | Baseline | Baseline | 3-5x (up to 10x+) |

## Key Insights
- **Rectilinear Polygon Property**: Edges are axis-aligned, simplifying boundary detection
- **Ray Casting Correctness**: Odd/even crossing rule works for any closed polygon
- **Dictionary Indexing**: O(1) lookup dominates when checking thousands of rectangles
- **Sorted Processing**: Enables early exit when no better solution possible
- **Edge Interior Crossing**: Strictly-inside check (using `<` not `≤`) prevents false positives on boundaries
- **Two-Corner Validation**: Both non-red corners must be valid; suffices due to axis-aligned edges
- **Boundary Aggregation**: Points at exact coordinate match always found first (O(1) dict lookup before O(n) ray casting)

## Solutions
- [`solution.py`](solution.py) - My Solution (python file)
- [`solution_ai.py`](solution_ai.py) - Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
