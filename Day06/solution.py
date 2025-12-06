import sys
from pathlib import Path

# Add parent directory to path to import utility modules
sys.path.insert(0, str(Path(__file__).parent.parent))

from timer_utils import timer, time_both_parts
from aoc_utils import get_input


# Part One
@timer(name="Part One")
def Part_One(worksheet) -> None:
    grand_total = 0
    problems = [line.split() for line in worksheet]
    problem_size = len(problems) - 1  # Number of rows containing operands
    no_of_problems = len(problems[0])  # Number of columns (problems)

    # Process each problem column
    for idx in range(no_of_problems):
        problem_operands = [int(problems[idy][idx]) for idy in range(problem_size)]
        problem_operation = problems[-1][idx]

        problem_answer = problem_solution(problem_operands, problem_operation)
        grand_total += problem_answer

    print(f"Part One - Grand total found by adding together all of the answers to the individual problems : {grand_total}")


# Part Two
@timer(name="Part Two")
def Part_Two(problems) -> None:
    grand_total = 0
    problem_size = len(problems) - 1  # Number of rows containing operands
    problem_operations = problems[-1]  # The operator row
    
    # Parse the operator row to identify individual problems
    operations = problem_operations[0]
    operations_list = []

    # Build list of operator strings (each represents spacing for one problem)
    for op in problem_operations[1:]:
        if op in ['+', '*']:
            operations_list.append(operations[:-1])  # Remove trailing space between columns
            operations = op
            continue
        operations += ' '
    operations_list.append(operations[:-1])

    no_of_problems = len(operations_list)
    old_number_size = 0  # Track position in the line

    # Process each problem
    for idx in range(no_of_problems):
        number_size = len(operations_list[idx])
        
        # Last problem may be longer (no trailing space for next column)
        if idx == no_of_problems - 1:
            number_size += 1
        
        new_number_size = old_number_size + number_size

        # Extract the substring for this problem from each operand row
        problem_operands = [problems[idy][old_number_size:new_number_size] for idy in range(problem_size)]
        problem_operation = operations_list[idx]
        
        new_operand = ''
        new_problem_operands = []

        # Read right-to-left through columns
        while number_size > 0:
            number_size -= 1
            
            # Read each column top-to-bottom to form a number
            for operand in problem_operands:
                new_operand += operand[number_size - 1]

            # Convert accumulated digits to integer
            operand_value = int(new_operand.strip())
            new_problem_operands.append(operand_value)
            new_operand = ''
        
        # Move position tracker for next problem
        old_number_size += len(operations_list[idx]) + 1

        problem_answer = problem_solution(new_problem_operands, problem_operation.rstrip())
        
        grand_total += problem_answer

    print(f"Part Two - Grand total found by adding together all of the answers to the individual problems (Numbers are read vertically (top to bottom)): {grand_total}")


def problem_solution(operands, operation):
    if operation == '+':
        return sum(operands)
    else:
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