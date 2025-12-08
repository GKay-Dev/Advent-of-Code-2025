import sys
from pathlib import Path
from itertools import combinations

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def euclidean_distance_sq(a, b) -> int:
    """Return squared Euclidean distance between 3D points a and b."""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def calculate_all_pairwise_distances(points):
    """Compute sorted list of (dist_sq, i, j) for all unique point pairs."""
    n = len(points)
    dist = []
    append = dist.append  # local binding for speed
    for i, j in combinations(range(n), 2):
        append((euclidean_distance_sq(points[i], points[j]), i, j))
    dist.sort(key=lambda x: x[0])
    return dist


class UnionFind:
    """Disjoint Set Union with path compression and union by rank."""
    __slots__ = ("parent", "rank")

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        """Return representative of set containing x (with path compression)."""
        parent = self.parent
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(self, x, y):
        """Union sets of x and y; return True if merged, False if already one."""
        px, py = self.find(x), self.find(y)
        if px == py:
            return False
        rank = self.rank
        if rank[px] < rank[py]:
            px, py = py, px
        self.parent[py] = px
        if rank[px] == rank[py]:
            rank[px] += 1
        return True

    def circuit_sizes(self):
        """Yield sizes of all disjoint sets."""
        from collections import Counter
        roots = [self.find(i) for i in range(len(self.parent))]
        return Counter(roots).values()


# Part One
@timer(name="Part One")
def Part_One(points) -> None:
    """Connect the 1000 closest pairs and return product of 3 largest circuits."""
    n = len(points)
    dists = calculate_all_pairwise_distances(points)

    uf = UnionFind(n)
    limit = min(1000, len(dists))
    for idx in range(limit):
        _, i, j = dists[idx]
        uf.union(i, j)

    sizes = sorted(uf.circuit_sizes(), reverse=True)
    result = sizes[0] * sizes[1] * sizes[2]
    
    print(f"Part One - Multiply together the sizes of the three largest circuits: {result}")


# Part Two
@timer(name="Part Two")
def Part_Two(points) -> None:
    """Connect pairs shortest-first until all in one circuit; multiply last X coords."""
    n = len(points)
    dists = calculate_all_pairwise_distances(points)

    uf = UnionFind(n)
    circuits = n
    last_i = last_j = None

    for _, i, j in dists:
        if uf.union(i, j):
            circuits -= 1
            last_i, last_j = i, j
            if circuits == 1:
                break

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