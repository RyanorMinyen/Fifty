
from cards import Card
from random import shuffle

DECK_SIZE = 6  # change this to change the number of decks

ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']


class Shoe:

    def __init__(self):
        self.cards = self.make_cards(DECK_SIZE)

    def count(self):
        return len(self.cards)

    def __toString__(self):

        stringofCards = ""
        for card in self.cards:
            stringofCards += card.rank + " "

        return stringofCards

    def draw(self):
        while self.isEmpty() == False:
            return self.cards.pop()

    def isEmpty(self):
        if self.count() == 0:
            return True
        else:
            return False

    def make_cards(self, DECK_SIZE):
        cards = []

        for i in range(0, DECK_SIZE):
            for rank in ranks:
                for i in range(0, 4):
                    cards.append(Card(rank))

        shuffle(cards)
        return cards
