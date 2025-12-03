import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(ids: list[str]) -> None:
    invalid_ids_sum = 0

    for id in ids:
        range_start, range_end = id.split('-')
        
        # Skip ranges where both bounds have odd length, or start with '0'
        if (len(range_start) % 2 != 0 and len(range_end) % 2 != 0) or range_start[0] == '0':
            continue

        # Adjust the range bounds to the nearest even-length number
        if len(range_start) % 2 != 0:
            range_start = '1' * (len(range_start) + 1)
        if len(range_end) % 2 != 0:
            range_end = '9' * (len(range_end) - 1)
        
        mid = len(range_start) // 2
        rs_start, rs_end, re_start, re_end = range_start[:mid], range_start[mid:], range_end[:mid], range_end[mid:]
        
        # In the starting bound, if first half < second half, increment first half (so repeated version is valid)
        if int(rs_start) < int(rs_end):
            rs_start = str(int(rs_start) + 1)
        
        # Skip if the smallest valid repeated number exceeds range_end
        if int(rs_start * 2) > int(range_end):
            continue
        
        # In the ending bound, if first half > second half, decrement first half (so repeated version is valid)
        if int(re_start) > int(re_end):
            re_start = str(int(re_start) - 1)
        
        invalid_ids_sum += sum(int(str(i) * 2) for i in range(int(rs_start), int(re_start) + 1))

    print("Sum of all the invalid IDs:", invalid_ids_sum)


# Part Two
@timer(name="Part Two")
def Part_Two(ids: list[str]) -> None:
    invalid_ids_sum = 0

    for id in ids:
        range_start, range_end = id.split('-')
        
        # Track numbers already seen_ids to avoid duplicates
        seen_ids = set()
        
        for id_len in range(len(range_start), len(range_end) + 1):
            # Determine the actual range for this length
            range_start_new = max(int(range_start), 10**(id_len - 1))
            range_end_new = min(int(range_end), 10**id_len - 1)
            
            if range_start_new > range_end_new:
                continue
            
            # Try each possible size
            for id_sub_len in range(1, id_len // 2 + 1):
                # Only check if id_sub_len divides id_len evenly
                if id_len % id_sub_len != 0:
                    continue
                
                reps = id_len // id_sub_len
                
                # Generate all possible base patterns
                min_base = 10**(id_sub_len - 1)
                max_base = 10**id_sub_len - 1
                
                for base in range(min_base, max_base + 1):
                    repeated_seq = int(str(base) * reps)
                    
                    # Check if it's in range and not already seen_ids
                    if range_start_new <= repeated_seq <= range_end_new and repeated_seq not in seen_ids:
                        invalid_ids_sum += repeated_seq
                        seen_ids.add(repeated_seq)
                        
                    # Early exit if we've exceeded the range
                    if repeated_seq > range_end_new:
                        break

    print( "Sum of all the invalid IDs (including the additional rule):", invalid_ids_sum)


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=2, force_fetch=False)
    ids = input_data.split(',')

    print("-"*50)
    print("*** Day 2 - Gift Shop ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(ids)
    # Part_Two(ids)    

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, ids)
