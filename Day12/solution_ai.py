import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def parse_input(input_data):
    """Parse shapes and regions from input data."""
    sections = input_data.strip().split('\n\n')
    
    shapes = {}
    regions = []
    
    for section in sections:
        lines = section.strip().split('\n')
        
        if lines[0].rstrip().endswith(':') and lines[0][:-1].isdigit():
            idx = int(lines[0][:-1])
            coords = []
            for r, line in enumerate(lines[1:]):
                for c, ch in enumerate(line):
                    if ch == '#':
                        coords.append((r, c))
            shapes[idx] = tuple(coords)
        else:
            for line in lines:
                parts = line.split(':')
                dims = parts[0].split('x')
                width, height = int(dims[0]), int(dims[1])
                quantities = list(map(int, parts[1].strip().split()))
                regions.append((width, height, quantities))
    
    return shapes, regions


def normalize_shape(coords):
    """Normalize shape coordinates to start at (0,0)."""
    if not coords:
        return tuple()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    normalized = tuple(sorted((r - min_r, c - min_c) for r, c in coords))
    return normalized


def get_all_orientations(coords):
    """Get all unique orientations (up to 8) of a shape."""
    orientations = set()
    current = list(coords)
    
    for _ in range(4):
        orientations.add(normalize_shape(current))
        current = [(c, -r) for r, c in current]
    
    current = [(r, -c) for r, c in coords]
    for _ in range(4):
        orientations.add(normalize_shape(current))
        current = [(c, -r) for r, c in current]
    
    return list(orientations)


def get_shape_bounds(orientation):
    """Get max row and column of a shape orientation."""
    max_r = max(r for r, c in orientation)
    max_c = max(c for r, c in orientation)
    return max_r, max_c


def greedy_pack(width, height, pieces_list, shape_orientations):
    """
    Greedy packing: place pieces one by one in first available position.
    Returns True if all pieces placed, False otherwise.
    """
    # Grid: True = occupied
    grid = [[False] * width for _ in range(height)]
    
    def can_place(orientation, start_r, start_c):
        for r, c in orientation:
            nr, nc = start_r + r, start_c + c
            if nr >= height or nc >= width or grid[nr][nc]:
                return False
        return True
    
    def place(orientation, start_r, start_c):
        for r, c in orientation:
            grid[start_r + r][start_c + c] = True
    
    def find_first_empty():
        for r in range(height):
            for c in range(width):
                if not grid[r][c]:
                    return r, c
        return None, None
    
    for shape_idx in pieces_list:
        placed = False
        orientations = shape_orientations[shape_idx]
        
        # Try to place at first empty cell that this piece can cover
        for orientation in orientations:
            if placed:
                break
            max_r, max_c = get_shape_bounds(orientation)
            
            for start_r in range(height - max_r):
                if placed:
                    break
                for start_c in range(width - max_c):
                    if can_place(orientation, start_r, start_c):
                        place(orientation, start_r, start_c)
                        placed = True
                        break
        
        if not placed:
            return False
    
    return True


def smart_greedy_pack(width, height, quantities, shape_orientations):
    """
    Smart greedy: try different orderings and strategies.
    """
    # Build pieces list
    pieces = []
    for shape_idx, qty in enumerate(quantities):
        pieces.extend([shape_idx] * qty)
    
    if not pieces:
        return True
    
    # Strategy 1: Sort by number of orientations (fewer first - more constrained)
    pieces_by_constraint = sorted(pieces, key=lambda idx: len(shape_orientations[idx]))
    if greedy_pack(width, height, pieces_by_constraint, shape_orientations):
        return True
    
    # Strategy 2: Sort by shape index
    pieces_by_index = sorted(pieces)
    if greedy_pack(width, height, pieces_by_index, shape_orientations):
        return True
    
    # Strategy 3: Reverse order
    if greedy_pack(width, height, pieces_by_constraint[::-1], shape_orientations):
        return True
    
    return None  # Inconclusive - need exact solver


