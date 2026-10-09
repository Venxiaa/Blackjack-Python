#Last and Final Version. its been fun coding this but its gotta end someway.
# Changelog (Compared to V3)

#   Added a shop system for purchasing power-ups
#   Added player inventory to store and manage purchased power-ups
#   Added three power-ups:
#       - Second Chance: Automatically voids a busting card once per round
#       - Guaranteed Safe Card: Draws a card that will not cause a bust
#       - Peek Dealer Card: Reveals the dealer's hand once per round
#   Added power-up prices and item abbreviations (SC, GSC, PDC)
#   Added quantity-based purchases with input validation and purchase confirmation
#   Added automatic Second Chance activation when the player busts
#   Added a dedicated Powerups class to manage power-up functionality
#   Improved Hand class with an is_losing() method to check for busts
#   Improved Hand class to use the Deck object directly
#   Added a player option to leave the betting phase
#   Added an all-in betting option
#   Added softlock prevention when the player's balance reaches zero
#   Refactored player turn commands into a function dictionary
#   Added in-game help and commands for power-ups, inventory, and item listings
#   Added reusable command menus for the main menu, shop, and game
#   Added a dedicated shop menu with item listings and purchasing
#   Added an inventory display in the main menu and during gameplay
#   Added a secret menu to access cheats
#   Improved cheat command handling and fixed the issue with leaving the secret menu
#   Replaced the main menu's if/elif command chain with a function dictionary
#   Refactored stand_off() to reduce repeated result-handling and payout code
#   Improved overall game organisation by separating power-up, shop, and game logic
#   Cleaned up betting and round flow to support the new features

import random

#-----Card Data-----
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

#-----Power Up data----
items_and_abriv = {
            "second-chance": {"name": "Second Chance", "price": 1500},
            "guaranteed-safe-card": {"name": "Guaranteed Safe Card", "price": 1250},
            "peek-dealer-card": {"name": "Peek Dealer Card", "price": 1150}
        }
items_and_abriv["sc"] = items_and_abriv["second-chance"]
items_and_abriv["gsc"] = items_and_abriv["guaranteed-safe-card"]
items_and_abriv["pdc"] = items_and_abriv["peek-dealer-card"]

#-----Deck Class-----
class Deck:
    def __init__(self, card_values, suits):
        self.card_values = card_values
        self.suits = suits
        self.deck_constructor()

    def deck_constructor(self): 
        available_cards = []
        for types in self.suits:
            for ranks in self.card_values:
                available_cards.append(ranks + " of " + types)
        random.shuffle(available_cards)
        self.available_cards = available_cards

    def draw(self):
        return self.available_cards.pop(0)

#-----Hand Class-----
class Hand:
    def __init__(self, hand, deck):
        self.hand = hand
        self.hand_deck = deck
        self.card_values = deck.card_values

    def calculate_hand(self):
        total = sum(self.card_values[card.split()[0]] for card in self.hand)
        aces = sum(card.split()[0] == "A" for card in self.hand)
        adjusted_total = total
        aces_as_one = 0
        while aces_as_one < aces and adjusted_total > 21:
            adjusted_total -= 10
            aces_as_one += 1
        self.raw_total = total
        self.calculated_hand = adjusted_total
        self.ace_count = aces
        return adjusted_total

    def draw_card(self):
        self.hand.append(self.hand_deck.draw())
        self.calculate_hand()

    def is_losing(self):
        return self.calculated_hand > 21
    
    def announce_ace_adjustment(self):
        current_ace = (self.raw_total - self.calculated_hand)  / 10
        if current_ace >= 1:
            print("since you have reaced >21 and have a ace, your ace turns into 1")

    def soft_17(self):
        current_ace = (self.raw_total - self.calculated_hand)  / 10
        return self.ace_count - current_ace >= 1 and self.calculated_hand == 17

#-----Player Class-----
class Player:
    def __init__(self, balance=1000):
        self.balance = balance
        self.placed_bet = 0
        self.inventory = {
            "Second Chance": 0,
            "Guaranteed Safe Card": 0,
            "Peek Dealer Card": 0,
        }

    def place_bet(self,amount):
        if amount > self.balance:
            return False
        else:
            self.balance -= amount
            self.placed_bet = amount
            return True

    def win_bet(self):
        self.balance += self.placed_bet*2
        self.placed_bet = 0

    def tie_bet(self):
        self.balance += self.placed_bet
        self.placed_bet = 0

    def lose_bet(self):
        self.placed_bet = 0

    def money(self,amount):
        self.balance += amount

    def softlock(self):
        if self.balance == 0:
            print("Softlock prevention: you sold your newborn child for $200")
            self.balance = 200

