# Sam Hill, 2023

import numpy as np

# Read the files
sample_file = open("day8/sample.txt")
sample_data = sample_file.read()
sample_file.close()

challenge_file = open("day8/challenge.txt")
challenge_data = challenge_file.read()
challenge_file.close()

# Helper Methods

# Returns the amount of steps from a starting position to an ending position
def step_count(map: dict, pattern: str, start: str):
    steps = 0

    position = start
    pattern_index = 0
    
    while position[2] != "Z":
        # Move to the left or right
        position = map[position][pattern[pattern_index] == "R"]

        # Step through
        steps += 1
        pattern_index += 1
        if pattern_index >= len(pattern):
            pattern_index = 0

    return steps

# Main Method
def main(data: str):
    # Split into lines
    lines = data.splitlines(False)

    # Goal
    steps = 0

    # The pattern we must follow
    pattern = lines[0]

    # Dictionary of directions
    # { "AAA": (BBB, CCC), }
    map = {}

    # Go through the rest of the lines and build the map
    for line in lines[2:]:
        map[line[0:3]] = ( line[7:10], line[12:15] )

    # Get all the starting positions
    start_positions = [pos for pos in map if pos[2] == "A"]

    # Get the step counts for each starting position
    step_counts = [step_count(map, pattern, pos) for pos in start_positions]

    # Get the least common multiple of the step counts, this is how many steps
    # we must do for all of the branches to get to the end
    steps = np.lcm.reduce(step_counts, dtype=object)

    # Return how many steps we took
    return steps

# Activate
print(f"SMPL:\t{main(sample_data)}")
print(f"CHLG:\t{main(challenge_data)}")