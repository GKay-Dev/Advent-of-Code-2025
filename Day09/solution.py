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
    
    # Separate horizontal and vertical edges
    h_edges = []  # (y, x_min, x_max)
    v_edges = []  # (x, y_min, y_max)
    for (x1, y1), (x2, y2) in edges:
        if y1 == y2:
            h_edges.append((y1, min(x1, x2), max(x1, x2)))
        else:
            v_edges.append((x1, min(y1, y2), max(y1, y2)))
    
    def rect_intersects_edge(min_rx, max_rx, min_ry, max_ry):
        # Check vertical edges that cross horizontally through rectangle interior
        for x, ymin, ymax in v_edges:
            if min_rx < x < max_rx:  # Edge x is strictly inside rectangle's x range
                # Check if edge's y range overlaps with rectangle's y range
                if ymin < max_ry and ymax > min_ry:
                    return True
        
        # Check horizontal edges that cross vertically through rectangle interior
        for y, xmin, xmax in h_edges:
            if min_ry < y < max_ry:  # Edge y is strictly inside rectangle's y range
                # Check if edge's x range overlaps with rectangle's x range
                if xmin < max_rx and xmax > min_rx:
                    return True
        
        return False
    
    def on_boundary(px, py):
        # Check if point is on polygon boundary
        for y, xmin, xmax in h_edges:
            if py == y and xmin <= px <= xmax:
                return True
        for x, ymin, ymax in v_edges:
            if px == x and ymin <= py <= ymax:
                return True
        return False
    
    def point_in_polygon(px, py):
        # Ray casting algorithm to check if point is inside polygon
        crossings = 0
        for (x1, y1), (x2, y2) in edges:
            if y1 == y2:  # Horizontal edge, skip
                continue
            if min(y1, y2) <= py < max(y1, y2):
                t = (py - y1) / (y2 - y1)
                x_intersect = x1 + t * (x2 - x1)
                if x_intersect > px:
                    crossings += 1
        return crossings % 2 == 1
    
    def is_valid_point(px, py):
        # Check if point is inside or on boundary of polygon
        return on_boundary(px, py) or point_in_polygon(px, py)
    
    # For each pair of red tiles, check if rectangle is valid
    largest_area = 0
    for i, j in combinations(range(n), 2):
        x1, y1 = red_tiles[i]
        x2, y2 = red_tiles[j]
        
        min_rx, max_rx = min(x1, x2), max(x1, x2)
        min_ry, max_ry = min(y1, y2), max(y1, y2)
        
        area = (max_rx - min_rx + 1) * (max_ry - min_ry + 1)
        if area <= largest_area:
            continue
        
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