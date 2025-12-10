import sys
from pathlib import Path
from itertools import product
from fractions import Fraction

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def parse_machine(lines):
    # Parse a machine line into target state, button configs, and joltage requirements
    for line in lines:
        *manual, joltages = line.split()
        target_state, button_configs_str = manual[0][1:-1], manual[1:]
        button_configs = [list(map(int, button[1:-1].split(','))) for button in button_configs_str]
        joltages = list(map(int, joltages[1:-1].split(','))) if joltages else []

        yield target_state, button_configs, joltages


# Part One
@timer(name="Part One")
def Part_One(machines) -> None:
    total_presses = 0
    
    for target, buttons, _ in parse_machine(machines):
        n_lights = len(target)
        n_buttons = len(buttons)
        
        # Build augmented matrix for system of linear equations over GF(2)
        # Each row represents a light equation, columns represent buttons
        # Last column is the target state (1 if light should be on, 0 if off)
        matrix = []
        for light_idx in range(n_lights):
            row = [0] * (n_buttons + 1)
            for button_idx, button in enumerate(buttons):
                if light_idx in button:
                    row[button_idx] = 1  # This button affects this light
            row[n_buttons] = 1 if target[light_idx] == '#' else 0  # Target state
            matrix.append(row)
        
        # Gaussian elimination to reduced row echelon form over GF(2)
        pivot_row = 0
        pivot_cols = []  # Track which columns have pivots (determined variables)
        
        for col in range(n_buttons):
            # Find a pivot (non-zero entry) in current column
            found_pivot = False
            for r in range(pivot_row, n_lights):
                if matrix[r][col] == 1:
                    # Swap rows to bring pivot to current pivot_row
                    matrix[pivot_row], matrix[r] = matrix[r], matrix[pivot_row]
                    found_pivot = True
                    break
            
            if not found_pivot:
                continue  # This column has no pivot - it's a free variable
            
            # Eliminate all other 1s in this column using XOR
            for r in range(n_lights):
                if r != pivot_row and matrix[r][col] == 1:
                    for c in range(n_buttons + 1):
                        matrix[r][c] ^= matrix[pivot_row][c]  # XOR operation in GF(2)
            
            pivot_cols.append(col)
            pivot_row += 1
        
        # Check for inconsistency (0 = 1, which means no solution)
        inconsistent = False
        for r in range(pivot_row, n_lights):
            if matrix[r][n_buttons] == 1:
                inconsistent = True
                break
        
        if inconsistent:
            total_presses += float('inf')
            continue  # Skip to next machine
        
        # Free variables are columns without pivots
        free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
        min_presses = float('inf')
        
        # Try all combinations of free variables (0 or 1 for each)
        for free_vals in product([0, 1], repeat=len(free_cols)):
            solution = [0] * n_buttons
            
            # Set free variables to current combination
            for i, col in enumerate(free_cols):
                solution[col] = free_vals[i]
            
            # Back-substitute to find pivot variables
            for r in range(len(pivot_cols) - 1, -1, -1):
                pivot_col = pivot_cols[r]
                val = matrix[r][n_buttons]
                # XOR with contributions from other variables
                for c in range(pivot_col + 1, n_buttons):
                    val ^= (matrix[r][c] * solution[c])
                solution[pivot_col] = val
            
            # Track minimum total button presses
            min_presses = min(min_presses, sum(solution))
        
        total_presses += min_presses

    print(f"Part One - Fewest button presses required to correctly configure the indicator lights on all of the machines : {total_presses}")


