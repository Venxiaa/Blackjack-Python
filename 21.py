#this was made to practice defining statements
#some very outdated code im not changing cause lazy

import random

#------Lists and values------
card_values = {
    "A": 11,  # Can also be 1
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

suits = [
"Hearts",
"Spades",
"Diamonds",
"Clubs",
]

available_cards = []
player_hand = []
dealer_hand = []

#------Deck System------
for types in suits:
    for ranks in card_values:
        available_cards.append(ranks + " of " + types)
random.shuffle(available_cards)

#------Dealing System------
def draw_card(hand):
    hand.append(available_cards.pop(0))
for i in range(2):
    draw_card(player_hand)
    draw_card(dealer_hand)

#------Hand Calculator------
def calculate_hand(hand):
    hand_total = 0
    ace_count = 0
    for cards in hand:
        hand_total += card_values[cards.split()[0]]
        if cards.split()[0] == "A":
            ace_count += 1
    while ace_count >= 1 and hand_total > 21:
        hand_total -= 10
        ace_count -= 1
    return hand_total

def raw_total_calculator(hand):
    ace_count = 0
    raw_total = 0
    for cards in hand:
        raw_total += card_values[cards.split()[0]]
        if cards.split()[0] == "A":
            ace_count += 1
    processed_total = calculate_hand(hand)
    return ace_count,raw_total,processed_total


def ace_dropped(hand):
    _, raw_total, processed_total = raw_total_calculator(hand)
    current_ace = (raw_total - processed_total) / 10
    if current_ace >= 1:
        print("since you have reaced >21 and have a ace, your ace turns into 1")

#------soft17 logic------
def soft_17(hand):
    ace_count, raw_total, processed_total = raw_total_calculator(hand)
    current_ace = (raw_total - processed_total)  / 10
    return ace_count - current_ace >= 1 and processed_total == 17

#------Main------
player_bust = False
dealer_bust = False
while True:
    calculate_player_hand = calculate_hand(player_hand)
    print("your cards:", ', '.join(player_hand))
    print("your total:", calculate_player_hand)
    print (f'dealers first card: {dealer_hand[0]}')
    command = input("commands, hit, stand : ").strip().lower()

    if command == "hit":
        draw_card(player_hand)
        ace_dropped(player_hand)
        current_player_hand_total = calculate_hand(player_hand)
        if current_player_hand_total > 21:
            player_bust = True
            print("Bust!")
            print("your cards at the end:", ', '.join(player_hand))
            print("your total:", current_player_hand_total)
            break
    elif command == "stand":
        print("player decided to stand")
        break
    else:
        print("Unknown command. Don't just make things up.")

#------Dealer Logic------
while player_bust is not True:
    calculate_dealer_hand = calculate_hand(dealer_hand)
    print("Dealer's hand: ", ', '.join(dealer_hand))
    print("Dealer's total:", calculate_dealer_hand)

    if calculate_dealer_hand > 21:
        dealer_bust = True
        break
    if (calculate_dealer_hand == 17 and not soft_17(dealer_hand)) or calculate_dealer_hand >= 18:
        print("dealer decided to stand")
        break
    else:
        print("dealer decided to hit")
        draw_card(dealer_hand)

#------Stand-off------
if player_bust:
    print("dealer Win")
elif dealer_bust:
    print("Player Win")
else:
    if calculate_player_hand == calculate_dealer_hand:
        print("tie, no one wins")
    elif calculate_player_hand > calculate_dealer_hand:
        print("Player Win")
    elif calculate_player_hand < calculate_dealer_hand:
        print("Dealer Win")