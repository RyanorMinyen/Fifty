import numpy as np
import game
import shoe
import cards
import torch as tr
import matplotlib.pyplot as pt

# Had an error plotting the learning curve
# This little section of the code is provided on https://stackoverflow.com/questions/20554074/sklearn-omp-error-15-initializing-libiomp5md-dll-but-found-mk2iomp5md-dll-a"
# Issue is fixed

import os
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

################################################

def dealer(dealer_hand, remaining_cards):
    dealer_score = sum(dealer_hand)
    while dealer_score < 50:
        dealer_hand.append(remaining_cards.draw())
        dealer_score = sum(dealer_hand)
        print("Dealer hand: " + game.show_hand(dealer_hand))
        print("Dealer score: " + str(dealer_score))

    dealer_busted = game.busted(dealer_hand)
    if(dealer_busted):
        print("Dealer busted, player wins")
        return (True, dealer_hand, remaining_cards)

    return (False, dealer_hand, remaining_cards)


def sum(cards) -> int:
    score = 0
    for card in cards:
        if card.rank == 'J':
            score += 10
        elif card.rank == 'Q':
            score += 10
        elif card.rank == 'K':
            score += 10
        elif card.rank == 'A':
            score += 11
        else:
            score += int(card.rank)
    return score


def ai_play_turn(player_hand, dealer_hand, remaining_cards):

    player_score = sum(player_hand)
    while player_score < 50:
        player_hand.append(remaining_cards.draw())
        player_score = sum(player_hand)
        print("Player hand: " + game.show_hand(player_hand))
        print("Player score: " + str(player_score))

    player_busted = game.busted(player_hand)
    if(player_busted):
        print("Player busted, dealer wins")
        return False, remaining_cards

    dealer_busted, dealer_hand, remaining_cards = dealer(
        dealer_hand, remaining_cards)
    if(dealer_busted == False):
        if(player_score > sum(dealer_hand)):
            print("Player wins")
            return True, remaining_cards
        elif(player_score < sum(dealer_hand)):
            print("Dealer wins")
            return False, remaining_cards
        else:
            print("Draw")
            return True, remaining_cards

    return dealer_busted, remaining_cards


def cards(DECK_SIZE) -> tuple:

    cards = shoe.Shoe(DECK_SIZE)

    return cards


def simulationOneGame(player_hand, dealer_Hand, remaining_cards):

    game_state = game.draw_cards(player_hand, dealer_Hand, remaining_cards)

    player_hand = game_state[0]
    dealer_hand = game_state[1]
    remaining_cards = game_state[2]

    player_score = sum(player_hand)
    dealer_score = sum(dealer_hand)

    print()
    print("Player hand: " + game.show_hand(player_hand))
    print("Dealer hand: " + game.show_hand(dealer_hand))

    # evaluate the first five cards

    if(game.FiftyFive(player_score, dealer_score)):
        if(player_score == 55 and dealer_score == 55):
            print("Draw")
            return (True, player_hand, remaining_cards)
        elif(player_score == 55):
            print("Player wins")
            return (True, player_hand, remaining_cards)
        else:
            print("Dealer wins")
            return (False, player_hand, remaining_cards)
    else:
        print("Player score: " + str(player_score))
        print("Dealer score: " + str(dealer_score))
        print("Remaining cards: " + str(remaining_cards.count()))

        player_win, remaining_cards = ai_play_turn(
            player_hand, dealer_hand, remaining_cards)
        if(player_win):
            print()
            print("Player score: " + str(sum(player_hand)) +
                  " Dealer score: " + str(sum(dealer_hand)))
            return (True, player_hand, remaining_cards)
        return player_win, player_hand, remaining_cards


# Reference code ANNs.ipynb from the in class example provided by Professor Katz
################################################################################
# This code is slightly modified
def state_tensor(cards, DECK_SIZE):
    # cards == [number,...,number]
    state = tr.zeros((DECK_SIZE, 52))
    for (number) in cards:
        state[number-1] = 1.
    state = state.reshape(DECK_SIZE*52)  # unwrap into a long vector
    return state

