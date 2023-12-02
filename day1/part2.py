import re

# Read the main file and convert it into lines
calibration_file = open("day1/input.txt", "r")
calibration = calibration_file.readlines()
calibration_file.close()

# calibration = [ "two1nine", "eightwothree", "abcone2threexyz", "xtwone3four", "4nineeightseven2", "zoneight234", "7pqrstsixteen" ]

# Go through each line and convert the complete words into digits
# We can't just use replace, because "twone" will become 1 instead of 2
def wordsToDigits(line):
    words = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    buffer = ""
    output = line

    continueLoop = True

    # Go through character by character
    charIndex = 0
    while charIndex < len(line):
        if continueLoop:
            buffer = buffer + line[charIndex]
            charIndex += 1
        continueLoop = True

        # Check if the buffer begins a word
        if any([word.startswith(buffer) for word in words]):
            
            # See if it fully matches any words
            matched_words = [word for word in words if word == buffer]

            if len(matched_words) > 0:
                # Replace in the output string
                output = output.replace(buffer, str(words.index(matched_words[0])) + buffer[1:], 1)
                if len(buffer) > 1:
                    buffer = buffer[1:]
                    continueLoop = False
                else:
                    buffer = ""

        else:
            # Does not begin a word, so reset buffer
            # If there is more than one character just remove the first one and try again
            if len(buffer) > 1:
                buffer = buffer[1:]
                continueLoop = False
            else:
                buffer = ""

    return output

calibration_digitified = [ wordsToDigits(line) for line in calibration ]

# Remove everything that's not a digit
calibration_digits = [ re.sub("[^\\d]", "", line) for line in calibration_digitified ]

# Add the first digit to the last digit
calibration_values = [ int( line[0] + line[-1] if len(line) > 0 else "0" ) for line in calibration_digits ]

# Sum up calibration values
calibration_sum = sum(calibration_values)

print(f"The sum is {calibration_sum}")