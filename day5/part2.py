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

# First, get the ranges of the seeds
seed_ranges = []
seed_range_string = input_lines[0].split(" ")[1:]
for i in range(0, len(seed_range_string), 2):
    range_start = int(seed_range_string[i])
    range_length = int(seed_range_string[i+1])
    seed_ranges.append( (range_start, range_length) )

# Returns True if the input number is in any of these ranges
def inSeedRange(number):
    for r in seed_ranges:
        if number >= r[0] and number < r[0] + r[1]:
            return True
    return False

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

### APPLICATION

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

# This first method uses brute force. I really, really tried to avoid it, but I could
# not figure it out to save my life.

def brute_force():
    lowest_location = -1
    index_seed_number = 0

    # Loop through the seed ranges
    print("Range_________\tStart_________\tStop__________\tLength________")
    for index,seed_range in enumerate(seed_ranges):
        r_start = seed_range[0]
        r_stop = seed_range[0] + seed_range[1]
        r_len = seed_range[1]
        print(f"{index}\t\t{r_start}\t{r_stop}\t{r_len}")

        # Loop through all of the seeds in this range
        for seed_number in range(r_start, r_stop):
            # Get the location number
            location_number = search_maps(seed_number)[-1]

            # Check if we should overwrite this
            if lowest_location == -1 or location_number < lowest_location:
                lowest_location = location_number
                index_seed_number = seed_number

    # Print our final answer
    print("=====")
    print(f"Min Location:\t{lowest_location}\t<=== ANSWER")
    print(f"Seed Number:\t{index_seed_number}")

# Approach two: Loop back and see if the interval 0 to N maps to anything
# Doesn't rely on brute force but does kind of rely on luck. If we get unlucky,
# this can probably be extended to the right solution anyway.

def zero_slice_method():
    # Find the slice of the locations that maps A to 0,
    # Find the slice of the humidity that maps B to A, trimming if necessary
    # Repeat until we get to the seed numbers, and hope to God there is some overlap.
    start_point = 0
    start_range = -1

    for map_index in range(len(maps) - 1, -1, -1):
        map = maps[map_index]

        # If we found an interval that we are included in
        found_interval = False
        min_interval_distance = -1

        # Loop through the intervals and find one that includes our start point
        for interval in map:
            int_dest = interval[0]
            int_src = interval[1]
            int_len = interval[2]

            # Check if our start point is in this interval's destination range
            if start_point >= int_dest and start_point < int_dest + int_len:
                found_interval = True

                # Calculate the offset from the interval destination point
                offset = start_point - int_dest

                # Set our new start point
                start_point = int_src + offset

                # If the length hasn't been set, calculate that
                if start_range == -1:
                    start_range = int_len - offset

                # Otherwise, the new range is the minimum of it and the distance
                # from the start point to the end of this interval
                else:
                    start_range = min(start_range, int_len - offset)

                # We can only be in one interval, so now we break
                break

            # If we are not in this interval, see if we should use it to manage the range
            else:
                # Calculate the distance to this interval
                distance = int_dest - start_point

                # Distance must be positive, otherwise either we're in the interval
                # or it's completely behind us.
                if distance > 0:
                    # Set our minimum distance (if it's -1 it's our first look)
                    min_interval_distance = min(min_interval_distance, distance) if min_interval_distance != -1 else distance

        # If we did not fit into any interval, then we must set our distance to ensure it doesn't
        # reach the start of the next interval
        if not found_interval:
            start_range = (min(start_range, min_interval_distance) if start_range != -1 else min_interval_distance) if min_interval_distance != -1 else start_range

    print("==============")

    print(f"Valid Seeds Range Start:\t{start_point}")
    print(f"Valid Seeds Range Length:\t{start_range}")

    # Now that we know the range of valid seeds for the zero slice method, we must see if there are
    # any seeds in this interval
    # 1. Loop through the seed ranges and find the smallest distance from our start point
    # 2. If this distance is larger than our interval, there are no valid seeds from this method
    # 3. Otherwise, the distance to the seed interval will be our lowest valid location number

    min_seed_distance = -1

    for seed_range in seed_ranges:
        int_start = seed_range[0]
        int_stop = seed_range[0] + seed_range[1]
        int_len = seed_range[1]

        distance = int_start - start_point
        if distance < 0:
            continue

        min_seed_distance = min(distance, min_seed_distance) if min_seed_distance != -1 else distance

    print(f"Minumum Actual Seed Distance:\t{min_seed_distance}")

    if min_seed_distance > start_range or min_seed_distance == -1:
        print(f"There are no valid seeds here.")
    
    else:
        print(f"Minumum Seed Location Number:\t{min_seed_distance}")

