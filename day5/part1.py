# Sam Hill, 2023

sample = """
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
"""[1:].splitlines(False)

# Read the file
input_file = open("day5/input.txt")
input_lines = input_file.read().splitlines(False) 
input_file.close()

# Replace with sample if necessary
# input_lines = sample

### SETUP

# First, get the seeds
seed_numbers = [int(s) for s in input_lines[0].split(" ")[1:]]

# Now loop through and load all of these maps into a data structure
# Structure:
# maps: [
#   [
#     (
#        destination,
#        source,
#        range
#     ),
#   ],
# ]

maps = []

input_mode = False # if true we are adding things to the map, otherwise we are waiting for the next section to start
current_range = 0

for line in input_lines[1:]:
    # If we aren't in input mode, check if we should switch, otherwise skip
    if not input_mode:
        # We switch when the line contains "map:"
        if "map:" in line:
            input_mode = True
            maps.append([])
        continue
    
    # If we are in input mode
    else:
        # If this line is empty, we are out of input mode
        if len(line) == 0:
            input_mode = False
            current_range += 1
            continue

        # Otherwise, split this range into integers and add to the maps
        numbers = [int(i) for i in line.split(" ")]
        maps[current_range].append( ( numbers[0], numbers[1], numbers[2] ) )

### APPLICATION FUNCTION

# For a given number, searches through the maps to find its numbers
def search_maps(number):
    # The different data points for the number, which is what will be returned
    points = [number]

    # Loop through each map
    current_number = number # The number at a given point in the loop
    for map in maps:

        # Loop through ranges in the map
        for range in map:
            # Extract data from map
            destination_start = range[0]
            source_start = range[1]
            range_length = range[2]

            # Check if the number falls into this range
            if current_number >= source_start and current_number < source_start + range_length:
                # Calculate the offset and apply the transformation
                offset = current_number - source_start
                current_number = destination_start + offset

                # The transformation is only applied once per map so stop looping
                break

        # Add this number after transformation to the return data
        points.append(current_number)

    return points

# Apply this to each item
map_results = [search_maps(seed) for seed in seed_numbers]

# Get the location numbers of each seed
location_numbers = [r[-1] for r in map_results]

# Print the puzzle result
print(min(location_numbers))