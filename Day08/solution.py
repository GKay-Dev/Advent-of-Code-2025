import sys
from pathlib import Path
from itertools import combinations
from collections import Counter

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def euclidean_distance_squared(point1, point2) -> float:
    return ((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2 + (point1[2] - point2[2]) ** 2) ** 0.5


def calculate_all_pairwise_distances(points) -> list[(float, int, int)]:
    n = len(points)
    distances = []
    for i, j in combinations(range(n), 2):
        dist = euclidean_distance_squared(points[i], points[j])
        distances.append((dist, i, j))
    distances.sort()
    return distances


def find(parent, x) -> int:
    if parent[x] != x:
        parent[x] = find(parent, parent[x])  # Path compression
    return parent[x]


def union(parent, rank, x, y) -> bool:
    px, py = find(parent, x), find(parent, y)
    if px == py:
        return False  # Already in same circuit
    
    # Union by rank
    if rank[px] < rank[py]:
        px, py = py, px
    parent[py] = px
    if rank[px] == rank[py]:
        rank[px] += 1
    return True


def get_circuit_sizes(parent, n) -> list[int]:
    roots = [find(parent, i) for i in range(n)]
    return list(Counter(roots).values())


# Part One
@timer(name="Part One")
def Part_One(points) -> None:
    n = len(points)
    distances = calculate_all_pairwise_distances(points)
    
    # Initialize Union-Find
    parent = list(range(n))
    rank = [0] * n
    connections_made = 0
    
    # Process exactly 1000 pairs (not 1000 successful unions)
    for idx in range(1000):
        dist, i, j = distances[idx]
        if union(parent, rank, i, j):
            connections_made += 1
    
    # print(f"Actual new connections made: {connections_made}")

    # Get circuit sizes and find top 3
    sizes = sorted(get_circuit_sizes(parent, n), reverse=True)
    result = sizes[0] * sizes[1] * sizes[2]
    
    # print(f"Number of circuits: {len(sizes)}")
    # print(f"Top circuit sizes: {sizes[:3]}")

    print(f"Part One - Multiply together the sizes of the three largest circuits: {result}")


# Part Two
@timer(name="Part Two")
def Part_Two(points) -> None:
    n = len(points)
    distances = calculate_all_pairwise_distances(points)
    
    # Initialize Union-Find
    parent = list(range(n))
    rank = [0] * n
    circuits_remaining = n  # Start with n individual circuits
    last_i, last_j = None, None
    
    for dist, i, j in distances:
        if union(parent, rank, i, j):
            circuits_remaining -= 1
            last_i, last_j = i, j
            if circuits_remaining == 1:
                # All junction boxes are now in one circuit
                break
    
    # print(f"Last connection: {points[last_i]} <-> {points[last_j]}")

    # Get X coordinates of the last two connected junction boxes
    x1 = points[last_i][0]
    x2 = points[last_j][0]
    result = x1 * x2

    print(f"Part Two - Multiply together the X coordinates of the last two junction boxes you need to connect: {result}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=8, force_fetch=False)

    # Process input as needed
    junc_box_pos = input_data.splitlines()
    points = [tuple(map(int, line.split(","))) for line in junc_box_pos]

    print("-"*50)
    print("*** Day 8 - Playground ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(points)
    # Part_Two(points)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, points)