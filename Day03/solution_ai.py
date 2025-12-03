import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def best_two_digit_subsequence(bank: str) -> int:
    """
    Pick the lexicographically largest 2-digit subsequence preserving order.
    Uses suffix maximum array for O(n) time complexity.
    Example: '9275' -> '97', '321' -> '32'
    """
    n = len(bank)
    if n == 0:
        return 0
    if n == 1:
        return int(bank)

    # Precompute suffix maximum digit at each position
    suffix_max = [''] * n
    suffix_max[-1] = bank[-1]
    for i in range(n - 2, -1, -1):
        suffix_max[i] = max(bank[i], suffix_max[i + 1])

    # Find the lexicographically largest 2-digit pair
    best = None
    for i in range(n - 1):
        first = bank[i]
        second = suffix_max[i + 1]  # Best digit after position i
        candidate = first + second
        if best is None or candidate > best:
            best = candidate

    # Fallback for edge cases
    if best is None:
        best = bank[-2] + bank[-1]
    return int(best)


def largest_subsequence(bank: str, K: int) -> int:
    """
    Build the lexicographically largest subsequence of length K using a greedy stack.
    Optimized with early exit when no more drops are allowed.
    Time complexity: O(n) where n is the length of bank
    """
    n = len(bank)
    if n <= K:
        return int(bank) if n > 0 else 0

    drops_allowed = n - K
    stack = []
    
    for i, ch in enumerate(bank):
        # Remove smaller digits while we can still drop
        while drops_allowed > 0 and stack and stack[-1] < ch:
            stack.pop()
            drops_allowed -= 1
        
        # Early exit: If no more drops allowed, append remaining string
        if drops_allowed == 0:
            return int("".join(stack) + bank[i:])
        
        stack.append(ch)
    
    # Handle strictly decreasing input: trim to K digits
    return int("".join(stack[:K]))


# Part One: Find the lexicographically largest 2-digit subsequence preserving order
@timer(name="Part One")
def Part_One(banks: list[str]) -> None:
    total_output_joltage_part1 = 0
    for bank in banks:
        total_output_joltage_part1 += best_two_digit_subsequence(bank)

    print(f"Part One - Total Output Joltage: {total_output_joltage_part1}")


# Part Two: Find the lexicographically largest 12-digit subsequence preserving order
@timer(name="Part Two")
def Part_Two(banks: list[str]) -> None:
    no_of_batteries = 12
    total_output_joltage_part2 = sum(largest_subsequence(bank, no_of_batteries) for bank in banks)
    print(f"Part Two - Total Output Joltage (including the additional rule): {total_output_joltage_part2}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=3, force_fetch=False)
    banks = input_data.splitlines()

    print("-"*50)
    print("*** Day 3 - Lobby [AI Version] ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(banks)
    # Part_Two(banks)    

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, banks)
