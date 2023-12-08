# Sam Hill, 2023

import math

# Read the files
sample_file = open("day6/sample.txt")
sample_lines = sample_file.read().splitlines(False)
sample_file.close()

challenge_file = open("day6/challenge.txt")
challenge_lines = challenge_file.read().splitlines(False)
challenge_file.close()

# Main function
def main(lines: list):
    # Get the time and distance allowed for the race
    time_string = ""
    for char in lines[0]:
        if char in "0123456789":
            time_string += char
    max_time = int(time_string)
    
    dist_string = ""
    for char in lines[1]:
        if char in "0123456789":
            dist_string += char
    max_distance = int(dist_string)

    # Bounds for when our distance is greater than the record
    lower_bound = math.ceil((-max_time + math.sqrt((max_time ** 2) - (4 * max_distance))) / (-2))
    upper_bound = math.floor((-max_time - math.sqrt((max_time ** 2) - (4 * max_distance))) / (-2))

    # Result
    ways_to_win = upper_bound - lower_bound + 1
    return ways_to_win

# Activate
print(f"SMPL:\t{main(sample_lines)}")
print(f"CHLG:\t{main(challenge_lines)}")