################################################################################
################################################################################
################################################################################

# Reference code ANNs.ipynb from the in class example provided by Professor Katz
################################################################################
# This code is not modified
class Linear(tr.nn.Module):
    def __init__(self, in_features, out_features):
        super(Linear, self).__init__()
        self.weight = tr.randn(in_features, out_features, requires_grad=True)
        self.bias = tr.randn(1, out_features, requires_grad=True)

    def parameters(self):
        return [self.weight, self.bias]

    def forward(self, x):
        return tr.mm(x, self.weight) + self.bias

################################################################################
################################################################################
################################################################################
if __name__ == '__main__':

    print("This a simulation of BlackJack with the baseline ai that has random behavior.")
    print("please enter the number of simulations you would like to run with appropriate deck_size")
    rounds = int(input())

    DECK_SIZE = int((rounds * 16) / 52)
    print("The appropriate deck size is: " + str(DECK_SIZE))

    wins = 0
    roundCount = 0
    remaining_cards = cards(DECK_SIZE)

    data = []  # (player_hand, win/loss) data set for the NN

    while(rounds > 0):

        print("\n*************************")
        print("iteration " + str(roundCount) + ":")
        player_hand = []
        dealer_hand = []
        player_win = False

        player_win, player_hand, remaining_cards = simulationOneGame(
            player_hand, dealer_hand, remaining_cards)

        if player_win:
            wins += 1
            hand = [i.value() for i in player_hand]
            item = hand, 1.  # winning hand
            data.append(item)
        else:
            hand = [i.value() for i in player_hand]
            item = hand, 0.  # losing hand
            data.append(item)
        roundCount += 1
        rounds -= 1

    print("You won " + str(wins) + " out of " + str(roundCount) + " games.")
    print("Win rate is " + str(wins/roundCount))
    print("*************************")
    print("*************************\n")

    # Reference code ANNs.ipynb from the in class example provided by Professor Katz
    ################################################################################
    # This code is slightly modified
    inputs = tr.stack([state_tensor(hand, DECK_SIZE) for (hand, _) in data])
    targets = tr.tensor([score for (_, score) in data]).reshape(-1, 1)

    inputsx = int(inputs.shape[1])
    inputsy = int(inputs.shape[0])

    targetsx = int(targets.shape[0])
    targetsy = int(targets.shape[1])

    cardnet = tr.nn.Sequential(
        tr.nn.Linear(inputsx, inputsy),
        tr.nn.Sigmoid(),
        tr.nn.Linear(targetsx, targetsy)
    )

    print("please input the learning rate")
    learning_rate = float(input())

    # Stochastic gradient descent optimizer with learning rate of 0.01
    sgd = tr.optim.SGD(cardnet.parameters(), lr=learning_rate)

    learning_curve = []

    for epoch in range(1000):
        # Run the training step
        sgd.zero_grad()
        output = cardnet(inputs)
        loss = tr.nn.functional.mse_loss(
            output, targets)  # mean squared error loss
        loss.backward()
        sgd.step()

        # Compute the loss
        learning_curve.append(loss.item())

        if epoch % 100 == 0:
            print("Epoch: {}\tLoss: {}".format(epoch, loss.item()))
################################################################################
################################################################################
################################################################################
    precicted_output = [float(i) for i in output]

    f = open("output.txt", "w")
    for i in range(len(precicted_output)):
        f.write(str(precicted_output[i]) + "\n")

    f.close()
    
# Reference code ANNs.ipynb from the in class example provided by Professor Katz
################################################################################
# This code is not modified

    pt.plot(learning_curve)
    pt.xlabel("Gradient descent steps")
    pt.ylabel("Batch Loss")
    pt.show()
################################################################################
################################################################################
################################################################################
