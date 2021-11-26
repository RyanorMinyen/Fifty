# the card class

class Card:
    suit = None
    rank = None

    suits = ['S', 'H', 'D', 'C']  # Spade, Heart, Diamond, Club
    ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __toString__(self):
        return self.rank + self.suit

    def __equal__(self, other):
        if isinstance(other, Card):  # check if the object is a Card
            return self.rank == other.rank and self.suit == other.suit
        else:
            return "Not a card!"  # if not a card, no comparison should be performed
