
from cards import Card
from random import shuffle

ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Deck:

    def __init__(self, DECK_SIZE):
        self.cards = self.init_cards()
        self.size = DECK_SIZE

    def counts(self):
        return len(self)

#     def shoe(DECK_SIZE):
#         shoe = []
#         for i in range(0, DECK_SIZE):
#             shoe.append(Deck())

#         shuffle(shoe)
#         return shoe

    def init_cards(self):
        cards = []

        for rank in ranks:
            for i in range(0, 4):
                cards.append(Card(rank))

        shuffle(cards)
        return cards
