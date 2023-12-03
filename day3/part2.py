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

# Sum of the gear ratios
gear_sum = 0

nums = "0123456789"

# Loop through the list horizontally and vertically
for y,line in enumerate(lines):
    for x,char in enumerate(line):

        # If this character is not a * symbol, skip to the next character
        if char != "*":
            continue

        # If the char is a * symbol, find all the part numbers next to it
        directions = [ (-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1) ]
        part_number_coords = []
        blacklist_top = False # if we find a part number at (-1, -1), then (-1, 0) MUST be a . in order for (-1, 1) to be a separate part number
        blacklist_bottom = False

        for d in directions:
            # If this is out of bounds, continue
            if (x + d[0] < 0) or (x + d[0] >= len(line)) or (y + d[1] < 0) or (y + d[1] >= len(lines)):
                continue

            content = lines[ y + d[1] ][ x + d[0] ]

            # If this is the top or bottom left, check if we should continue with the middle
            if d == (-1, -1):
                blacklist_top = content in nums

            elif d == (-1, 1):
                blacklist_bottom = content in nums

            # If this is the top or bottom, check if we should bother with the next one
            elif d == (0, -1):
                if blacklist_top:
                    blacklist_top = content in nums
                    continue
                else:
                    blacklist_top = content in nums

            elif d == (0, 1):
                if blacklist_bottom:
                    blacklist_bottom = content in nums
                    continue
                else:
                    blacklist_bottom = content in nums

            # If this is the top or bottom right, check if we should just stop
            elif d == (1, -1):
                if blacklist_top:
                    continue

            elif d == (1, 1):
                if blacklist_bottom:
                    continue

            # If we didn't continue, we should check this cell
            if content in nums:
                part_number_coords.append(d)

        # If there aren't exactly two part numbers, quit
        if len(part_number_coords) != 2:
            continue

        # Start at all the part number coords, and get all the part numbers
        part_numbers = []
        for c in part_number_coords:
            num_y = c[1] + y

            start_x = c[0] + x
            while start_x > 0 and lines[num_y][start_x - 1] in nums:
                start_x = start_x - 1

            end_x = c[0] + x
            while end_x < len(line) - 1 and lines[num_y][end_x + 1] in nums:
                end_x = end_x + 1

            part_numbers.append(int(lines[num_y][start_x:end_x + 1]))

        # Find the gear ratio
        gear_ratio = part_numbers[0] * part_numbers[1]

        gear_sum = gear_sum + gear_ratio

# Print the answer
print(gear_sum)