# Part Two
@timer(name="Part Two")
def Part_Two(machines) -> None:
    total_presses = 0
    
    for _, buttons, joltages in parse_machine(machines):
        n_counters = len(joltages)
        n_buttons = len(buttons)
        
        # Handle edge case
        if n_buttons == 0:
            if all(j == 0 for j in joltages):
                # No buttons needed, all joltages are 0
                continue
            else:
                # Impossible to reach non-zero joltages with no buttons
                total_presses += float('inf')
                continue
        
        # Build augmented matrix A|b where:
        # A[counter][button] = 1 if button affects counter, 0 otherwise
        # b[counter] = target joltage for that counter
        matrix = []
        for counter_idx in range(n_counters):
            row = []
            for button_idx in range(n_buttons):
                if counter_idx in buttons[button_idx]:
                    row.append(Fraction(1))  # Use Fraction for exact arithmetic
                else:
                    row.append(Fraction(0))
            row.append(Fraction(joltages[counter_idx]))  # Target value
            matrix.append(row)
        
        # Gaussian elimination to reduced row echelon form (RREF)
        pivot_row = 0
        pivot_cols = []
        col_to_pivot_row = {}  # Map pivot column to its row
        
        for col in range(n_buttons):
            # Find non-zero entry in this column
            best_row = -1
            for r in range(pivot_row, n_counters):
                if matrix[r][col] != 0:
                    best_row = r
                    break
            
            if best_row == -1:
                continue  # No pivot in this column - free variable
            
            # Swap rows to bring pivot to current position
            matrix[pivot_row], matrix[best_row] = matrix[best_row], matrix[pivot_row]
            
            # Scale pivot row so pivot element becomes 1
            pivot_val = matrix[pivot_row][col]
            for c in range(n_buttons + 1):
                matrix[pivot_row][c] /= pivot_val
            
            # Eliminate this column in all other rows
            for r in range(n_counters):
                if r != pivot_row and matrix[r][col] != 0:
                    factor = matrix[r][col]
                    for c in range(n_buttons + 1):
                        matrix[r][c] -= factor * matrix[pivot_row][c]
            
            col_to_pivot_row[col] = pivot_row
            pivot_cols.append(col)
            pivot_row += 1
        
        # Check for inconsistency (no solution exists)
        inconsistent = False
        for r in range(pivot_row, n_counters):
            if matrix[r][n_buttons] != 0:
                inconsistent = True
                break
        
        if inconsistent:
            total_presses += float('inf')
            continue  # Skip to next machine
        
        # Identify free variables (columns without pivots)
        free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
        n_free = len(free_cols)
        
        # Map each free column to its index in the free_cols list
        free_col_to_idx = {fc: i for i, fc in enumerate(free_cols)}
        
        # Build expressions for pivot variables in terms of free variables
        # After RREF: pivot_var = constant - sum(coeff * free_var)
        pivot_info = []
        for col in pivot_cols:
            r = col_to_pivot_row[col]
            constant = matrix[r][n_buttons]
            coeffs = []  # List of (free_var_index, coefficient) tuples
            for fc in free_cols:
                if matrix[r][fc] != 0:
                    coeffs.append((free_col_to_idx[fc], matrix[r][fc]))
            pivot_info.append((col, constant, coeffs))
        
        def try_solution(free_vals):
            # Compute solution given free variable values, return total or None if invalid
            solution = [0] * n_buttons
            
            # Set free variables to given values
            for i, fc in enumerate(free_cols):
                solution[fc] = free_vals[i]
            
            # Compute pivot variables from free variables
            for col, constant, coeffs in pivot_info:
                val = constant
                for free_idx, coeff in coeffs:
                    val -= coeff * free_vals[free_idx]
                
                # Check if result is a non-negative integer
                if val < 0 or val.denominator != 1:
                    return None
                solution[col] = int(val)
            
            return sum(solution)
        
        # Special case: no free variables means unique solution
        if n_free == 0:
            result = try_solution([])
            if result is not None:
                total_presses += result
            else:
                total_presses += float('inf')
            continue  # Move to next machine
        
        # Calculate upper bounds for each free variable
        # This dramatically reduces the search space
        upper_bounds = []
        for i, fc in enumerate(free_cols):
            ub = max(joltages) if joltages else 0  # Start with max joltage as bound
            
            # Tighten bounds based on constraints
            # For pivot = constant - coeff * free:
            # If coeff > 0, then free <= constant / coeff (for pivot >= 0)
            for col, constant, coeffs in pivot_info:
                for free_idx, coeff in coeffs:
                    if free_idx == i and coeff > 0:
                        # Only apply bound if no other free vars can compensate
                        has_negative_coeff = any(c < 0 for _, c in coeffs if _ != i)
                        if not has_negative_coeff:
                            max_val = int(constant / coeff) if constant >= 0 else 0
                            ub = min(ub, max_val)
            
            upper_bounds.append(max(0, ub))
        
        # Expand bounds if they're too restrictive
        for i in range(n_free):
            if upper_bounds[i] == 0:
                upper_bounds[i] = max(joltages) if joltages else 10
        
        min_presses = float('inf')
        
        def search(idx, free_vals, current_free_sum):
            # Recursive search through free variable space with pruning and explore all valid combinations to find minimum total button presses
            nonlocal min_presses
            
            # Prune: if current sum already exceeds best found, stop
            if current_free_sum >= min_presses:
                return
            
            # Base case: all free variables assigned
            if idx == n_free:
                result = try_solution(free_vals)
                if result is not None:
                    min_presses = min(min_presses, result)
                return
            
            # Try each possible value for current free variable
            for v in range(upper_bounds[idx] + 1):
                # Prune: if adding this value exceeds best, stop trying larger values
                if current_free_sum + v >= min_presses:
                    break
                free_vals[idx] = v
                search(idx + 1, free_vals, current_free_sum + v)
        
        # Start recursive search
        search(0, [0] * n_free, 0)
        
        total_presses += min_presses

    print(f"Part Two - Fewest button presses required to correctly configure the joltage level counters on all of the machines: {total_presses}")


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=10, force_fetch=False)

    # Process input as needed
    machines = input_data.splitlines()

    print("-"*50)
    print("*** Day 10 - Factory ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(machines)
    # Part_Two(machines)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, machines)