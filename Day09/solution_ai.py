import sys
from pathlib import Path
from itertools import combinations

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(red_tiles) -> None:
    largest_area = 0

    # For each pair of red tiles, calculate the area of the rectangle they form.
    for i, j in combinations(range(len(red_tiles)), 2):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        area = (abs(x1 - x2) + 1) * (abs(y1 - y2) + 1)

        # Update largest area if needed
        if area > largest_area:
            largest_area = area

    print(f"Part One - Largest area of any rectangle you can make : {largest_area}")


# Part Two
@timer(name="Part Two")
def Part_Two(red_tiles) -> None:
    n = len(red_tiles)
    
    # Build edge segments
    edges = []
    for i in range(n):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[(i + 1) % n]
        edges.append(((x1, y1), (x2, y2)))
    
    # Separate horizontal and vertical edges with better indexing
    h_edges = []  # (y, x_min, x_max)
    v_edges = []  # (x, y_min, y_max)
    h_edges_by_y = {}  # Quick lookup for horizontal edges by y coordinate
    v_edges_by_x = {}  # Quick lookup for vertical edges by x coordinate
    
    for (x1, y1), (x2, y2) in edges:
        if y1 == y2:
            edge = (y1, min(x1, x2), max(x1, x2))
            h_edges.append(edge)
            h_edges_by_y[y1] = edge
        else:
            edge = (x1, min(y1, y2), max(y1, y2))
            v_edges.append(edge)
            v_edges_by_x[x1] = edge
    
    def rect_intersects_edge(min_rx, max_rx, min_ry, max_ry):
        """Check if any edge crosses through the interior of the rectangle."""
        # Check vertical edges that cross horizontally through rectangle interior
        for x, ymin, ymax in v_edges:
            if min_rx < x < max_rx and ymin < max_ry and ymax > min_ry:
                return True
        
        # Check horizontal edges that cross vertically through rectangle interior
        for y, xmin, xmax in h_edges:
            if min_ry < y < max_ry and xmin < max_rx and xmax > min_rx:
                return True
        
        return False
    
    def on_boundary(px, py):
        """Check if point is on polygon boundary using quick lookups."""
        # Check horizontal edges
        if py in h_edges_by_y:
            y, xmin, xmax = h_edges_by_y[py]
            if xmin <= px <= xmax:
                return True
        
        # Check vertical edges
        if px in v_edges_by_x:
            x, ymin, ymax = v_edges_by_x[px]
            if ymin <= py <= ymax:
                return True
        
        return False
    
    def point_in_polygon(px, py):
        """Ray casting algorithm - optimized for vertical edges only."""
        crossings = 0
        for (x1, y1), (x2, y2) in edges:
            if y1 == y2:  # Skip horizontal edges
                continue
            
            y_min, y_max = min(y1, y2), max(y1, y2)
            if y_min <= py < y_max:
                # Linear interpolation to find x intersection
                t = (py - y1) / (y2 - y1)
                x_intersect = x1 + t * (x2 - x1)
                if x_intersect > px:
                    crossings += 1
        
        return crossings % 2 == 1
    
    def is_valid_point(px, py):
        """Check if point is inside or on boundary of polygon."""
        return on_boundary(px, py) or point_in_polygon(px, py)
    
    # Sort red tiles by area to check larger rectangles first (early termination potential)
    tile_pairs = list(combinations(range(n), 2))
    tile_pairs.sort(
        key=lambda pair: (abs(red_tiles[pair[0]][0] - red_tiles[pair[1]][0]) + 1) * 
                         (abs(red_tiles[pair[0]][1] - red_tiles[pair[1]][1]) + 1),
        reverse=True
    )
    
    largest_area = 0
    for i, j in tile_pairs:
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        
        min_rx, max_rx = min(x1, x2), max(x1, x2)
        min_ry, max_ry = min(y1, y2), max(y1, y2)
        
        area = (max_rx - min_rx + 1) * (max_ry - min_ry + 1)
        
        # Early termination: if this area is smaller than current best, skip all remaining
        if area < largest_area:
            break
        
        # Quick check: both red corner points must be in red_tiles (they are by definition)
        # Check the other two corners are valid
        corner1 = (min_rx, max_ry)
        corner2 = (max_rx, min_ry)
        
        if not (is_valid_point(*corner1) and is_valid_point(*corner2)):
            continue
        
        # Check no edge crosses through the rectangle interior
        if rect_intersects_edge(min_rx, max_rx, min_ry, max_ry):
            continue
        
        largest_area = area
    
    print(f"Part Two - Largest area of any rectangle you can make using only red and green tiles : {largest_area}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=9, force_fetch=False)

    # Process input as needed
    red_tiles_location = input_data.splitlines()
    red_tiles = [(int(loc.split(",")[0]), int(loc.split(",")[1])) for loc in red_tiles_location]

    print("-"*50)
    print("*** Day 9 - Movie Theater ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(red_tiles)
    # Part_Two(red_tiles)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, red_tiles)