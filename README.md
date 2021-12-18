# FiftyFive

FiftyFive is an AI project for CIS667. Instead of aiming for 21 like blackjack, Fifty raises the number to 55 so to experiment with deeper search tree.

# Contributor

- Ben Smrtic
- Minyen Chiang

# Dependencies

- Numpy
- Pytorch

# How to run the fiftyFive domain

- In terminal run, "python game.py" for a one round game, this is just to demonstrate the domain implementation
- For the naive ai, "python baselineAI.py" and follow the prompts
- For expectimaxAI, "python expectimaxAI.py" and follow the prompts
- For the connected feed-forward neural network section:
  - First, run "python FCFFNet.py" to get the output.txt, which we will need for the nn_game.py execution
  - Second, run "nn_game.py" and follow the prompts

# Experiments

- The prompts will ask the user for the number of rounds in most of the implementations
- In FCCNet.py, the user can also adjust the learning rate when prompted

# Reference

- In this project, our nn implementation is based on the ANNs.ipynb provided by Professor Katz as class example.
