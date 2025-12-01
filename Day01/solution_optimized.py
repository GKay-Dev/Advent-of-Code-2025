from pathlib import Path

input_path = Path(__file__).parent / "input.txt"

with open(input_path, "r") as file:
    rotation = [line.strip() for line in file]


# Part One
ptr = 50
ctr = sum(1 for r in rotation if (ptr := (ptr - int(r[1:]) if r[0] == 'L' else ptr + int(r[1:])) % 100) == 0)

print("Actual Password to open the door:", ctr)


# Part Two
ptr = 50
ctr = 0

for r in rotation:
    direction, distance = r[0], int(r[1:])
    
    if direction == 'L':
        ctr += abs((ptr - distance) // 100) - (ptr == 0)
        ptr = (ptr - distance) % 100
        ctr += (ptr == 0)
    else:
        ctr += (ptr + distance) // 100
        ptr = (ptr + distance) % 100

print("Using password method 0x434C49434B, Password to open the door:", ctr)