import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(device_paths) -> None:
    source = 'you'
    target = 'out'
    all_paths = []        # Collect all valid paths for counting
    visited = set()       # Track nodes currently on the recursion stack to prevent cycles

    def DFS(v, path):
        if v == target:
            all_paths.append(path.copy())
            return

        for neighbor in device_paths.get(v, []):
            if neighbor not in visited:
                visited.add(neighbor)
                DFS(neighbor, path + [neighbor])
                visited.remove(neighbor)

    visited.add(source)
    DFS(source, [source])

    print(f"Part One - Number of different paths leading from 'you' to 'out' : {len(all_paths)}")


# Part Two
@timer(name="Part Two")
def Part_Two(device_paths) -> None:
    source = 'svr'
    target = 'out'
    required_devices = {'dac', 'fft'}
    memo = {}  # Memoize (node, seen_required) -> count

    def dfs(node, seen):
        key = (node, seen)
        if key in memo:
            return memo[key]
        if node == target:
            return 1 if seen == required_devices else 0

        # If current node is required, add it to the seen set (kept immutable for hashing)
        new_seen = seen | {node} if node in required_devices else seen

        total = 0
        for nxt in device_paths.get(node, []):
            total += dfs(nxt, new_seen)

        memo[key] = total
        return total

    count_paths_with_required_devices = dfs(source, frozenset())

    print(f"Part Two - Number of different paths that lead from 'svr' to 'out', that visit both 'dac' and 'fft' : {count_paths_with_required_devices}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=11, force_fetch=False)

    # Process input as needed
    device_to_outputs = input_data.splitlines()
    device_paths = {line.split(":")[0]: line.split(":")[1].strip().split(" ") for line in device_to_outputs}

    print("-"*50)
    print("*** Day 11 - Reactor ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(device_paths)
    # Part_Two(device_paths)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, device_paths)