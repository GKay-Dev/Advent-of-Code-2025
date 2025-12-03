import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One: Optimized - Direct calculation without string conversion
@timer(name="Part One")
def Part_One(ids: list[str]) -> None:
    invalid_ids_sum = 0

    for id in ids:
        range_start, range_end = id.split('-')
        lo, hi = int(range_start), int(range_end)
        lo_len, hi_len = len(range_start), len(range_end)
        
        # Skip ranges where both bounds have odd length
        if (lo_len % 2 != 0 and hi_len % 2 != 0) or range_start[0] == '0':
            continue

        # Process each even length
        for n_len in range(lo_len + (lo_len % 2), hi_len + 1, 2):
            # Determine the actual range for this length
            range_lo = max(lo, 10**(n_len - 1))
            range_hi = min(hi, 10**n_len - 1)
            
            if range_lo > range_hi:
                continue
            
            # For repeated halves: number = base * (10^half_len + 1)
            half_len = n_len // 2
            multiplier = 10**half_len + 1
            
            # Find base range
            min_base = (range_lo + multiplier - 1) // multiplier  # Ceiling division
            max_base = range_hi // multiplier  # Floor division
            
            if min_base <= max_base:
                # Use arithmetic series sum: sum = n * (first + last) / 2
                # But we need sum of (base * multiplier), so factor out multiplier
                count = max_base - min_base + 1
                sum_bases = count * (min_base + max_base) // 2
                invalid_ids_sum += sum_bases * multiplier

    print("Sum of all the invalid IDs:", invalid_ids_sum)


# Part Two: Optimized - Calculate base range mathematically
@timer(name="Part Two")
def Part_Two(ids: list[str]) -> None:
    invalid_ids_sum = 0

    for id in ids:
        range_start, range_end = id.split('-')
        lo, hi = int(range_start), int(range_end)
        lo_len, hi_len = len(range_start), len(range_end)
        
        # Track numbers already counted to avoid duplicates
        seen_ids = set()
        
        # Process each length in the range
        for n_len in range(lo_len, hi_len + 1):
            # Determine the actual range for this length
            range_lo = max(lo, 10**(n_len - 1))
            range_hi = min(hi, 10**n_len - 1)
            
            if range_lo > range_hi:
                continue
            
            # Try each possible block size (divisor of n_len)
            for block in range(1, n_len // 2 + 1):
                # Only check if block divides n_len evenly
                if n_len % block != 0:
                    continue
                
                reps = n_len // block
                
                # Calculate multiplier for repeated pattern
                # For block=2, reps=3: 121212 = 12 * 10101 = 12 * (10^4 + 10^2 + 1)
                multiplier = sum(10**(block * i) for i in range(reps))
                
                # Find base range
                min_base = max(10**(block - 1), (range_lo + multiplier - 1) // multiplier)
                max_base = min(10**block - 1, range_hi // multiplier)
                
                # Add valid repeated numbers
                for base in range(min_base, max_base + 1):
                    repeated_num = base * multiplier
                    
                    # Verify in range and not duplicate
                    if range_lo <= repeated_num <= range_hi and repeated_num not in seen_ids:
                        invalid_ids_sum += repeated_num
                        seen_ids.add(repeated_num)
                    elif repeated_num > range_hi:
                        break

    print("Sum of all the invalid IDs (including the additional rule):", invalid_ids_sum)


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=2, force_fetch=False)
    ids = input_data.split(',')

    print("-"*50)
    print("*** Day 2 - Gift Shop [AI Version] ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(ids)
    # Part_Two(ids)    

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, ids)