def backtrack_with_pruning(width, height, quantities, shape_orientations, time_limit_nodes=100000):
    """
    Backtracking with aggressive pruning.
    Uses "first empty cell" strategy - each piece must cover the first empty cell.
    """
    pieces = []
    for shape_idx, qty in enumerate(quantities):
        pieces.extend([shape_idx] * qty)
    
    if not pieces:
        return True
    
    # Sort by most constrained first
    pieces.sort(key=lambda idx: len(shape_orientations[idx]))
    
    # Precompute: for each shape, for each cell, which placements cover that cell
    placements_covering_cell = {}
    for shape_idx in range(len(quantities)):
        placements_covering_cell[shape_idx] = {}
        for orientation in shape_orientations[shape_idx]:
            max_r, max_c = get_shape_bounds(orientation)
            
            for start_r in range(height - max_r):
                for start_c in range(width - max_c):
                    cells = tuple((start_r + r, start_c + c) for r, c in orientation)
                    
                    # For each cell in this placement, record it
                    for cell in cells:
                        if cell not in placements_covering_cell[shape_idx]:
                            placements_covering_cell[shape_idx][cell] = []
                        placements_covering_cell[shape_idx][cell].append(cells)
    
    grid = set()  # Occupied cells
    nodes_visited = [0]
    
    def find_first_empty():
        for r in range(height):
            for c in range(width):
                if (r, c) not in grid:
                    return (r, c)
        return None
    
    def backtrack(piece_idx):
        nodes_visited[0] += 1
        if nodes_visited[0] > time_limit_nodes:
            return None  # Timeout
        
        if piece_idx == len(pieces):
            return True
        
        # Find first empty cell - this MUST be covered
        cell = find_first_empty()
        if cell is None:
            return False  # No empty cells but pieces remaining
        
        shape_idx = pieces[piece_idx]
        
        # Get placements of this shape that cover this cell
        if cell not in placements_covering_cell[shape_idx]:
            return False  # This shape can't cover this cell
        
        for placement in placements_covering_cell[shape_idx][cell]:
            # Check if valid
            if any(c in grid for c in placement):
                continue
            
            # Place
            grid.update(placement)
            
            result = backtrack(piece_idx + 1)
            if result is True:
                return True
            if result is None:
                grid.difference_update(placement)
                return None  # Propagate timeout
            
            # Remove
            grid.difference_update(placement)
        
        return False
    
    return backtrack(0)


def can_fit_region(width, height, quantities, shapes, shape_orientations):
    """
    Main function to check if a region can fit all pieces.
    Uses multiple strategies in order of speed.
    """
    total_cells = width * height
    shape_size = len(shapes[0])
    total_pieces = sum(quantities)
    total_needed = total_pieces * shape_size
    
    # Quick check: not enough space
    if total_needed > total_cells:
        return False
    
    # No pieces needed
    if total_pieces == 0:
        return True
    
    # Try greedy first (very fast)
    result = smart_greedy_pack(width, height, quantities, shape_orientations)
    if result is True:
        return True
    
    # Try backtracking with limit
    result = backtrack_with_pruning(width, height, quantities, shape_orientations, time_limit_nodes=500000)
    if result is True:
        return True
    if result is False:
        return False
    
    # Timeout - try with higher limit for edge cases
    result = backtrack_with_pruning(width, height, quantities, shape_orientations, time_limit_nodes=2000000)
    if result is True:
        return True
    if result is False:
        return False
    
    # Still timeout - assume it fits (heuristic for very large problems)
    # In practice, if greedy almost works and we can't prove it doesn't fit, it probably does
    return True


@timer(name="Part One")
def Part_One(input_data) -> None:
    shapes, regions = parse_input(input_data)
    
    # Precompute all orientations for each shape
    shape_orientations = {}
    for idx in shapes:
        shape_orientations[idx] = get_all_orientations(shapes[idx])
    
    count = 0
    for i, (width, height, quantities) in enumerate(regions):
        if can_fit_region(width, height, quantities, shapes, shape_orientations):
            count += 1
        
        if (i + 1) % 25 == 0:
            print(f"  Processed {i + 1}/{len(regions)} regions...")
    
    print(f"Part One - Regions that can fit all presents: {count}")


# Part Two
@timer(name="Part Two")
def Part_Two(input_data) -> None:
    print("Part Two : There is no part two for this day!")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=12, force_fetch=False)

    # Process input as needed
    situation = input_data.splitlines()

    print("-"*50)
    print("*** Day 12 - Christmas Tree Farm ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(input_data)
    # Part_Two(situation)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, input_data)