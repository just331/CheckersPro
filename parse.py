# Imports
import pandas as pd
import numpy as np
import re

# Pull in data
raw_txt = open("raw.txt","r+")

# Part of understanding the file section and the board view are taken from the explanation in the dataset's repo
# Understanding the file:
# Example:
#   [Event "Manchester 1841"]
#   [Date "1841-??-??"]
#   [Black "Moorhead, W."]
#   [White "Wyllie, J."]
#   [Site "Manchester"]
#   [Result "0-1"]
#   1. 11-15 24-20 2. 8-11 28-24 3. 9-13 22-18 4. 15x22 25x18 5. 4-8 26-22 6. 10-14
#   18x9 7. 5x 14 22-18 8. 1-5 18x9 9. 5x14 29-25 10. 11-15 24-19 11. 15x24 25-22 12.
#   24-28 22-18 13. 6-9 27-24 14. 8-11 24-19 15. 7-10 20-16 16. 11x20 18-15 17. 2-6
#   15-11 18. 12-16 19x12 19. 10-15 11-8 20. 15-18 21-17 21. 13x22 30-26 22. 18x27
#   26x17x10x1 0-1

# #-# is a move from one cell to another
# #x# is jumping a piece from one cell to another
# The last pair is the results repeated and not a move -> '0-1'

# Board view:
#          32  31  30  29
#        28  27  26  25
#          24  23  22  21
#       20  19  18  17
#         16  15  14  13
#        12  11  10  09
#          08  07  06  05
#       04  03  02  01

# Understanding the game:
# Black always goes first - black is placed on the bottom three rows of this board
# A piece must make a jump if it can, and multiple jumps are allowed (forced)

def getGames(raw_txt):
    gameList = []
    tempString = ''
    for line in raw_txt:
        if line != "\n":
            tempString = tempString + line
        else:
            gameList.append(tempString)
            tempString = ''
    return gameList

def parseMoves(moves):
    # moves is a multi-line string. Need to standardize the string where there are only moves separated by a space
    moves = re.sub(r'\n|\t|\r', ' ', moves) # Removes all new lines and tabs
    moves = re.sub(r'\d*\.', ' ', moves)    # Removes the turn number
    moves = re.sub(r'\s*1-0\s*$', '', moves)       # Removes Score
    moves = re.sub(r'\s*0-1\s*$', '', moves)       # Removes Score
    moves = re.sub(r'\s*1/2-1/2\s*$', '', moves)   # Removes Score
    moves = re.sub(r' +', ' ', moves)       # Replaces multi-spaces with a single space
    moves = re.sub(r'^ +', '', moves)       # Removes leading spaces
    moves = re.sub(r' +$', '', moves)       # Removes trailing spaces

    movesList = moves.split(' ')            # Since the moves are now standardized we can split them on a space
    blackMoves = []
    whiteMoves = []
    for i in range(0, len(movesList)):
        if i % 2 == 0:  # Even turn and therefore Black's turn
            blackMoves.append(movesList[i])
        else:  # Odd turn and therefore White's turn
            whiteMoves.append(movesList[i])
    return [blackMoves, whiteMoves]


def parseGames(gameList):
    parsedGames = []
    for game in gameList:  # Cycle through the games
        lines = game.split("\n")  # text blob back into lines
        moves = ''  # Place holder string for the moves
        getMoves = False
        for i in range(0,len(lines)):
            if re.search(r'Result',lines[i]):  # Get winner
                if re.search(r'1-0',lines[i]):
                    winner = "Black"
                elif re.search(r'0-1',lines[i]):
                    winner = "White"
                else:
                    winner = "Draw"
            elif lines[i][0:2]=='1.':  # Start collecting moves
                getMoves = True
            if getMoves == True:
                moves = moves + " " + lines[i] + " "
        masterMoves = parseMoves(moves)
        blackMoves = masterMoves[0]
        whiteMoves = masterMoves[1]
        gameInfo = [blackMoves, whiteMoves, winner]
        parsedGames.append(gameInfo)
    return parsedGames

games = getGames(raw_txt)

parseGamesList = parseGames(games)

games_df = pd.DataFrame.from_records(parseGamesList)
games_df.columns=['BlackMoves','WhiteMoves','Winner']

print(games_df.shape)
print(games_df.head(1))

games_df.to_pickle('Pickles/games_df.p')

