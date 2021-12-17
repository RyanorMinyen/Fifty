import numpy as np
import random
import game


def ai_play_turn(player_hand, dealer_hand, shoe) -> tuple:

    print("Hit or stay?")
    choice = random.choice(["hit", "stay"])
    player_busted = game.busted(player_hand)

    while (player_busted == False and choice == "hit"):
        player_hand.append(shoe.draw())
        print("Player hand: " + game.show_hand(player_hand))
        print("Player score: " + str(game.score(player_hand)))
        player_busted = game.busted(player_hand)
        if(player_busted):
            print("Player busted, dealer wins")
            return (True, (player_hand, dealer_hand, shoe))
        print("Hit or stay?")
        choice = random.choice(["hit", "stay"])

    if choice == "stay":
        while game.score(dealer_hand) < game.score(player_hand):
            game.dealer_turn(player_hand, dealer_hand, shoe)

        if (game.compare_hands(player_hand, dealer_hand)) == 1 and game.busted(player_hand) == False:
            print("Player wins!")
        elif (game.compare_hands(player_hand, dealer_hand)) == -1 and game.busted(dealer_hand) == False:
            print("Dealer wins!")
        elif(game.compare_hands(player_hand, dealer_hand) == 0):
            print("Draw!")
        else:
            print()

    return player_hand, dealer_hand, shoe


if __name__ == '__main__':

    AIplayer_busted = False
    dealer_busted = False

    print("This a simulation of BlackJack with the baseline ai that has random behavior.\n")
    print("please enter the number of simulations you would like to run: either 50 or 100")
    rounds = int(input())
    if rounds == 50:
        print("Running 50 simulations\n")
        DECK_SIZE = 40
    elif rounds == 100:
        DECK_SIZE = 80
        print("Running 100 simulations\n")

    wins = 0
    roundCount = 0

    game_state = game.initial_state(DECK_SIZE)

    while(rounds > 0 and game_state[2].count() > 0):

        game_state = game.draw_cards(
            game_state[0], game_state[1], game_state[2])

        player_hand = game_state[0]
        dealer_hand = game_state[1]
        remaining_cards = game_state[2]

        player_score = game.score(player_hand)
        dealer_score = game.score(dealer_hand)

        # evaluate the first five cards
        if(game.FiftyFive(player_score, dealer_score)):

            if(game.score(player_hand) > game.score(dealer_hand)):
                wins += 1
        else:

            game_over = ai_play_turn(
                game_state[0], game_state[1], game_state[2])[0]
            if(game.score(player_hand) > game.score(dealer_hand)):
                wins += 1
            print()
            print("Player score: " + str(game.score(player_hand)) +
                  " Dealer score: " + str(game.score(dealer_hand)))

        roundCount += 1
        rounds -= 1

    print("You won " + str(wins) + " out of " + str(roundCount) + " games.")
    print("Win rate is " + str(wins/roundCount))
