# Problem Set
#https://www.codingame.com/ide/puzzle/winamax-battle

import sys
import math

def cmp(card1, card2):
    value1 = card1[:-1]
    value2 = card2[:-1]

    # for ease of card value comparsion
    if value1 == '10':
        value1 = 'C'
    if value2 == '10':
        value2 = 'C'
    if value1 == 'A':
        value1 = 'Z'
    if value2 == 'A':
        value2 = 'Z'
    if value1 == 'K':
        value1 = 'Y'
    if value2 == 'K':
        value2 = 'Y'

    return (value1 > value2) - (value1 < value2)

def draw(player1_deck, player2_deck, player1_bet, player2_bet):

    # not enough card for WAR
    if len(player1_deck) < 3 or len(player2_deck) < 3:
        return False

    # Game Rule -- put aside 3 cards for WAR
    for i in range(3):
        player1_bet.append(player1_deck.pop(0))
        player2_bet.append(player2_deck.pop(0))

    return True

def fight(player1_deck, player2_deck, player1_bet, player2_bet, in_war=0):
    if in_war:
        if len(player1_deck) == 0 or len(player2_deck) == 0:
            return "PAT"

    card1 = player1_deck.pop(0)
    card2 = player2_deck.pop(0)

    player1_bet.append(card1)
    player2_bet.append(card2)
    result = cmp(card1, card2)

    # player1 win
    if result == 1:
        player1_deck.extend(player1_bet)
        player1_deck.extend(player2_bet)
    elif result == -1:
        player2_deck.extend(player1_bet)
        player2_deck.extend(player2_bet)
    else:
        # draw
        if draw(player1_deck, player2_deck, player1_bet, player2_bet):
            return fight(player1_deck, player2_deck, player1_bet, player2_bet, in_war=1)
        else:
            return "PAT"

    if len(player1_deck) == 0:
        return "2"
    elif len(player2_deck) == 0:
        return "1"
    return "cont"

player1_deck = []
player2_deck = []
round = 0

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

n = int(input())  # the number of cards for player 1
for i in range(n):
    cardp_1 = input()  # the n cards of player 1
    player1_deck.append(cardp_1)

m = int(input())  # the number of cards for player 2
for i in range(m):
    cardp_2 = input()  # the m cards of player 2
    player2_deck.append(cardp_2)

while(True):
    player1_bet = []
    player2_bet = []
    round += 1

    print(player1_deck, file=sys.stderr)
    print(player2_deck, file=sys.stderr)
    result = fight(player1_deck, player2_deck, player1_bet, player2_bet)

    print("Round {}".format(round), file=sys.stderr)
    print(player1_deck, file=sys.stderr)
    print(player2_deck, file=sys.stderr)

    # Should I continue the game ?
    if result != "cont":
        break

# Write an action using print
# To debug: print("Debug messages...", file=sys.stderr)
if result == "PAT":
    print(result)
else:
    print("{} {}".format(result, round))