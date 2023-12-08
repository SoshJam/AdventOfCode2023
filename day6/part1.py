# Sam Hill, 2023

# Read the files
sample_file = open("day6/sample.txt")
sample_lines = sample_file.read().splitlines(False)
sample_file.close()

challenge_file = open("day6/challenge.txt")
challenge_lines = challenge_file.read().splitlines(False)
challenge_file.close()

# Main function
def main(lines: list):
    wins_product = 1 # make sure to start at 1 instead of 0

    # Separate the lines into races
    # a race is a tuple of the allowed time and the max distance
    times = [int(x) for x in lines[0].split(" ")[1:] if x.strip()]
    distances = [int(x) for x in lines[1].split(" ")[1:] if x.strip()]
    races = [(times[i], distances[i]) for i in range(min(len(times), len(distances)))]
    
    # Go through each race and calculate how many ways to win
    for race in races:
        # Get data from the race
        max_time = race[0]
        max_distance = race[1]

        # How many wins we get
        wins = 0

        # Loop through holding time
        for holding_time in range(0, max_time + 1):
            # Calculate the time for the boat to travel
            travel_time = max_time - holding_time

            # Distance = speed * time and speed = holding_time
            distance = holding_time * travel_time

            # Check if we win
            if (distance > max_distance):
                wins += 1

        # Save result
        wins_product = wins_product * wins

    return wins_product

# Activate
print(f"SMPL:\t{main(sample_lines)}")
print(f"CHLG:\t{main(challenge_lines)}")