import re

# Read the input file
calibration_file = open("1-1/input.txt", "r")
calibration = calibration_file.readlines()
calibration_file.close()

# Turn lines into just lines of digits
digits = [ re.sub("[^\\d]", "", line) for line in calibration ]

# Turn lines of digits into calibration values
calibration_values = [ int( line[0] + line[-1] if len(line) > 0 else "0" ) for line in digits ]

# Sum up calibration values
calibration_sum = sum(calibration_values)

print(f"The sum is {calibration_sum}")