#import pandas as pd
import numpy as np
import random

# Board view:
#       --31--30--29--28
#       27--26--25--24--
#       --23--22--21--20
#       19--18--17--16--
#       --15--14--13--12
#       11--10--09--08--
#       --07--06--05--04
#       03--02--01--00--

value_dic = {"ownMan": 1, "ownKing": 1.5, "enemyMan": -1.5, "enemyKing": -3}
gameBoard = np.zeros(32)  # By default the board is an empty 1x32 matrix ... see parse.py for board example
# Not a fan of this method but for now it'll work. I think all moves are accounted for
blackMoves = {0: [4, 5], 1: [5, 6], 2: [6, 7], 3: [7], 4: [8], 5: [8, 9], 6: [9, 10], 7: [10, 11], 8: [12, 13],
              9: [13, 14], 10: [14, 15], 11: [15], 12: [16], 13: [16, 17], 14: [17, 18], 15: [18, 19], 16: [20, 21],
              17: [21, 22], 18: [22, 23], 19: [23], 20: [24], 21: [24, 25], 22: [25, 26], 23: [26, 27], 24: [28, 29],
              25: [29, 30], 26: [30, 31], 27: [31]}

whiteMoves = {4: [0], 5: [0, 1], 6: [1, 2], 7: [2, 3], 8: [4, 5], 9: [5, 6], 10: [6, 7], 11: [7], 12: [8],
              13: [8, 9], 14: [9, 10], 15: [10, 11], 16: [12, 13], 17: [13, 14], 18: [14, 15], 19: [15], 20: [16],
              21: [16, 17], 22: [17, 18], 23: [18, 19], 24: [20, 21], 25: [21, 22], 26: [22, 23], 27: [23], 28: [24],
              29: [24, 25], 30: [25, 26], 31: [26, 27]}

kingMoves = {0: [4, 5], 1: [5, 6], 2: [6, 7], 3: [7], 4: [0, 8], 5: [0, 1, 8, 9], 6: [1, 2, 9, 10], 7: [2, 3, 10, 11],
             8: [4, 5, 12, 13], 9: [5, 6, 13, 14], 10: [6, 7, 14, 15], 11: [7, 15], 12: [8, 16], 13: [8, 9, 16, 17],
             14: [9, 10, 17, 18], 15: [10, 11, 18, 19], 16: [12, 13, 20, 21], 17: [13, 14, 21, 22],
             18: [14, 15, 22, 23], 19: [15, 23], 20: [16, 24], 21: [16, 17, 24, 25], 22: [17, 18, 25, 26],
             23: [18, 19, 26, 27], 24: [20, 21, 28, 29], 25: [21, 22, 29, 30], 26: [22, 23, 30, 31], 27: [23, 31],
             28: [24], 29: [24, 25], 30: [25, 26], 31: [26, 27]}

edgeCells = [0, 1, 2, 3, 4, 11, 12, 19, 20, 27, 28, 29, 30, 31]
blackEndZone = [0, 1, 2, 3]  # White piece turns to king when it reaches the end zone.
whiteEndZone = [28, 29, 30, 31]  # Black piece turns to king when it reaches the end zone.


def startGame(color):  # status: Done
    returnBoard = gameBoard.copy()

    if color.lower() == "white":
        returnBoard[20:32] = value_dic["ownMan"]
        returnBoard[0:12] = value_dic["enemyMan"]
    elif color.lower() == "black":
        returnBoard[20:32] = value_dic["enemyMan"]
        returnBoard[0:12] = value_dic["ownMan"]

    #print(returnBoard)
    return returnBoard


def printBoard(activeBoard, agentColor):  # status: Working   TODO: Upgrade to GUI
    cell_num = 0
    blank = True
    for i in range(8):
        for j in range(8):
            if blank == True:
                print("|=|", end='')
            else:
                # The section below is very gross and should be changed but I am doing this for now
                value = activeBoard[31-cell_num]
                if agentColor.lower() == 'white':
                    if value == value_dic["ownMan"]:
                        value_nm = 'W'
                    elif value == value_dic["ownKing"]:
                        value_nm = 'WK'
                    elif value == value_dic["enemyMan"]:
                        value_nm = 'B'
                    elif value == value_dic["enemyKing"]:
                        value_nm = 'BK'
                    else:
                        value_nm = "-"
                elif agentColor.lower() == 'black':
                    if value == value_dic["ownMan"]:
                        value_nm = 'B'
                    elif value == value_dic["ownKing"]:
                        value_nm = 'BK'
                    elif value == value_dic["enemyMan"]:
                        value_nm = 'W'
                    elif value == value_dic["enemyKing"]:
                        value_nm = 'WK'
                    else:
                        value_nm = "-"
                print("|" + str(value_nm) + "|", end='')
                cell_num += 1
            blank = not blank
        blank = not blank
        print("\n")

