# *************
# This file contains game states implementation
# *************

from cards import Card
from deck import Deck

DECK_SIZE = 6


def initial_state() -> tuple:
    player = 0
    hand = []
    deck = Deck(DECK_SIZE)

    return (player, hand, deck)


def check_hand(hands: Card) -> bool:

    sum = 0
    for card in hands:
        sum+card.ranks

    if sum <= 50:
        return False
    else:
        return True
