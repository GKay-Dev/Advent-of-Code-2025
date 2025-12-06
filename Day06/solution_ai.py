import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(worksheet) -> None:
    """
    Solve Part One: Read problems left-to-right horizontally.
    Each column represents one problem with numbers stacked vertically.
    """
    # Pre-split all lines once (avoid repeated splits)
    problems = [line.split() for line in worksheet]
    problem_size = len(problems) - 1  # Number of rows containing operands
    no_of_problems = len(problems[0])  # Number of problems (columns)
    
    grand_total = 0

    # Process each problem column
    for idx in range(no_of_problems):
        # Extract all operands for this problem in one pass
        operands = [int(problems[row][idx]) for row in range(problem_size)]
        operation = problems[-1][idx]

        # Calculate and accumulate result
        grand_total += problem_solution(operands, operation)

    print(f"Part One - Grand total found by adding together all of the answers to the individual problems: {grand_total}")


# Part Two
@timer(name="Part Two")
def Part_Two(worksheet) -> None:
    """
    Solve Part Two: Read problems right-to-left.
    Each vertical column (top-to-bottom) forms a complete number.
    Problems are identified by parsing the operator row structure.
    """
    problem_size = len(worksheet) - 1  # Number of operand rows
    problem_operations = worksheet[-1]  # The operator row as a string
    
    # Parse operator row to identify individual problems by their spacing
    operations = problem_operations[0]
    operations_list = []
    
    # Build list of operator strings (each represents spacing for one problem)
    for char_idx in range(1, len(problem_operations)):
        char = problem_operations[char_idx]
        if char in ['+', '*']:
            # Found next operator, save previous problem's operator section
            operations_list.append(operations[:-1])  # Remove trailing space
            operations = char
        else:
            operations += char
    # Add the last operator section
    operations_list.append(operations[:-1] if operations.endswith(' ') else operations)
    
    no_of_problems = len(operations_list)
    grand_total = 0
    position = 0  # Current position in the line
    
    # Process each problem
    for idx in range(no_of_problems):
        section_width = len(operations_list[idx])
        
        # Last problem may be longer (no trailing space)
        if idx == no_of_problems - 1:
            section_width += 1
        
        next_position = position + section_width
        
        # Extract substring for this problem from each operand row
        problem_sections = [worksheet[row][position:next_position] for row in range(problem_size)]
        operation = operations_list[idx].rstrip()
        
        operands = []
        
        # Read right-to-left through this problem's columns
        for col_offset in range(section_width - 1, -1, -1):
            # Read this column top-to-bottom to form a number
            column_digits = ''
            for section in problem_sections:
                if col_offset < len(section) and section[col_offset].isdigit():
                    column_digits += section[col_offset]
            
            if column_digits:
                operands.append(int(column_digits))
        
        # Move position tracker for next problem
        position = next_position + 1  # +1 for the space separator
        
        # Calculate the answer for this problem
        if operands and operation:
            grand_total += problem_solution(operands, operation)
    
    print(f"Part Two - Grand total found by adding together all of the answers to the individual problems (Numbers are read vertically (top to bottom)): {grand_total}")


def problem_solution(operands, operation):
    """
    Calculate result of applying operation to operands.
    Optimized to use built-in functions where possible.
    
    Args:
        operands: List of numbers
        operation: '+' for sum, '*' for product
    
    Returns:
        Calculated result
    """
    if operation == '+':
        return sum(operands)  # Built-in sum is optimized
    else:  # multiplication
        # Use a single loop instead of manual iteration
        result = 1
        for operand in operands:
            result *= operand
        return result


if __name__ == "__main__":
    # Fetch input from AOC website (cached after first run, or use `save_to_file=False` to never save)
    input_data = get_input(day=6, force_fetch=False)

    # Process input as needed
    worksheet = input_data.splitlines()
    
    print("-"*50)
    print("*** Day 6 - Trash Compactor ***")
    print("-"*50, "\n")

    # Option 1: Time individually
    # Part_One(worksheet)
    # Part_Two(worksheet)

    # Option 2: Time both parts together for cleaner output
    time_both_parts(Part_One, Part_Two, worksheet)