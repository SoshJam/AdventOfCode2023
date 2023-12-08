# Sam Hill, 2023

# Read the files
sample_file = open("day8/sample.txt")
sample_data = sample_file.read()
sample_file.close()

challenge_file = open("day8/challenge.txt")
challenge_data = challenge_file.read()
challenge_file.close()

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

    # Traverse through the map to the goal
    position = "AAA"
    pattern_index = 0
    while position != "ZZZ":
        # Move to the left or right
        position = map[position][pattern[pattern_index] == "R"]

        # Step through
        steps += 1
        pattern_index += 1
        if pattern_index >= len(pattern):
            pattern_index = 0

    # Return how many steps we took
    return steps
        

# Activate
print(f"SMPL:\t{main(sample_data)}")
print(f"CHLG:\t{main(challenge_data)}")