import random
#From a standard 52 card set you choose a suit, such as the spades.
#From your selected suit you keep the face cards (J, Q, and K) and the ace (A).
#In most games the standard ordering of these cards (from least strong to strongest) is JQKA.
#make order of faces. 
faces = ["J", "Q", "K", "A"] #placeholder until I get more confirmation

#Players: 1 player against computer or 2 human players.

#Task 1: Game calibration

#Estimate how often (how likely) a count of 0, 1, 2, or 4 is to be observed.

#To do
#function to compare two sets of cards and return the score.
def compare(cards1: list, cards2: list) -> int:
    #initialize counter
    same_count = 0
    print("Original order: JQKA")
    print(f"New order: {''.join(cards2)}")
    #compare cards in each position
    for i in range(4):
        if cards1[i] == cards2[i]:
            same_count += 1
    return same_count

#    Write a function that shuffles the cards JQKA and counts the number of cards that stay put relative to the standard ordering.
def shuffle_count(cards: list) -> int:
    #makes a copy of cards list and shuffles that
    shuffled = [card for card in cards]
    random.shuffle(shuffled)
    #gets the score between the original deck and shuffled deck
    return compare(cards, shuffled)

#    Write a program that estimates the probability of each of these outcomes. Choose an appropiate data structure to save these data.

#calculate possible outcomes and store them in probabilities dictionary for reference.
def get_chances() -> None:
    #since having a score of four would mean each card has one possible destination, there's only one outcome that would lead to that score.
    fours = 1
    #a score of two would mean two cards stay in the same position, while the other two flip. That means for each possible pair of cards, there's one outcome that leads to a 2 
    # (for example, if J and Q stay in the same place, the two outcomes are JQKA (a 4), or JQAK (a 2))
    #So the amount of possible outcomes that lead to a 2 score is the same as the amount of possible combinations of two cards from the faces.
    #For four cards, this equals 3 (amount of pairs for the first card) plus 2 (amount of pairs for second card, not counting the first card) plus one (third card and fourth card)
    twos = 6
    #A score of one means only one card stays in position. For each card this happens to, there are three cards that are free to move. Since the amount of ways to arrange a number of objects is the factorial of said number, this makes 3 * 2 * 1 (or 6) combos
    # (for example, if J stays in place, the possible outcomes are JQKA, JQAK, JKQA, JKAQ, JAQK, JAKQ)
    #Out of these six outcomes, only two result in a 1 outcome. Since there are four cards, that's two results each, leaving us with eight.
    ones = 8
    #The amount of possible combinations of any group of items is equal to the factorial of the number of items. Since there's four cards, that gives us 4 * 3  * 2 * 1, or 24 possible outcomes.
    total_possibilities = 24
    #Since the only other possible outcome is a score of 0, we can just subtract all other outcomes from the total, or 24 - (1 + 6 + 8)
    zeros = 9
    #enter the chances for each outcome here
    probabilities = {0: 9, 1: 8, 2: 6, 4: 1}

#Task 2: Game development
#This will be player one and player two.
class Player:
    def __init__(self, name, is_self_aware: bool) -> None:
        self.bet = 0
        self.budget = 1000
        self.name = name
        #determine if player is user controlled or computer controlled.
        self.aware = is_self_aware
    #get a bet from the player
    def get_bet(self) -> None:
        #if human controlled, ask for bet.
        if self.aware:
            while True:
                bet = input(f"{self.name}, you have {self.budget} chips. How much would you like to bet?\n")
                #check if user entered a number, and if not, restart the loop until they do.
                if not bet.isnumeric():
                    print("Please enter a number.")
                    continue
                #change bet from string to integer.
                bet = int(bet)
                #if bet is in valid range, set the player's bet to it.
                if bet > 0 and bet <= self.budget:
                    self.bet = bet
                    break
                print(f"Please enter a number between 1 and {self.budget}.")
        #if robot controlled, bet a random amount.
        else:
            self.bet = random.randint(1, self.budget)
        #display bet.
        print(f"{self.name} bets {self.bet} chips!")
    #have player guess what the score will be.
    def get_guess(self) -> None:
        #if human controlled, ask for guess and display multipliers.
        if self.aware:
            print(f"{self.name}, how many cards out of four do you think will be unchanged after shuffling?")
            print("0) None (1x bet multiplier if correct)")
            print("1) One (1x bet multiplier if correct)")
            print("2) Two (1.5x bet multiplier if correct)")
            print("4) All four (3x bet multiplier if correct)")
            while True:
                guess = input("Enter the number of your choice here: ")
                #check to see if a valid guess was entered, and if so, set the guess.
                if guess in ["0", "1", "2", "4"]:
                    self.guess = int(guess)
                    print(f"{self.name} guesses {guess}.")
                    break
                print("Please enter 0, 1, 2, or 4.")
        #if robot controlled, guess a random score.
        else:
            self.guess = random.choice([0, 1, 2, 4])
            print(f"{self.name} guesses {self.guess}.")


