# Sam Hill, 2023

# Goal
card_totals = []

# Open the file
input_file = open("day4/input.txt", "r")
input_lines = input_file.readlines()
input_file.close()

# Overwrite with sample if needed
sample = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""[1:].splitlines(False)

# input_lines = sample

# Ensure the card_totals is full of 1s because we start with 1 copy
# of each card
for line in input_lines:
    card_totals.append(1)

# Process the file
for index,line in enumerate(input_lines):
    data = line.split(":")[1].split("|")
    winning_numbers = [int(x) for x in data[0].split(" ") if len(x) > 0]
    card_numbers = [int(x) for x in data[1].split(" ") if len(x) > 0]

    matches = 0

    # Count matches if necessary
    for num in card_numbers:
        if num in winning_numbers:
            matches += 1

    copies = card_totals[index]

    # Add more scratch cards based on how many copies of this card
    # we have and how many matches we got
    for i in range(matches):
        card_totals[index + i + 1] += copies

print(sum(card_totals))