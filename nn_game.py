import numpy as np
import game
import shoe
import cards
import FCFFNet


def nn_eval(outputs):

    for (number) in outputs:
        if number >= 0.52:
            return 1
        else:
            return 0


def nn_play_turn(player_hand, dealer_hand, remaining_cards, predicted_outputs):
    player_score = FCFFNet.sum(player_hand)
    for i in predicted_outputs:
        if i >= 0.52:
            player_hand.append(remaining_cards.draw())
            player_score = FCFFNet.sum(player_hand)
            print("Player hand: " + game.show_hand(player_hand))
            print("Player score: " + str(player_score))
        else:
            break

    player_busted = game.busted(player_hand)
    if(player_busted):
        print("Player busted, dealer wins")
        return False, remaining_cards

    dealer_busted, dealer_hand, remaining_cards = FCFFNet.dealer(
        dealer_hand, remaining_cards)
    if(dealer_busted == False):
        if(player_score > FCFFNet.sum(dealer_hand)):
            print("Player wins")
            return True, remaining_cards
        elif(player_score < FCFFNet.sum(dealer_hand)):
            print("Dealer wins")
            return False, remaining_cards
        else:
            print("Draw")
            return True, remaining_cards

    return dealer_busted, remaining_cards


def nn_simulation_OneGame(player_hand, dealer_hand, remaining_cards, predicted_outputs):
    game_state = game.draw_cards(player_hand, dealer_hand, remaining_cards)

    player_hand = game_state[0]
    dealer_hand = game_state[1]
    remaining_cards = game_state[2]

    player_score = FCFFNet.sum(player_hand)
    dealer_score = FCFFNet.sum(dealer_hand)

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

        player_win, remaining_cards = nn_play_turn(
            player_hand, dealer_hand, remaining_cards, predicted_outputs)
        if(player_win):
            print()
            print("Player score: " + str(FCFFNet.sum(player_hand)) +
                  " Dealer score: " + str(FCFFNet.sum(dealer_hand)))
            return (True, player_hand, remaining_cards)
        return player_win, player_hand, remaining_cards


if __name__ == '__main__':

    print("This a simulation of BlackJack with the baseline ai that has random behavior.")
    print("please enter the number of simulations you would like to run with appropriate deck_size")
    rounds = int(input())

    DECK_SIZE = int((rounds * 16) / 52)
    print("The appropriate deck size is: " + str(DECK_SIZE))

    wins = 0
    roundCount = 0
    remaining_cards = FCFFNet.cards(DECK_SIZE)

    f = open("output.txt", "r")
    predicted_outputs = []

    while(f.readline()) != "":
        f1 = f.readline()
        f2 = f1[:3]
        predicted_outputs.append(float(f2))

    f.close()

    while(rounds > 0):

        print("\n*************************")
        print("iteration " + str(roundCount) + ":")
        player_hand = []
        dealer_hand = []
        player_win = False

        player_win, player_hand, remaining_cards = nn_simulation_OneGame(
            player_hand, dealer_hand, remaining_cards, predicted_outputs)

        if player_win:
            wins += 1

        roundCount += 1
        rounds -= 1

    print("You won " + str(wins) + " out of " + str(roundCount) + " games.")
    print("Win rate is " + str(wins/roundCount))
    print("*************************")
    print("*************************\n")
