import random


class Card:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value


class Deck:
    def __init__(self):
        self.cards = ['2', '3', '4', '5', '6', '7',
                      '8', '9', '10', 'J', 'Q', 'K', 'A'] * 4
        random.shuffle(self.cards)

    def dealCard(self):
        return Card(self.cards.pop())


def BaccaratGame(deck, balance):
    def getCardValue(card):
        if card.value in ['J', 'Q', 'K', '10']:
            return 0
        elif card.value == 'A':
            return 1
        else:
            return int(card.value)

    def calculateHandScore(hand):
        return sum(getCardValue(card) for card in hand) % 10

    if balance <= 0:
        print("Not enough balance!")
        return balance

    try:
        betAmount = int(input("Enter your bet: "))
    except ValueError:
        print("Invalid input.")
        return balance

    if betAmount > balance:
        print("Balance is to low for this bet")
        return balance

    betChoice = input("Bet on (player/banker/tie): ").lower()
    if betChoice not in ["player", "banker", "tie"]:
        print("Invalid bet choice.")
        return balance

    playerHand = [deck.dealCard(), deck.dealCard()]
    bankerHand = [deck.dealCard(), deck.dealCard()]

    playerScore = calculateHandScore(playerHand)
    bankerScore = calculateHandScore(bankerHand)

    print(
        f"Player's hand: {[card.value for card in playerHand]}, score: {playerScore}")
    print(
        f"Banker's hand: {[card.value for card in bankerHand]}, score: {bankerScore}")

    result = ""
    if playerScore > bankerScore:
        result = "player"
    elif playerScore < bankerScore:
        result = "banker"
    else:
        result = "tie"

    if result == betChoice:
        if betChoice == "tie":
            balance += betAmount * 8
        else:
            balance += betAmount
        print(f"You won! New balance: ${balance}")
    else:
        balance -= betAmount
        print(f"You lost. New balance: ${balance}")

    return balance


def calculateScore(hand):
    score = 0
    for card in hand:
        if card.value in ['J', 'Q', 'K']:
            score += 10
        elif card.value == 'A':
            score += 11 if score + 11 <= 21 else 1
        else:
            score += int(card.value)
    return score


def blackjackGame(deck, bet):
    playerHand = [deck.dealCard(), deck.dealCard()]
    dealerHand = [deck.dealCard(), deck.dealCard()]

    print(f"Dealer's visible card: {dealerHand[0]}")
    while True:
        playerScore = calculateScore(playerHand)
        print(f"Your hand: {playerHand}, score: {playerScore}")

        if playerScore > 21:
            return -bet
        if playerScore == 21:
            return bet

        playerChoice = input(
            "Do you want to hit or stand? Type 'hit' or 'stand': ")
        if playerChoice.lower() == 'hit':
            playerHand.append(deck.dealCard())
        else:
            break

    dealerScore = calculateScore(dealerHand)
    while dealerScore < 17:
        dealerHand.append(deck.dealCard())
        dealerScore = calculateScore(dealerHand)

    print(f"Dealer's final hand: {dealerHand}, score: {dealerScore}")
    if dealerScore > 21 or dealerScore < playerScore:
        return bet
    elif dealerScore > playerScore:
        return -bet
    else:
        return 0


def main():
    balance = 5000
    while True:
        print("Welcome to Tin's Casino! Choose your game:")
        print("1. Blackjack")
        print("2. Baccarat")
        print("3. Exit")
        choice = input("Enter your choice (1, 2, or 3): ")

        if choice == '1':
            while balance > 0:
                print(f"Current balance: ${balance}")
                bet = int(input("Bet amount? "))
                if bet > balance:
                    print("Invalid bet. Try a lower bet to be under balance.")
                    continue
                deck = Deck()
                balanceChange = blackjackGame(deck, bet)
                balance += balanceChange
                print(f"New balance: ${balance}")
                if balance <= 0:
                    print("No more money. You lose!")
                    break
                playAgain = input("Play again? (yes/no): ")
                if playAgain.lower() != 'yes':
                    break
        elif choice == '2':
            deck = Deck()
            balance = BaccaratGame(deck, balance)
        elif choice == '3':
            print("Thanks for playing!")
            break
        else:
            print("Try again. Please choose 1, 2, or 3.")


if __name__ == "__main__":
    main()