# zero_slice_method()

# Attempt 3 - Slice Method
# Attempts to recreate the zero-slice method, but able to start from any interval

# Returns a tuple of the smallest interval and the distance found

def slice_method(original_start_point):
    # Find the slice of the locations that maps A to start_point,
    # Find the slice of the humidity that maps B to A, trimming if necessary
    # Repeat until we get to the seed numbers, and hope to God there is some overlap.
    start_point = original_start_point
    start_range = -1

    if start_point == 46:
        print("",end="")

    for map_index in range(len(maps) - 1, -1, -1):
        map = maps[map_index]

        # If we found an interval that we are included in
        found_interval = False
        min_interval_distance = -1

        # Loop through the intervals and find one that includes our start point
        for interval in map:
            int_dest = interval[0]
            int_src = interval[1]
            int_len = interval[2]

            # Check if our start point is in this interval's destination range
            if start_point >= int_dest and start_point < int_dest + int_len:
                found_interval = True

                # Calculate the offset from the interval destination point
                offset = start_point - int_dest

                # Set our new start point
                start_point = int_src + offset

                # If the length hasn't been set, calculate that
                if start_range == -1:
                    start_range = int_len - offset

                # Otherwise, the new range is the minimum of it and the distance
                # from the start point to the end of this interval
                else:
                    start_range = min(start_range, int_len - offset)

                # We can only be in one interval, so now we break
                break

            # If we are not in this interval, see if we should use it to manage the range
            else:
                # Calculate the distance to this interval
                distance = int_dest - start_point

                # Distance must be positive, otherwise either we're in the interval
                # or it's completely behind us.
                if distance > 0:
                    # Set our minimum distance (if it's -1 it's our first look)
                    min_interval_distance = min(min_interval_distance, distance) if min_interval_distance != -1 else distance

        # If we did not fit into any interval, then we must set our distance to ensure it doesn't
        # reach the start of the next interval
        if not found_interval:
            start_range = (min(start_range, min_interval_distance) if start_range != -1 else min_interval_distance) if min_interval_distance != -1 else start_range

    # Now that we know the range of valid seeds for the zero slice method, we must see if there are
    # any seeds in this interval
    # 1. Loop through the seed ranges and find the smallest distance from our start point
    # 1. Loop through the seed ranges and see if we are in any intervals
    # 2. Also track the smallest distances from our start point
    # 3. If we are in an interval, return immediately with an offset of 0
    # 4. Otherwise, use our distance to the next seed interval to see if anything later on fits
    # 5. If this distance is larger than our interval, there are no valid seeds from this method
    # 6. Otherwise, the distance to the seed interval will be our lowest valid location number

    min_seed_distance = -1

    for seed_range in seed_ranges:
        int_start = seed_range[0]
        int_stop = seed_range[0] + seed_range[1]
        int_len = seed_range[1]

        # See if we are in this interval
        if start_point >= int_start and start_point < int_stop:
            # Immediately return with our results
            return (start_point, start_range, 0, True)

        # Calculate distance to next interval
        distance = int_start - start_point
        if distance < 0:
            continue

        min_seed_distance = min(distance, min_seed_distance) if min_seed_distance != -1 else distance

    success = not (min_seed_distance > start_range or min_seed_distance == -1)

    # Return the info so that we can try again
    return (start_point, start_range, min_seed_distance, success)

start_point = 0
lowest_location = -1
valid_seed = -1
success = False

# Repeat until we find the result
while success == False:
    # Prepare
    print(f"Start\t{start_point}\t",end="")

    # Get the results
    results = slice_method(start_point)
    success = results[3]

    # Output the results
    print(f"Smallest Interval\t{results[1]}\t",end="")
    print(f"Potential Seed Start Point\t{results[0]}\t",end="")
    print(f"Minimum Next Seed Distance\t{results[2]}\t",end="")
    print(f"Successful\t{results[3]}\t",end="")
    print("")

    if results[3]:
        lowest_location = start_point + results[2]
        valid_seed = results[0] + results[2]
    
    # Prepare for the next call
    start_point = start_point + results[1]

print(f"Lowest Valid Seed Location: {lowest_location}")
print(f"Lowest Valid Seed Nubmer:   {valid_seed}")