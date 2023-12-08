# Sam Hill, 2023

import math
from enum import Enum

# Game setup
cards = "J23456789TQKA"

# Types of hands
class HandType(Enum):
    FIVE_OF_A_KIND = 7
    FOUR_OF_A_KIND = 6
    FULL_HOUSE = 5
    THREE_OF_A_KIND = 4
    TWO_PAIR = 3
    ONE_PAIR = 2
    HIGH_CARD = 1
    NONE = 0

# Helper Methods

# Returns 1 if a > b, -1 if a < b, 0 if a = b
def compare(a: int, b: int):
    if a > b:
        return 1
    elif a < b:
        return -1
    return 0

# Returns 1 if card 1 wins, -1 if card 2 wins, 0 if tied
def compare_cards(card1: str, card2: str):
    return compare(cards.index(card1[0]), cards.index(card2[0]))

# Returns the type of the hand
def get_hand_type(hand: str):
    # Get the count of each card
    card_counts = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    joker_count = 0
    for card in hand:
        if card != "J":
            card_counts[cards.index(card)] += 1
        else:
            joker_count += 1
    
    # Sort the counts, it doesn't matter which card has which count
    card_counts = sorted(card_counts, reverse=True)

    # Return the hand type based on the card counts
    if card_counts[0] + joker_count == 5:
        return HandType.FIVE_OF_A_KIND
    if card_counts[0] + joker_count == 4:
        return HandType.FOUR_OF_A_KIND
    if card_counts[0] + joker_count == 3 and card_counts[1] == 2:
        return HandType.FULL_HOUSE
    if card_counts[0] + joker_count == 3 and card_counts[1] == 1:
        return HandType.THREE_OF_A_KIND
    if card_counts[0] + joker_count == 2 and card_counts[1] == 2:
        return HandType.TWO_PAIR
    if card_counts[0] + joker_count == 2 and card_counts[1] == 1:
        return HandType.ONE_PAIR
    if card_counts[0] + joker_count == 1:
        return HandType.HIGH_CARD
    
    # not sure if this can happen but whatever
    return HandType.NONE

# Returns 1 if hand 1 is higher ranking than hand 2, etc.
def compare_hands(hand1: str, hand2: str):
    # Check the hand types
    hand1_type = get_hand_type(hand1)
    hand2_type = get_hand_type(hand2)
    type_comparison = compare(hand1_type.value, hand2_type.value)

    # Return the winner unless they have the same rank
    if type_comparison != 0:
        return type_comparison
    
    # Otherwise go through the cards in each hand one by one
    for i in range(5):
        card_comparison = compare_cards(hand1[i], hand2[i])

        if card_comparison != 0:
            return card_comparison
        
    # if the hands are equal just return 0
    return 0

# Converts a hand to an int based on the type and value of cards.
# e.g. AAAAA = 71414141414
#      23332 = 50203030302
def hand_to_int(hand: str):
    sum = 0

    # Hand type
    sum += get_hand_type(hand).value * 10000000000

    # Cards
    sum += (cards.index(hand[0]) + 1) * 100000000
    sum += (cards.index(hand[1]) + 1) * 1000000
    sum += (cards.index(hand[2]) + 1) * 10000
    sum += (cards.index(hand[3]) + 1) * 100
    sum += (cards.index(hand[4]) + 1) * 1

    return sum

# Read the files
sample_file = open("day7/sample.txt")
sample_lines = sample_file.read().splitlines(False)
sample_file.close()

challenge_file = open("day7/challenge.txt")
challenge_lines = challenge_file.read().splitlines(False)
challenge_file.close()

# Main Function
def main(inputs: list):
    # Separate into tuples of hands and bids
    players = [(i.split(" ")[0], int(i.split(" ")[1])) for i in inputs]

    # Sort the list based on which cards win
    players_sorted = sorted(players, key=lambda player: hand_to_int(player[0]))

    # Target
    total_winnings = 0

    # Loop through the players with their bids and add up the winnings
    for index,player in enumerate(players_sorted):
        total_winnings += player[1] * (index + 1)

    return total_winnings

# Activate
print(f"SMPL:\t{main(sample_lines)}")
print(f"CHLG:\t{main(challenge_lines)}")