'''
def checkForJumps(activeBoard, activePlayer, activeColor):  # Need to work on this
    # A player MUST make a jump if they can (and double jumps)
    
    # Step 1) Cycle through each cell. Focus only on the active player's pieces
    # Step 2) For each of the active player's pieces, check if one of their moves brings them to an occupied enemy cell 
    # Step 3) Using the jump pattern, determine if jumping the occupied cell would bring the piece to an empty cell 
    # Note: If occupied cell is in a "no jump" cell then don't bother looking  
    # If a piece makes a jump look again ONLY for that piece (double jump)
    # Once that piece is done jumping you can stop looking

    # Step 1) Figure out how to read the board
    if activePlayer == 'agent':
      man = value_dic["ownMan"]
      king = value_dic["ownKing"]
      e_man = value_dic["enemyMan"]
      e_king = value_dic["enemyKing"]
    else:  # Player
      man = value_dic["enemyMan"]
      king = value_dic["enemyKing"]
      e_man = value_dic["ownMan"]
      e_king = value_dic["ownKing"]
    

    # Step 2) Cycle through the board and look for friendly pieces
    for cellNum in range(len(activeBoard)):
      # Found a friendly man, analyze their moves
      if activeBoard[cellNum] == man:
        if activeColor.lower() == 'black':
          possibleMoves = blackMoves[cellNum]
        else:
          possibleMoves = whiteMoves[cellNum]
      # Found a friendly king, analyze their moves
      elif activeBoard[cellNum] == king:
        print("do stuff")

    print("uwu")
'''

def chooseMove(activeBoard, agentColor):  #status: Done
    possible_moves = []
    for i in range(len(activeBoard)):
        if activeBoard[i] == value_dic["ownMan"]:
            if agentColor == 'black':
                tempSpots = blackMoves[i]
            elif agentColor == 'white':
                tempSpots = whiteMoves[i]
            for spot in tempSpots:
                if activeBoard[spot] == 0:  # Spot is not occupied
                    possible_moves.append([i, spot, value_dic["ownMan"]])  # Old spot, New spot, piece
        elif activeBoard[i] == value_dic["ownKing"]:
            tempSpots = kingMoves[i]
            for spot in tempSpots:
                if activeBoard[spot] == 0:  # Spot is not occupied
                    possible_moves.append([i, spot, value_dic["ownKing"]])  # Old spot, New spot, piece
    randomMove = random.choice(possible_moves)
    activeBoard[randomMove[0]] = 0
    activeBoard[randomMove[1]] = randomMove[2]

    return activeBoard


def checkMove(activeBoard, u_move, playerColor):  #status: Done
    # Check number 1) Is the spot occupied
    for i in range(len(u_move)):
        u_move[i] = int(u_move[i])
    if activeBoard[u_move[1]] != 0:
        return False
    # Check number 2) Is this a legal move
    if activeBoard[u_move[0]] == value_dic["enemyMan"]:
        if playerColor == 'b':
            if u_move[1] not in blackMoves[u_move[0]]:
                return False
        elif playerColor == 'w':
            if u_move[1] not in whiteMoves[u_move[0]]:
                return False
    elif activeBoard[u_move[0] == value_dic["enemyKing"]]:
        if u_move[1] not in kingMoves[u_move[0]]:
            return False
    # Passed both checks
    return True


def checkForKing(activeBoard, agentColor):  #status: Done
  # Cycle through all cells on the board
  for cellNum in range(len(activeBoard)):
    # If we find a normal 'man' piece that belongs to the agent
    if activeBoard[cellNum] == value_dic["ownMan"]:
      # Check if this piece is in the end zone
      if agentColor == "black":
        if cellNum in whiteEndZone:
          # If so, King it
          activeBoard[cellNum] = value_dic["ownKing"]
      else:
        if cellNum in blackEndZone:
          activeBoard[cellNum] = value_dic["ownKing"]
    # Found a player's man
    elif activeBoard[cellNum] == value_dic["enemyMan"]:
        # Check if this piece is in the end zone
      if agentColor == "black":
        if cellNum in blackEndZone:
          # If so, King it
          activeBoard[cellNum] = value_dic["enemyKing"]
      else:
        if cellNum in blackEndZone:
          activeBoard[cellNum] = value_dic["enemyKing"]       

  return activeBoard   