#-----Powerups Class----
class Powerups:
    def __init__(self, game_data):
        self.game = game_data
        self.used_second_chance = False
        self.used_peek_dealer_card = False
    
    def peek_dealer_card(self):
        if self.used_peek_dealer_card == False:
            self.used_peek_dealer_card = True
            print(f"dealer's cards: {', '.join(self.game.dealer_hand.hand)}")
            self.game.player.inventory["Peek Dealer Card"] -= 1
        else: print(f"Powerup has already been used")
        
    def guaranteed_safe_card(self):
        game_object = self.game
        if game_object.player_hand.calculated_hand == 21:
            print("Player already has 21, no available card would be found. Player is not charged")
            return
        count = 0
        card_found = False
        current_gamestate = game_object.deck.available_cards.copy(), game_object.player_hand.hand.copy()
        temp_deck = Deck(card_values, suits)
        temp_deck.available_cards = current_gamestate[0]
        temp_hand = Hand(current_gamestate[1], temp_deck)
        while True:
            if len(temp_deck.available_cards) == 0:
                print("Available card cannot be found, player wasn't charged")
                break
            temp_hand.draw_card()
            if temp_hand.is_losing():
                temp_hand.hand.pop()
                count += 1
            else: 
                card_found = True
                break
        if card_found == True:
            print(f"Card You Got: {game_object.deck.available_cards[count]}")
            game_object.player_hand.hand.append(game_object.deck.available_cards.pop(count))
            game_object.player_hand.calculate_hand()
            game_object.player.inventory["Guaranteed Safe Card"] -= 1
        

    def second_chance(self):
        game_object = self.game
        
        if game_object.player_hand.is_losing() and self.used_second_chance == False:
            card = game_object.player_hand.hand.pop()
            print(f"Second chance has been automatically used. card voided: {card}")
            game_object.player_hand.calculate_hand()
            game_object.player.inventory["Second Chance"] -= 1
            self.used_second_chance = True
            return
        elif self.used_second_chance:
            print("Second Chance has already been used.")


#-----Game Logic----
class Game:
    def __init__(self, player):
        self.player = player
        self.player_bust = False
        self.dealer_bust = False

    def betting_phase(self):
        while True:
            show_balance()
            if self.player.balance > 0:
                try:
                    bet = input("How much to bet? (amount/leave/allin): ").strip().lower()
                    if bet == "leave":
                        print("")
                        return None
                    elif bet == "allin":
                        print(f"\nYou placed a bet of ${self.player.balance}")
                        self.player.place_bet(self.player.balance)
                        return True

                    bet = int(bet)
                    if bet <= 0:
                        raise ValueError
                    if self.player.place_bet(bet):
                        print(f"\nYou placed a bet of ${bet}")
                        return True
                    else:
                        print(f"\nYou don't have enough money missing amount: ${bet - self.player.balance}") 
                        continue
                except ValueError:
                    print("\nInvalid Input, needs to be a positive whole number.")
                    continue
            else:
                return False

    def start_round(self):
        deck = Deck(card_values, suits)
        player_hand = Hand([], deck)
        dealer_hand = Hand([], deck)
        for _ in range(2):
            player_hand.draw_card()
            dealer_hand.draw_card()
        self.deck = deck
        self.player_hand = player_hand
        self.dealer_hand = dealer_hand
        self.powerups = Powerups(self)
        
    def player_turn(self):
        def hit():
            player_hand.draw_card()
            if self.player.inventory["Second Chance"] > 0:
                self.powerups.second_chance()
            player_hand.announce_ace_adjustment()
            if player_hand.calculated_hand > 21:
                self.player_bust = True
                print(
                "\nBust!\n"
                f"your cards at the end: {', '.join(player_hand.hand)}\n"
                f"your total: {player_hand.calculated_hand}"
                )

        def use_powerup(command):
            if command in items_and_abriv:
                if self.player.inventory[items_and_abriv[command]["name"]] >= 1:
                    command_name = items_and_abriv[command]["name"].lower().replace(" ","_")
                    if command_name != "second_chance":
                        method = getattr(self.powerups, command_name)
                        method()
                    else:
                        print(f"You can't use Second chance, its activated automatically")
                else:
                    print("You cannot use a item you don't have")
            else:
                print(f"{command} isn't a command. you can type 'items' for all the items")

        def deck():
            if xray_: print(f"next 5 upcomming cards: {', '.join(self.deck.available_cards[:5])}")
            else: print("Unknown command. Don't just make things up.")

        def dealer():
            if xray_: print(f"{', '.join(self.dealer_hand.hand)}")
            else: print("Unknown command. Don't just make things up.")

        def winbutton():
            if win_button: self.dealer_bust = True
            else: print("Unknown command. Don't just make things up.")

        player_hand = self.player_hand
        game_commands = {
            "hit": hit,
            "use": use_powerup,
            "items": show_shop_items,
            "inv": show_player_inventory,
            "deck": deck,
            "dealer": dealer,
            "win": winbutton,
        }

        game_command_menu()

        while True:
            players_hand_total = player_hand.calculated_hand
            message_banner(
            f"Your cards: {', '.join(player_hand.hand)}\n"
            f"Your total: {players_hand_total}\n"
            f"Dealer's first card: {self.dealer_hand.hand[0]}"
            )
            game_command = input(f"Command: ").strip().lower()

            if game_command in ["help", "?"]:
                game_command_menu()
            elif game_command in game_commands and game_command != "use":
                game_commands[game_command]()
                if self.player_bust or self.dealer_bust:
                    break
            elif len(game_command) > 0 and game_command.split()[0] == "use": 
                if game_command == "use":
                    print("Cannot use nothing, try use <item>. you can type items to show item list")
                else:
                    game_commands[game_command.split()[0]](game_command.split()[1])
            elif game_command == "stand":
                print("player decided to stand")
                break
            else:
                print("Unknown command. Don't just make things up.")

    def dealer_turn(self):
        dealer_hand = self.dealer_hand
        while self.player_bust == False and self.dealer_bust == False:
            calculated_dealer_hand = dealer_hand.calculated_hand
            print(
                f"\nDealer's hand: {', '.join(dealer_hand.hand)}\n"
                f"Dealer's total: {calculated_dealer_hand}"
                )
            if calculated_dealer_hand > 21:
                self.dealer_bust = True
                print("Dealer Has Busted")
                break
            if (calculated_dealer_hand == 17 and not dealer_hand.soft_17()) or calculated_dealer_hand >= 18:
                print("dealer decided to stand")
                break
            print("dealer decided to hit")
            dealer_hand.draw_card()

    def stand_off(self):
        if self.player_bust:
            result = "Player Lost"
            action = self.player.lose_bet

        elif self.dealer_bust:
            result = "Player Won!"
            action = self.player.win_bet

        elif self.player_hand.calculated_hand == self.dealer_hand.calculated_hand:
            result = "Player Tied"
            action = self.player.tie_bet

        elif self.player_hand.calculated_hand > self.dealer_hand.calculated_hand:
            result = "Player Won!"
            action = self.player.win_bet

        else:
            result = "Player Lost"
            action = self.player.lose_bet

        message_banner(result)
        action()
        show_balance()


