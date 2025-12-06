import requests
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def get_session_token():
    """Get AOC session token from environment variable."""
    token = os.getenv("AOC_SESSION")
    if not token:
        raise ValueError("AOC_SESSION not found in environment variables. Create a .env file with AOC_SESSION=your_token")
    
    return token


def fetch_input(year, day):
    """Fetch input from Advent of Code website."""
    url = f"https://adventofcode.com/{year}/day/{day}/input"
    session_token = get_session_token()
    
    headers = {"Cookie": f"session={session_token}"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Failed to fetch input: {response.status_code}")
    
    return response.text


def get_input(day, force_fetch=False, save_to_file=True):
    """
    Get input for a specific day. Uses cached file if available, otherwise fetches from web.
    
    Args:
        year: Year of the puzzle
        day: Day of the puzzle
        force_fetch: If True, always fetch from web even if cached file exists
        save_to_file: If True, saves fetched input to file for caching
    
    Returns:
        List of strings (lines from input)
    """
    # Determine the directory for this day's solution
    day_dir = Path(__file__).parent / f"Day{day:02d}"
    input_file = day_dir / "input.txt"
    
    # Check if we can use cached file
    if not force_fetch and input_file.is_file():
        with open(input_file, "r") as f:
            return f.read()
    
    # Fetch from web
    print(f"Fetching input for Day {day}...")
    year = os.getenv("AOC_YEAR", str(datetime.now().year))  # Default to current year if not set
    input_data = fetch_input(year, day)
    
    # Optionally save to file
    if save_to_file:
        day_dir.mkdir(exist_ok=True)
        with open(input_file, "w") as f:
            f.write(input_data)
        print(f"Input saved to {input_file}")
    
    # Return the retrieved input
    return input_data
    