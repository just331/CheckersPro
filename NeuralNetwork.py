'''
Neural Network:
    Board can be represented by an 8x4 matrix
    Each cell can have the value of [-3, -1.5, 0, 1, +1.5]
Output (two ideas):
    A single move (what piece to move and to what spot)
    Same format as input (with a single change to 1 cell)
Training:
    Need to convert the current dataframe
    (state, move) - (state, move) - (state, move) … winner
    We are providing the state and the move taken. It can then learn from this?
'''

import pandas as pd
import numpy as np

# Read in the parsed data frame
games_df = pd.read_pickle('Pickles/games_df.p')

value_dic = {"ownMan": 1, "ownKing": 1.5, "enemyMan": -1.5, "enemyKing": -3}
gameBoard = np.zeros(32)  # By default the board is an empty 1x32 matrix ... see parse.py for board example

def startGame(color):
    returnBoard = gameBoard.copy()
    if color.lower() == "white":
        returnBoard[20:32] = value_dic["ownMan"]
        returnBoard[0:12] = value_dic["enemyMan"]
    elif color.lower() == "black":
        returnBoard[20:32] = value_dic["enemyMan"]
        returnBoard[0:12] = value_dic["ownMan"]

    return returnBoard


# Part 1: Train the Neural Network using black moves
def findBlackValue():

    return 1

# Part 2: Train the Neural Network using white moves
def findWhiteValue():

    return 1

def prepareGame():
    '''
    Takes in a row from games_df as well as what color
    '''
    return 1

white = startGame("white")

black = startGame("black")