# Advent of Code 2025 🎄

Welcome to my **Advent of Code 2025** journey! This repository contains my solutions to the daily coding challenges from [Advent of Code](https://adventofcode.com), an annual event where programming and problem-solving meet the holiday spirit.

## About Advent of Code
Advent of Code is a series of daily programming puzzles released every December leading up to Christmas. Each puzzle offers a fun challenge, a chance to learn, and an opportunity to showcase problem-solving skills.

## Structure  
Each day's solutions are organized into individual directories:
```graphql
📂 DayXX/
  ├── DayXX_<ProblemTitle>.md   # Problem solving approach
  ├── input.txt                 # Puzzle input (cached from AOC website after first run)
  ├── solution.py               # My Solution (python file)
  ├── solution_ai.py            # Vibe coded using AI to refactor & optimize my solution (Sometimes not so optimized)
```

## Technologies Used
- **Programming Language**: Python 3.x
- **Libraries**: 
  - `requests` - For fetching puzzle inputs from adventofcode.com
  - `python-dotenv` - For managing environment variables securely
  - `pathlib` - For cross-platform file path handling

## Setup Instructions

### 1. Clone the repository:
   ```bash
   git clone https://github.com/GKay-dev/Advent-Of-Code-2025.git
   cd Advent-Of-Code-2025
   ```

### 2. Create and Activate Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install requests python-dotenv
```

### 4. Get Your Session Token
1. Log in to [Advent of Code](https://adventofcode.com)
2. Open browser DevTools (F12)
3. Go to **Application** → **Cookies** → `https://adventofcode.com`
4. Copy the value of the `session` cookie

### 5. Configure Environment Variables
Create a `.env` file in the repository root:
```bash
AOC_SESSION=your_session_token_here
AOC_YEAR=event_year  # AOC event year (event is happening since 2015)
```

**Important**: Never commit your `.env` file! It's already included in `.gitignore`.

### 6. Run Solutions

#### Run Individual Day Solutions
Navigate to a specific day's folder and run the solution:
```bash
cd DayXX                # Replace XX with day number (01-12)

python solution.py
# or
python solution_ai.py
```

#### Run All Solutions at Once
Execute all completed day solutions from the repository root:
```bash
python run_all.py
```

This will:
- Run both `solution.py` and `solution_ai.py` for each completed day
- Display timing information for each solution
- Save all output to `AOC_2025_Output.txt`
- Configure the number of days to run by modifying `no_of_days` variable in `run_all.py`

On first run, the script will automatically:
- Fetch your puzzle input from adventofcode.com
- Cache it to `input.txt` for subsequent runs

## Technical Details

### Input Handling System
- **Automated Fetching**: The `aoc_utils.py` module automatically fetches puzzle inputs using your session token
- **Smart Caching**: Inputs are cached locally to `input.txt` to avoid unnecessary web requests
- **Flexible Options**:
  - `get_input(day=1)` - Uses cache if available, otherwise fetches and saves
  - `get_input(day=1, force_fetch=True)` - Always fetches from web, overwrites cache
  - `get_input(day=1, save_to_file=False)` - Fetches but never saves to file

### Timer Utility
- **Performance Monitoring**: The `timer_utils.py` module provides decorators for timing function execution
- **Usage**:
  ```python
  @timer(name="Part One")
  def Part_One(input_data):
      # Your solution code
      pass
  
  # Time both parts together for cleaner output
  time_both_parts(Part_One, Part_Two, input_data)
  ```

### Utility Functions
**`aoc_utils.py`**:
```python
get_input(day, force_fetch=False, save_to_file=True)
```
- Handles fetching and caching puzzle inputs
- Automatically creates day directories if needed
- Returns input as string

**`timer_utils.py`**:
```python
@timer(name="Timer Name")             # Decorator for timing individual functions (Timer name optional)
time_both_parts(func1, func2, *args)  # Time two functions with same arguments
```

**`run_all.py`**:
```python
run_day(day_num)          # Execute both solution files for a specific day
run_all_days(no_of_days)  # Execute solutions for all days up to no_of_days
```
- Automatically discovers and runs all solution files in each day's directory
- Captures and redirects output to `AOC_2025_Output.txt`
- Provides timing information for individual days and overall execution

### Modular Design
- `aoc_utils.py` contains reusable utilities for fetching inputs
- `timer_utils.py` provides performance measurement tools
- `run_all.py` orchestrates execution of all day solutions
- Each solution file is self-contained and can run independently
- Environment variables are loaded automatically via `python-dotenv`

### Solution Variants
- **`solution.py`**: Original solution approach (No usage of AI in any manner)
- **`solution_ai.py`**: AI-optimized version with improved algorithms and performance enhancements (Sometimes, not so optimized)

## Progress
| Day                                          | Part 1 | Part 2 |
|:-------------------------------------------- | :----: | :----: |
| [Day 1](Day01/Day01_Historian_Hysteria.md)   | ✅     | ✅     |
| [Day 2](Day02/Day02_Red_Nosed_Reports.md)    | ✅     | ✅     |
| [Day 3](Day03/Day03_Lobby.md)                | ✅     | ✅     |
| Day 4                                        | ❌     | ❌     |
| Day 5                                        | ❌     | ❌     |
| Day 6                                        | ❌     | ❌     |
| Day 7                                        | ❌     | ❌     |
| Day 8                                        | ❌     | ❌     |
| Day 9                                        | ❌     | ❌     |
| Day 10                                       | ❌     | ❌     |
| Day 11                                       | ❌     | ❌     |
| Day 12                                       | ❌     | ❌     |

## Feedback
Suggestions? Reach out via [GitHub Issues](https://github.com/GKay-dev/advent-of-code-2025/issues).