#-----buy item function-----
def buy_item(shop_command):
    parts = shop_command.split()

    def number_validator(value):
        try: valid_number = int(value)
        except ValueError:
            return "NaN"
        if valid_number > 0:
            return "valid"
        elif valid_number == 0:
            return "zero"
        else:
            return "negetive"

    if len(parts) == 3:
        check_number = number_validator(parts[2])
        if parts[1] in items_and_abriv and check_number == "valid":

            item = parts[1]
            item_price = items_and_abriv[item]["price"]
            quantity = int(parts[2])
            total_price = quantity*item_price

            if player.balance >= total_price:
                item_name = items_and_abriv[item]["name"]
                message_banner(
                f"Item: {item_name} x {quantity}\n"
                f"Total Cost: ${total_price} (Current Balance: ${player.balance})")
                while True:
                    confirm_input = input("purchase (yes/no)(leaving it empty is a automatic yes)? ").strip().lower()
                    if confirm_input in ["yes", "y", ""]:
                        confirm = True
                        break
                    elif confirm_input in ["no", "n"]:
                        confirm = False
                        break
                    else:
                        print("Unknown command.")
                if confirm:
                    player.inventory[item_name] += quantity
                    player.balance -= total_price
                    print(f"Purchase successful! Remaining balance: ${player.balance}")
                    show_player_inventory()
                else:
                    print("\nPurchase cancelled by user.")
            else:
                print(f"\nNot enough money! You need ${total_price - player.balance} more.")
        elif parts[1] not in items_and_abriv:
            print("Item not found")
        else:
            if check_number == "zero":
                print("\nYou can't buy 0 items!")
            elif check_number == "negetive":
                print("\nYou can't buy negetive items!")
            elif check_number == "NaN":
                print("\nNot a number")
    else:
        print("\nUnknown command. Format should be: buy <item> <quantity>")


#-----Reusable Prints-----
def message_banner(message):
    print(
    f"{'-' * 30}\n"
    f"{message}\n"
    f"{'-' * 30}")

