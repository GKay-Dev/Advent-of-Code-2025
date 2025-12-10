import sys
from pathlib import Path
from itertools import product
from fractions import Fraction

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


def parse_machine(lines):
    """Parse machine line into target state, button configs, and joltage requirements."""
    for line in lines:
        *manual, joltages = line.split()
        target_state, button_configs_str = manual[0][1:-1], manual[1:]
        button_configs = [list(map(int, button[1:-1].split(','))) for button in button_configs_str]
        joltages = list(map(int, joltages[1:-1].split(','))) if joltages else []
        
        yield target_state, button_configs, joltages


# Part One
@timer(name="Part One")
def Part_One(machines) -> None:
    """Find minimum button presses to configure indicator lights using GF(2) Gaussian elimination."""
    total_presses = 0
    
    for target, buttons, _ in parse_machine(machines):
        n_lights = len(target)
        n_buttons = len(buttons)
        
        # Build augmented matrix [A|b] over GF(2)
        matrix = []
        for light_idx in range(n_lights):
            row = [0] * (n_buttons + 1)
            for button_idx, button in enumerate(buttons):
                if light_idx in button:
                    row[button_idx] = 1
            row[n_buttons] = 1 if target[light_idx] == '#' else 0
            matrix.append(row)
        
        # Gaussian elimination to RREF over GF(2)
        pivot_row = 0
        pivot_cols = []
        
        for col in range(n_buttons):
            # Find pivot
            found_pivot = False
            for r in range(pivot_row, n_lights):
                if matrix[r][col] == 1:
                    matrix[pivot_row], matrix[r] = matrix[r], matrix[pivot_row]
                    found_pivot = True
                    break
            
            if not found_pivot:
                continue
            
            # Eliminate column using XOR
            for r in range(n_lights):
                if r != pivot_row and matrix[r][col] == 1:
                    for c in range(n_buttons + 1):
                        matrix[r][c] ^= matrix[pivot_row][c]
            
            pivot_cols.append(col)
            pivot_row += 1
        
        # Check for inconsistency
        inconsistent = any(matrix[r][n_buttons] == 1 for r in range(pivot_row, n_lights))
        if inconsistent:
            total_presses += float('inf')
            continue
        
        # Find free variables and minimize solution
        free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
        min_presses = float('inf')
        
        # Try all combinations of free variables
        for free_vals in product([0, 1], repeat=len(free_cols)):
            solution = [0] * n_buttons
            
            for i, col in enumerate(free_cols):
                solution[col] = free_vals[i]
            
            # Back-substitute pivot variables
            for r in range(len(pivot_cols) - 1, -1, -1):
                pivot_col = pivot_cols[r]
                val = matrix[r][n_buttons]
                for c in range(pivot_col + 1, n_buttons):
                    val ^= (matrix[r][c] * solution[c])
                solution[pivot_col] = val
            
            min_presses = min(min_presses, sum(solution))
        
        total_presses += min_presses

    print(f"Part One - Fewest button presses required to correctly configure the indicator lights on all of the machines : {total_presses}")


# Part Two
@timer(name="Part Two")
def Part_Two(machines) -> None:
    """Find minimum button presses to reach target joltage levels using integer linear programming."""
    total_presses = 0
    
    for _, buttons, joltages in parse_machine(machines):
        n_counters = len(joltages)
        n_buttons = len(buttons)
        
        # Edge case: no buttons
        if n_buttons == 0:
            if all(j == 0 for j in joltages):
                continue
            total_presses += float('inf')
            continue
        
        # Build augmented matrix [A|b] with fractions for exact arithmetic
        matrix = []
        for counter_idx in range(n_counters):
            row = [Fraction(1) if counter_idx in buttons[button_idx] else Fraction(0) 
                   for button_idx in range(n_buttons)]
            row.append(Fraction(joltages[counter_idx]))
            matrix.append(row)
        
        # Gaussian elimination to RREF
        pivot_row = 0
        pivot_cols = []
        col_to_pivot_row = {}
        
        for col in range(n_buttons):
            # Find pivot
            best_row = next((r for r in range(pivot_row, n_counters) if matrix[r][col] != 0), -1)
            if best_row == -1:
                continue
            
            # Swap and scale pivot row
            matrix[pivot_row], matrix[best_row] = matrix[best_row], matrix[pivot_row]
            pivot_val = matrix[pivot_row][col]
            matrix[pivot_row] = [matrix[pivot_row][c] / pivot_val for c in range(n_buttons + 1)]
            
            # Eliminate column in other rows
            for r in range(n_counters):
                if r != pivot_row and matrix[r][col] != 0:
                    factor = matrix[r][col]
                    matrix[r] = [matrix[r][c] - factor * matrix[pivot_row][c] for c in range(n_buttons + 1)]
            
            col_to_pivot_row[col] = pivot_row
            pivot_cols.append(col)
            pivot_row += 1
        
        # Check for inconsistency
        inconsistent = any(matrix[r][n_buttons] != 0 for r in range(pivot_row, n_counters))
        if inconsistent:
            total_presses += float('inf')
            continue
        
        # Build pivot expressions
        free_cols = [c for c in range(n_buttons) if c not in pivot_cols]
        n_free = len(free_cols)
        free_col_to_idx = {fc: i for i, fc in enumerate(free_cols)}
        
        pivot_info = []
        for col in pivot_cols:
            r = col_to_pivot_row[col]
            constant = matrix[r][n_buttons]
            coeffs = [(free_col_to_idx[fc], matrix[r][fc]) for fc in free_cols if matrix[r][fc] != 0]
            pivot_info.append((col, constant, coeffs))
        
        def try_solution(free_vals):
            """Evaluate solution for given free variable values."""
            solution = [0] * n_buttons
            
            for i, fc in enumerate(free_cols):
                solution[fc] = free_vals[i]
            
            for col, constant, coeffs in pivot_info:
                val = constant - sum(coeff * free_vals[idx] for idx, coeff in coeffs)
                
                if val < 0 or val.denominator != 1:
                    return None
                solution[col] = int(val)
            
            return sum(solution)
        
        # Handle unique solution
        if n_free == 0:
            result = try_solution([])
            total_presses += result if result is not None else float('inf')
            continue
        
        # Calculate tight upper bounds for free variables
        upper_bounds = []
        for i in range(n_free):
            ub = max(joltages) if joltages else 0
            
            # Apply constraint-based bounds
            for col, constant, coeffs in pivot_info:
                for idx, coeff in coeffs:
                    if idx == i and coeff > 0 and constant >= 0:
                        # Only restrict if other coeffs aren't negative
                        if not any(c < 0 for j, c in coeffs if j != i):
                            ub = min(ub, int(constant / coeff))
            
            upper_bounds.append(max(0, ub))
        
        # Expand if too restrictive
        for i in range(n_free):
            if upper_bounds[i] == 0:
                upper_bounds[i] = max(joltages) if joltages else 10
        
        # Recursive search with pruning
        min_presses = float('inf')
        
        def search(idx, free_vals, current_sum):
            nonlocal min_presses
            
            if current_sum >= min_presses:
                return
            
            if idx == n_free:
                result = try_solution(free_vals)
                if result is not None:
                    min_presses = min(min_presses, result)
                return
            
            for v in range(upper_bounds[idx] + 1):
                if current_sum + v >= min_presses:
                    break
                free_vals[idx] = v
                search(idx + 1, free_vals, current_sum + v)
        
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