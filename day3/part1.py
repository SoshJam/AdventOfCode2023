import re

# Read the file
input_file = open("day3/input.txt", "r")
lines = input_file.readlines()
input_file.close()

sample = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""[1:].split("\n")

# lines = sample

# Sum of the part numbers
part_sum = 0

# Loop through the list horizontally and vertically
skips = 0
for y,line in enumerate(lines):
    for x,char in enumerate(line):
        # Skip if necessary
        if skips > 0:
            skips = skips - 1
            continue

        # If this character is not a digit, skip to the next character
        if not char in "0123456789":
            continue

        # If the char is a digit, continue until we get to a char that isn't and that is our length
        length = 1
        while (x + length < len(line) and line[x + length] in "0123456789"):
            length = length + 1

        # Get the current number
        current = int(line[x:x+length])

        # Get the coordinates of our search
        min_x = max(0, x - 1)
        max_x = min(len(line) - 1, x + length + 1)

        # Search the adjacent lines for symbols
        valid = False

        # Search the top line
        if y > 0:
            fragment = lines[y - 1][min_x:max_x]
            if re.search("[^\d\.]", fragment):
                valid = True

        # Search the middle
        if (not valid):
            fragment = lines[y][min_x:max_x]
            if re.search("[^\d\.]", fragment):
                valid = True

        # Search the bottom line
        if (not valid) and y < len(lines) - 1:
            fragment = lines[y + 1][min_x:max_x]
            if re.search("[^\d\.]", fragment):
                valid = True

        if (valid):
            part_sum = part_sum + current

        # Skip the next characters
        skips = length - 1

# Print the answer
print(part_sum)