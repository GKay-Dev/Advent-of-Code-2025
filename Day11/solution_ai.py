import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One: count paths without storing them
@timer(name="Part One")
def Part_One(device_paths) -> None:
    source = 'you'
    target = 'out'
    visited = set()

    def dfs(node):
        if node == target:
            return 1  # found a path
        total = 0
        for nxt in device_paths.get(node, []):
            if nxt not in visited:           # avoid cycles
                visited.add(nxt)
                total += dfs(nxt)
                visited.remove(nxt)
        return total

    visited.add(source)
    count = dfs(source)
    print(f"Part One - Number of different paths leading from 'you' to 'out' : {count}")


# Part Two: bitmask + memo for required devices
@timer(name="Part Two")
def Part_Two(device_paths) -> None:
    source = 'svr'
    target = 'out'
    required_devices = ('dac', 'fft')          # stable order for bits
    req_index = {dev: i for i, dev in enumerate(required_devices)}
    FULL_MASK = (1 << len(required_devices)) - 1
    memo = {}

    def dfs(node, mask):
        key = (node, mask)
        if key in memo:
            return memo[key]
        if node == target:
            return 1 if mask == FULL_MASK else 0

        # Add current node to mask if it is required
        if node in req_index:
            mask |= 1 << req_index[node]

        total = 0
        for nxt in device_paths.get(node, []):
            total += dfs(nxt, mask)

        memo[key] = total
        return total

    count = dfs(source, 0)
    print(f"Part Two - Number of different paths that lead from 'svr' to 'out', that visit both 'dac' and 'fft' : {count}")


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