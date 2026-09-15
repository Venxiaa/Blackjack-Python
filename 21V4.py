#Last and Final Version. its been fun coding this but its gotta end someway.
#TODO:
#   Powerup system
#   finalise things
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

#-----Deck Class-----
class Deck:
    def __init__(self, card_values, suits):
        self.card_values = card_values
        self.suits = suits
        self.deck_constructer()

    def deck_constructer(self):
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

    def temp_draw_card(self): #for Guaranteed non-bust
        self.hand.append(self.hand_deck.draw())

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
        self.inventory = []

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

#-----Shop Class----
class Shop:
    def __init__(self, player):
        self.player = player

    def peek_dealer_card(self):
        pass

    def guaranteed_safe_card(self):
        pass

    def discount_bet(self):
        pass

    def second_chance(self):
        pass



#-----Game Logic----
class Game:
    def __init__(self, player):
        self.player = player
        self.player_bust = False
        self.dealer_bust = False

    def betting_phase(self):
        while True:
            show_balance()
            if player.balance > 0:
                try:
                    bet = int(input("How much to bet?: "))
                    if bet < 0:
                        raise ValueError
                    if player.place_bet(bet):
                        print(f"\nYou placed a bet of ${bet}")
                        return True
                    else:
                        print(f"You don't have enough money missing amount: ${bet - player.balance}") 
                        continue
                except ValueError:
                    print("Invalid Input, needs to be a positive whole number.")
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

    def player_turn(self):
        deck = self.deck
        player_hand = self.player_hand
        dealer_hand = self.dealer_hand
        while True:
            players_hand_total = player_hand.calculated_hand
            message_banner(
            f"Your cards: {', '.join(player_hand.hand)}\n"
            f"Your total: {players_hand_total}\n"
            f"Dealer's first card: {dealer_hand.hand[0]}"
            )
            game_commands = ["Hit", "Stand"]
            game_command = input(f"Commands: {", ".join(game_commands)}: ").strip().lower()
            if game_command == "hit":
                player_hand.draw_card()
                player_hand.announce_ace_adjustment()
                if player_hand.calculated_hand > 21:
                    self.player_bust = True
                    print(
                    "\nBust!\n"
                    f"your cards at the end: {', '.join(player_hand.hand)}\n"
                    f"your total: {player_hand.calculated_hand}"
                    )
                    break
            elif game_command == "stand":
                print("player decided to stand")
                return
            elif game_command == "deck" and xray_:
                print(f"next 5 upcomming cards: {', '.join(deck.available_cards[:5])}")
            elif game_command == "dealer" and xray_:
                print(f"{', '.join(dealer_hand.hand)}")
            elif game_command == "win" and win_button:
                self.dealer_bust = True
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
        player_bust = self.player_bust
        dealer_bust = self.dealer_bust
        dealers_hand_total = self.dealer_hand.calculated_hand
        players_hand_total = self.player_hand.calculated_hand
        if player_bust:
            message_banner("Player Lost")
            player.lose_bet()
            show_balance()
        elif dealer_bust:
            message_banner("Player Won!")
            player.win_bet()
            show_balance()
        else:
            if players_hand_total == dealers_hand_total:
                message_banner("Player Tied")
                player.tie_bet()
                show_balance()
            elif players_hand_total > dealers_hand_total:
                message_banner("Player Won!")
                player.win_bet()
                show_balance()
            elif players_hand_total < dealers_hand_total:
                message_banner("Player Lost")
                player.lose_bet()
                show_balance()

#-----Reusable Prints-----
def message_banner(message):
    print(
    f"{'-' * 30}\n"
    f"{message}\n"
    f"{'-' * 30}")

#-----Menu Functions-----
def show_balance():
    print(f"\nYour Balance: ${player.balance}")

def start_play():
    game = Game(player)
    if game.betting_phase():
        #----Game Set-up-----
        game.start_round()
        #-----Player inteaction-----
        game.player_turn()
        #------Dealer Logic------
        game.dealer_turn()
        #------Stand-off------
        game.stand_off()
    else:
        print("No money to bet")

def exit_game():
    print("Exiting, Bye!")
    exit()

#-----Cheats-----
def hidden_menu():
    hidden_menu_actions = {
        "Money": money,
        "Xray": xray,
        "Winbutton": winbutton,
        "Leave": "",
    }
    while True:
        command = input(f"\nCommands: {", ".join(hidden_menu_actions)}: ").strip().capitalize()
        if command in hidden_menu_actions and cheats == True:
            hidden_menu_actions[command]()
        elif command == "Leave":
            print("")
            break
        else:
            print("unknown command")

def show_cheats():
    global cheats
    cheats = True
    print(
    "\nCheat commands (Enter in hidden menu):\n"
    "Money, spawns in money\n"
    "Xray, see dealer/deck cards\n"
    "Winbutton, win button."
    )

def money():
    try:
        player.money(int(input("How much money do you want: ")))
        show_balance()
    except ValueError:
        print("\nInvalid Input, needs to be a positive whole number.")

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
    "Play": start_play,
    "Balance": show_balance,
    "Exit": exit_game,
    "Secretmenu": hidden_menu,
    "Whatcheats": show_cheats,
}
while True:
    command = input(f"Commands: {", ".join(menu_actions)}: ").strip().capitalize()
    if command in menu_actions:
        menu_actions[command]()
    else:
        print("unknown command")