#bet multipliers depending on probability.
multipliers = {0: 1.0, 1: 1.0, 2: 1.5, 4: 3}
#Write a program that asks for a number of players (1 or 2 players). If number of players is one, player plays against a computer player.
def game():
    while True:
        #will keep asking until a valid response is given.
        how_many = input("Would you like to play with (1) player or (2) players? Please enter your number now: ")
        if how_many in ["1", "2"]:
            break
    #convert how_many into a bool to enter into player initialization
    how_many = (how_many == "2")
    #create players
    players = [Player("Player1", True), Player("Player2", how_many)]
    #Playing mode: Some specified number of rounds r or until a player goes bankrupt, which ever happens first. After r rounds the player with highest balance wins. If player A goes bankrupt, player B wins!
    round_count = 7
    while round_count > 0:
        print(f"Rounds left: {round_count}")
        #Write a program that asks for a bet from the user. A bet includes a guess for the number of fixed cards and a currency amount.
        for player in players:
            player.get_bet()
            player.get_guess()
        #Based on the probability of a possible count, choose appropiate prizes.
        #get the actual score
        result = shuffle_count(faces)
        #If a player's guess for the count is successful, the player wins some amount of currency times the amount bet
        for player in players:
            if player.guess == result:
                #multiply earnings by appropriate multiplier
                winnings = int(player.bet * multipliers[result])
                print(f"{player.name} guessed right and wins {winnings} chips!")
            else:
                #earnings is a loss of the betted amount
                winnings = -(player.bet)
                print(f"{player.name} guessed wrong and loses {player.bet} chips!")
            #adjust player chips accordingly and reset bet
            player.bet = 0
            player.budget += winnings
            print(f"{player.name} now has {player.budget} chips.")
        #check if either player is bankrupt, and if so, exit the game.
        for i in range(2):
            if players[i].budget <= 0:
                #players[i-1] is the other player. if i is zero, then i-1 = -1, and players[-1] would just be the last item on the list, or player 2
                input(f"{players[i-1].name} wins! Enter any input to exit :")
                return
        #decrement round counter and reset all necessary variables
        round_count -= 1
        winnings = 0
    #if all rounds run out, end the game, print the scores, and decide the winner.
    print(f"Game over! Final scores: {players[0].name}: {players[0].budget}. {players[1].name}: {players[1].budget}.")
    #figure out winner
    if players[0].budget > players[1].budget:
        print(f"{players[0].name} wins!")
    elif players[0].budget < players[1].budget:
        print(f"{players[1].name} wins!")
    else:
        print("Tie!")
    input("Enter any input to exit: ")
    #Your program should track the bets, the winnings, the balance for each player, and declare a winner.



#Task 3: Combine

#Unify all the subrutines above into one coherent program.
#game loop
while True:
    start_game = input("Welcome to GuessGame! Would you like to start a new game? y/n\n")
    if start_game == "y":
        game()
    elif start_game == "n":
        break
    else:
        print("Not a valid answer. Please enter y or n.")
