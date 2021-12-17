# the card class
# Suits doesn't matter in Fifty nor in BlackJack
# ranks 2-9 have value 2-9, correspondingly. Ace can be either 1 or 11, 10 through kings all have value 10.
# the natural win is five 10s


class Card:

    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, rank):
        # self.suit = suit
        self.rank = rank

    def __toString__(self):
        return self.rank

    def __equal__(self, other):
        if isinstance(other, Card):  # check if the object is a Card
            return self.rank == other.rank
        else:
            return "Not a card!"  # if not a card, no comparison should be performed

    def value(self) -> int:

        if self.rank == 'J':
            return 10
        elif self.rank == 'Q':
            return 10
        elif self.rank == 'K':
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
