import numpy as np
import random
import game
import shoe
import cards


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
            return (True, remaining_cards)
        elif(player_score == 55):
            print("Player wins")
            return (True, remaining_cards)
        else:
            print("Dealer wins")
            return (False, remaining_cards)
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
            return (True, remaining_cards)
        return player_win, remaining_cards


if __name__ == '__main__':

    print("This a simulation of BlackJack with the baseline ai that has random behavior.")
    print("please enter the number of simulations you would like to run:")
    rounds = int(input())
    DECK_SIZE = int((rounds * 16) / 52)
    print("The appropriate deck size is: " + str(DECK_SIZE))

    wins = 0
    roundCount = 0

    remaining_cards = cards(DECK_SIZE)

    while(rounds > 0):

        print("\n*************************")
        print("iteration " + str(roundCount) + ":")
        player_hand = []
        dealer_hand = []
        player_win = False

        player_win, remaining_cards = simulationOneGame(
            player_hand, dealer_hand, remaining_cards)

        if player_win:
            wins += 1
        roundCount += 1
        rounds -= 1

    print("You won " + str(wins) + " out of " + str(roundCount) + " games.")
    print("Win rate is " + str(wins/roundCount))