def CheckGameOver(activeBoard):  #status: Done

    agentWin = True
    playerWin = True
    for cellNum in range(len(activeBoard)):
      # If a player piece is found the agent did not win
      if activeBoard[cellNum] == value_dic["enemyMan"] or activeBoard[cellNum] == value_dic["enemyKing"]:
        agentWin = False
      elif activeBoard[cellNum] == value_dic["ownMan"] or activeBoard[cellNum] == value_dic["ownKing"]:
        playerWin = False
    
    if agentWin:
      return True, "Sorry you lost :("
    elif playerWin:
      return True, "You Won!!"
    else:
      return False, "N/A"


def main():
    '''
    TODO:
        Create a GUI instead of inline
        Streamline the available moves
        Create CheckForJumps function
        Create CheckForKing using the EndZone lists at the top of the code
        create CheckForGameEnd see if only one color is left
        Currently I the agent always goes first,
            This needs to be changed so that whoever is black goes first
    '''
    player_color = input("What Color do you want to be? (type 'b' or 'w')")
    if player_color == "b":
        agentColor = 'white'
        activeGame = startGame(agentColor)
    # Using else instead of elif in case the user enters something other than 'b' or 'w'
    else:
        agentColor = 'black'
        activeGame = startGame(agentColor)

    # TODO: Agent is always going first, but Black should only go first
    while(True):
        # Show the board
        printBoard(activeGame, agentColor)
        # Let agent go
        # Check for jumps and force them
        activeGame = checkForKing(activeGame, agentColor)  # See if these jumps resulted in a king
          # TODO: Check for jumps
        # Let agent take a move ONLY IF THERE WAS NO JUMPS: NEED LOGIC FOR THIS
        activeGame = chooseMove(activeGame,agentColor)
        activeGame = checkForKing(activeGame, agentColor)  # See if the move resulted in a king
        # Print board
        print("---------------------------------------")
        printBoard(activeGame, agentColor)
        print("---------------------------------------")
        # Check for jumps
        # Let player take move
        u_move = input("Enter start cell and end cell: '# #'")
        #FOR TESTTING-----------------------------------------------------------------
        if u_move == 'end':  # Ends the game
          break
        elif u_move == 'delete agent':
          for cellNum in range(len(activeGame)):
            if activeGame[cellNum] == value_dic["ownMan"] or activeGame[cellNum] == value_dic["ownKing"]:
              activeGame[cellNum] = 0
          printBoard(activeGame, agentColor)
          gameOver, message = CheckGameOver(activeGame)
          if gameOver:
            print(message)
            break
          u_move = input("Teleport to: '# #'")
          user_move = u_move.split(" ")
          for i in range(len(user_move)):
            user_move[i] = int(user_move[i])
          temp_value = activeGame[user_move[0]]
          activeGame[user_move[0]] = 0
          activeGame[user_move[1]] = temp_value
          activeGame = checkForKing(activeGame, agentColor)
          printBoard(activeGame, agentColor)
          break
        #-----------------------------------------------------------------------------
        user_move = u_move.split(" ")
        validMove = False  # Assume the move is invalid
        # Make sure move is valid
        while(not validMove):
            validMove = checkMove(activeGame, user_move, player_color)  # Check if the move is valid
            if not validMove:
                u_move = input("You did a bad job...Enter start cell and end cell: '# #'")
                user_move = u_move.split(" ")
        # Convert move numbers (strings) as actual ints
        for i in range(len(user_move)):
            user_move[i] = int(user_move[i])
        # Update board with user's move  -- The section below COULD be moved into a function later
        temp_value = activeGame[user_move[0]]  # Collect the piece info at the old cell
        activeGame[user_move[0]] = 0           # Remove the piece from the old cell
        activeGame[user_move[1]] = temp_value  # Move the piece to the new cell
        activeGame = checkForKing(activeGame, agentColor)  # See if this move resulted in a king
        # Print board
        printBoard(activeGame, agentColor)
        print("---------------------------------------")
        # See if game is over
        gameOver, message = CheckGameOver(activeGame)
        if gameOver:
          print(message)
          break
