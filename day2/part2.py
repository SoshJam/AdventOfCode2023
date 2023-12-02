import re

# Starter values
max_red = 12
max_green = 13
max_blue = 14

# Read the input file
input_file = open("day2/input.txt", "r")
data = input_file.readlines()
input_file.close()

# Replace the data to sample data if necessary

sample_data = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""[1:].splitlines(True)

# data = sample_data

# Returns a tuple of any invalid games

results = []

for line in data:
    index = int( line.split(":")[0] .split("Game ")[1] )

    input = line.split(": ")[1]
    handfuls = input.split("; ")

    largest = { "red": 0, "green": 0, "blue": 0 }
    for handful in handfuls:
        picked_colors = handful.split(", ")

        for picked_color in picked_colors:
            for color in ["red", "green", "blue"]:
                if color in picked_color:
                    number = int(picked_color.split(" ")[0])
                    largest[color] = max(number, largest[color])

    power = largest["red"] * largest["green"] * largest["blue"]

    results.append(power)

# Calculate the IDs of the invalid games

# valid_games = [ i+1 for i in range(len(results)) if all(results[i]) ]

print( str(sum(results)) )