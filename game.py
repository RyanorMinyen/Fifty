# *************
# This file contains game states implementation
# *************

from cards import Card
from shoe import Shoe


def initial_state() -> tuple:
    player = 0
    hand = []
    shoe = Shoe()

    return (player, hand, shoe)


def check_hand(hands: Card) -> bool:

    sum = 0
    for card in hands:
        sum+card.rank

    if sum <= 50:
        return False
    else:
        return True
