import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(banks: list[str]) -> None:
    total_output_joltage = 0

    for bank in banks:
        # Get unique digits sorted in descending order
        batteries = sorted(set(bank), reverse=True)
        max_bat = batteries[0]
        max_bat_loc = bank.index(max_bat)
        
        # If max digit is at the end, use second largest first
        if max_bat_loc == len(bank) - 1:
            bat2 = max_bat
            bat1 = batteries[1]
        else:
            # Otherwise, use max digit first and find largest digit after it
            bat1 = max_bat
            for battery in batteries:
                if battery in bank[max_bat_loc + 1:]:
                    bat2 = battery
                    break
        
        output_joltage = int(bat1 + bat2)
        total_output_joltage += output_joltage

    print(f"Part One - Total Output Joltage: {total_output_joltage}")


# Part Two
@timer(name="Part Two")
def Part_Two(banks: list[str]) -> None:
    total_output_joltage = 0
    no_of_batteries = 12

    for bank in banks:
        # If bank has 12 or fewer digits, use all of them
        if len(bank) <= no_of_batteries:
            total_output_joltage += int(bank)
            continue

        # Use greedy stack to build largest subsequence
        drops_allowed = len(bank) - no_of_batteries
        stack = []

        for battery in bank:
            # Remove smaller digits while we can still drop and current digit is larger
            while stack and stack[-1] < battery and drops_allowed > 0:
                stack.pop()
                drops_allowed -= 1
            stack.append(battery)

        # Take first 12 digits from the stack
        full_string = "".join(stack)
        output_joltage = int(full_string[:no_of_batteries])
        total_output_joltage += output_joltage

    print(f"Part Two - Total Output Joltage (including the additional rule): {total_output_joltage}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=3, force_fetch=False)
    banks = input_data.splitlines()

    print("-"*50)
    print("*** Day 3 - Lobby ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(banks)
    # Part_Two(banks)    

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, banks)
