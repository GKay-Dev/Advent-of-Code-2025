from pathlib import Path
from timer_utils import timer
from contextlib import redirect_stdout

@timer(name="All Solutions")
def run_day(day_num: int) -> None:
    """Run both solution files for a given day."""
    day_path = Path(f"Day{day_num:02d}")
    if not day_path.exists():
        return
    
    print(f"\n{'='*60}")
    print(f"Day {day_num}")
    print('='*60)
    
    for solution_file in ["solution.py", "solution_ai.py"]:
        file_path = day_path / solution_file
        if not file_path.exists():
            continue
        
        print(f"\n{solution_file}:")
        
        # Execute the solution file in its own namespace
        with open(file_path, 'r') as f:
            code = compile(f.read(), file_path, 'exec')
        exec(code, {'__name__': '__main__', '__file__': str(file_path)})

        # # Alternatively, using exec directly (less safer and lower performance/security):
        # exec(open(file_path).read(), {'__name__': '__main__', '__file__': str(file_path)})        

@timer(name="Solutions from all days")
def run_all_days(no_of_days: int) -> None:
    """Execute solutions for all days up to no_of_days."""
    for day in range(1, no_of_days + 1):
        run_day(day)


if __name__ == "__main__":
    no_of_days = 12  # Adjust this as needed
    
    with open('AOC_2025_Output.txt', 'w') as f:
        with redirect_stdout(f):
            run_all_days(no_of_days)