def main_menu_command_list():
    message_banner(
        "Available Commands:\n"
        "? / help | Shows available commands\n"
        "Play | Starts the game\n"
        "Shop | Buy Powerups at the shop™\n"
        "Balance | Show the player's balance\n"
        "Inv | Shows the player's powerup inventory\n"
        "Exit | Closes the game\n"
        "WhatCheats | Shows and enables cheats"
    )
def shop_menu_command_list():
    message_banner(
        "Available Commands:\n"
        "? / help | Shows available commands\n"
        "Items | Shows available items and it's description\n"
        "Buy | Buys item(s) usage: buy <item> <amount> / buy guaranteed-safe-card 21 / buy GSC 21\n"
        "Leave | Leaves the shop"
    )
def show_shop_items():
    message_banner(
        "items also have abbreviations e.g guaranteed-safe-card -> GSC\n"
        "second-chance ($1500) | Activates automatically upon player getting more than 21 (ONLY CAN BE USED ONCE PER ROUND)\n"
        "guaranteed-safe-card ($1250) | Manual activation before hitting (P.S. using it automaticaly hits)\n"
        "peek-dealer-card ($1150) | Manual activation. shows dealer's cards (ONLY CAN BE USED ONCE PER ROUND)\n"
    )

def game_command_menu():
    message_banner(
        "Available Commands:\n"
        "? / help | Shows available commands\n"
        "Hit | Draw a card for the deck. If you get more than 21, you bust\n"
        "Stand | Your score is locked and Ends your turn\n"
        "Items | Shows available items and it's description\n"
        "Use | Uses a item if you have one. usage: use <item> e.g. use gsc\n"
        "Inv | Displays the items in your inventory\n"
        )

def show_player_inventory():
    message_banner(f"player inventory:\n{"\n".join(f"{item}: {amount}" for item, amount in player.inventory.items())}")

#-----Menu Functions-----
def start_play():
    game = Game(player)
    bet = game.betting_phase()
    if bet:
        #----Game Set-up-----
        game.start_round()
        #-----Player inteaction-----
        game.player_turn()
        #------Dealer Logic------
        game.dealer_turn()
        #------Stand-off------
        game.stand_off()
    elif bet == None:
        print("Player chose to leave")
    else:
        print("No money to bet")


def shop():
    shop_menu_command_list()
    print("Welcome to the shop!\n")
    while True:
        shop_command = input("Shop Command: ").strip().lower()
        if shop_command == "items":
            show_shop_items()
        elif shop_command != "" and shop_command.split()[0] == "buy":
            buy_item(shop_command)
        elif shop_command == "leave":
            print("\nYou left the Shop")
            break
        else:
            print("\nunknown command")

def show_balance():
    print(f"Your Balance: ${player.balance}")


def exit_game():
    print("Exiting, Bye!")
    exit()


#-----Cheats-----
def hidden_menu():
    hidden_menu_actions = {
        "Money": money,
        "Xray": xray,
        "Winbutton": winbutton,
        "Leave": "\nExiting Secret Menu.",
    }
    while True:
        command = input(f"Commands: {", ".join(hidden_menu_actions)}: ").strip().capitalize()
        if command == "Leave":
            print(hidden_menu_actions[command])
            break
        elif cheats == False:
            print("\nCheats are disabled, enter whatcheats in the main command to activate")
        elif command in hidden_menu_actions and cheats == True:
            hidden_menu_actions[command]()
        else:
            print("\nunknown command")

def show_cheats():
    global cheats
    cheats = True
    message_banner(
    "Cheat commands (Enter 'secretmenu' inside the commands to use):\n"
    "Money, spawns in money\n"
    "Xray, see dealer/deck cards\n"
    "Winbutton, win button."
    )

def money():
    try:
        wanted_money = int(input("How much money do you want: "))
        if wanted_money <= 0:
            print("You can't spawn in 0 or a negetive amount of money")
        else:
            player.money(wanted_money)
            show_balance()
    except ValueError:
        print("\nInvalid Input, needs to be a whole number.")

def xray():
    global xray_
    xray_ = True
    print("\nxray enabled, during hit/stand type in deck/dealer to see the cards")

def winbutton():
    global win_button 
    win_button = True
    print("\nwin button enabled, during hit/stand type win to instantly win")

#-----main-----
player = Player()
cheats = False
xray_ = False
win_button = False

menu_actions = {
    "play": start_play,
    "shop": shop,
    "balance": show_balance,
    "inv": show_player_inventory,
    "exit": exit_game,
    "secretmenu": hidden_menu,
    "whatcheats": show_cheats,
}
main_menu_command_list()
while True:
    player.softlock()
    command = input(f"Commands: ").strip().lower()
    if command in ["?", "help"]:
        main_menu_command_list()
    elif command in menu_actions:
        print("")
        menu_actions[command]()
    else:   
        print("\nunknown command")