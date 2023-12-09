# Sam Hill, 2023

# Read the files
sample_file = open("day9/sample.txt")
sample_data = sample_file.read()
sample_file.close()

challenge_file = open("day9/challenge.txt")
challenge_data = challenge_file.read()
challenge_file.close()

# Main Method
def main(data: str):
    # Goal
    extrapolated_sum = 0

    # Data is on each line
    for line in data.splitlines(False):

        # Separate into ints
        start = [int(x) for x in line.split(" ")]
        layers = [start]
        
        # Loop until we get a line of all zeroes
        while any(layers[-1]):

            # Get the diff between numbers
            differences = []
            for i in range(len(layers[-1]) - 1):
                differences.append(layers[-1][i + 1] - layers[-1][i])

            # Add it to the list
            layers.append(differences)

        # Add a 0 to the last layer
        layers[-1].insert(0, 0)

        # Loop backward through the layers, skipping the top layer
        for i in range(len(layers) - 1, 0, -1):
            # Subtract the first number of the this layer from the first number of the last layer
            next_number = layers[i-1][0] - layers[i][0]

            # Put it in the above layer
            layers[i-1].insert(0, next_number)

        # The first number of the first layer is our extrapolated value
        extrapolated_sum += layers[0][0]

    return extrapolated_sum

# Activate
print(f"SMPL:\t{main(sample_data)}")
print(f"CHLG:\t{main(challenge_data)}")