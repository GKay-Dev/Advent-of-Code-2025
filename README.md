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
  ├── solution.py               # Solution (python file)
  ├── solution_optimized.py     # Refactored & optimized solution for efficiency & performance
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
AOC_YEAR=event_year  # AOC event year (events run from 2015 onwards)
```

**Important**: Never commit your `.env` file! It's already included in `.gitignore`.
Navigate to a specific day's folder and run the solution
### 6. Run Solutions
Navigate to a specific day's folder and run the solution
```bash
cd DayXX            # Replace XX with day number (01-12)
python solution.py  # Or python3 solution.py
```

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

### Utility Function
```python
get_input(day, force_fetch=False, save_to_file=True)
```
- Handles fetching and caching puzzle inputs
- Automatically creates day directories if needed
- Returns input as a list of stripped strings

### Modular Design
- `aoc_utils.py` contains reusable utilities for all days
- Each solution file is self-contained and can run independently
- Environment variables are loaded automatically via `python-dotenv`

## Progress
| Day    | Part 1 | Part 2 |
|:---    |  :---: |  :---: |
| Day 1  | ✅     | ✅     |
| Day 2  | ❌     | ❌     |
| Day 3  | ❌     | ❌     |
| Day 4  | ❌     | ❌     |
| Day 5  | ❌     | ❌     |
| Day 6  | ❌     | ❌     |
| Day 7  | ❌     | ❌     |
| Day 8  | ❌     | ❌     |
| Day 9  | ❌     | ❌     |
| Day 10 | ❌     | ❌     |
| Day 11 | ❌     | ❌     |
| Day 12 | ❌     | ❌     |

## Feedback
Suggestions? Reach out via [GitHub Issues](https://github.com/GKay-dev/advent-of-code-2025/issues).
