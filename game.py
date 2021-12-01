# *************
# This file contains game states implementation
# *************

import numpy as np
from cards import Card
from shoe import Shoe

# global variables
player = 0
dealer = 1


def initial_state() -> tuple:

    dealer_hand = []
    player_hand = []
    shoe = Shoe()

    return (player_hand, dealer_hand, shoe)


def show_hand(hand: Card):
    stringofCards = ""
    for card in hand:
        stringofCards += card.rank + " "

    return stringofCards


def draw_cards(player_hand, dealer_hand, shoe) -> tuple:
    # draw 5 cards for player and dealer
    for i in range(5):
        player_hand.append(shoe.draw())
        dealer_hand.append(shoe.draw())

    return (player_hand, dealer_hand, shoe)


def draw_one_card(player_hand, dealer_hand, shoe) -> tuple:
    player_hand.append(shoe.draw())

    return (player_hand, dealer_hand, shoe)


def compare_hands(player_hand, dealer_hand) -> int:
    if score(player_hand) > score(dealer_hand):
        return 1
    elif score(player_hand) < score(dealer_hand):
        return -1
    else:
        return 0


def score(hand: Card) -> int:
    sum = 0
    for card in hand:
        if card.rank == 'J':
            sum += 10
        elif card.rank == 'Q':
            sum += 10
        elif card.rank == 'K':
            sum += 10
        elif card.rank == 'A':
            sum += 11
        else:
            sum += int(card.rank)

    return sum


if __name__ == '__main__':

    game_state = initial_state()
    game_state = draw_cards(game_state[0], game_state[1], game_state[2])

    player_hand = game_state[0]
    dealer_hand = game_state[1]
    remaining_cards = game_state[2]

    print("Player hand: " + show_hand(player_hand))
    print("Dealer hand: " + show_hand(dealer_hand))
    print("Remaining cards: " + str(remaining_cards.count()))

    player_score = score(player_hand)
    dealer_score = score(dealer_hand)

    while player_score < 55 and dealer_score < 55:
        print("Player score: " + str(player_score))
        print("Dealer score: " + str(dealer_score))
        print("Remaining cards: " + str(remaining_cards.count()))
        print("Hit or stay?")
        choice = input()

        if choice == "hit":
            game_state = draw_one_card(
                game_state[0], game_state[1], game_state[2])
            player_hand = game_state[0]
            print("Player hand: " + show_hand(player_hand))
            dealer_hand = game_state[1]
            remaining_cards = game_state[2]
            player_score = score(player_hand)
            dealer_score = score(dealer_hand)
        else:
            # dealer will stand on 50
            # yet to be implemented

            print("Dealer hand: " + show_hand(dealer_hand))

            if (compare_hands(player_hand, dealer_hand)) == 1:
                print("Player wins!")
                break
            elif (compare_hands(player_hand, dealer_hand)) == -1:
                print("Dealer wins!")
                break
            else:
                print("Draw!")
                break
