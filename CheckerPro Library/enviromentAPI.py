"""
This Document will act as an 'API' similar to what open AI gym offers
Bellow are the following calls that can be made:

Create Environment:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
    Output: An empty 1x32 np.array
                 Board view:
                   --31--30--29--28
                   27--26--25--24--
                   --23--22--21--20
                   19--18--17--16--
                   --15--14--13--12
                   11--10--09--08--
                   --07--06--05--04
                   03--02--01--00--

Create Random Environment:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
           King probability = a float value in the range of [0,1]
    Output: A random (legal) board state represented by a 1x32 np.array (see image above)

Get Jumps: *** Verify ***
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
    Output: A list of lists with each sub list being the start square, end square, piece removed, piece moved
            AND a bool value that says if this jump leads to another jump - Double Jump
        Ex. [0, 9, -3.0, 1.0], False
        This action uses a 'man' piece in square 0 to jump an enemy king piece in square 5 and land at square 9
        Additionally, there is no double jump available

Get Moves:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
           Game Board = The 1x32 np.array generated upon creation with any number of legal moves made prior
    Output: A list of lists with each sub list being the start square, end square, and the piece to be moved
        Ex. [0, 5, 1.0]
        This action moves a 'man' piece from square 0 to square 5 (see image above)

Make Jump:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
           Game Board = The 1x32 np.array generated upon creation with any number of legal moves made prior
           Jump Action = A jump list 'object' produced by Get Jumps (see example)
    Output: The updated 1x32 np.array

Make Move:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
           Game Board = The 1x32 np.array generated upon creation with any number of legal moves made prior
           Move Action = A move list 'object' produced by Get Moves (see example)
    Output: The updated 1x32 np.array

Take Step:
    Input: Agent's Color = 'w'|'W' or 'b'|'B'
           Game Board = The 1x32 np.array generated upon creation with any number of legal moves made prior
    Output: The updated 1x32 np.array (after the opponent made a move)
"""

# Imports
import numpy as np
import random

# Changeable Values
value_dic = {"ownMan": 1, "ownKing": 1.5, "enemyMan": -1.5, "enemyKing": -3}

# Hard Coded Logic
gameBoard = np.zeros(32)   # Empty board

# Unfortunately, we have not been able to come up with a more sophisticated representation of valid moves
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

# Important cells.
edgeCells = [0, 1, 2, 3, 4, 11, 12, 19, 20, 27, 28, 29, 30, 31]
blackEndZone = [0, 1, 2, 3]      # White piece turns to king when it reaches the end zone.
whiteEndZone = [28, 29, 30, 31]  # Black piece turns to king when it reaches the end zone.

# Helper Functions ----------
def printBoard(activeBoard, agentColor):  # This will no longer be needed
    cell_num = 0
    blank = True
    for i in range(8):
        for j in range(8):
            if blank:
                print("|=|", end='')
            else:
                # The section below is very gross and should be changed but I am doing this for now
                value = activeBoard[31 - cell_num]
                if agentColor.lower() == 'w':
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
                elif agentColor.lower() == 'b':
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


def print_dict(a_dict):
    key_list = sorted(a_dict.keys())
    for key in key_list:
        print(key, ':', a_dict[key])


def checkForKing(inputState, color):
    color = color.lower()  # Reducing the number of times I have to write that
    # Cycle through all cells on the board

    board = inputState.copy()

    for cellNum in range(len(board)):
        # If we find a normal 'man' piece that belongs to the agent
        if board[cellNum] == value_dic["ownMan"]:
            # Check if this piece is in the end zone
            if color == "b" and cellNum in whiteEndZone:
                # If so, King it
                board[cellNum] = value_dic["ownKing"]
            elif color == "w" and cellNum in blackEndZone:
                # If so, King it
                board[cellNum] = value_dic["ownKing"]
        # Found an opponent's man
        elif board[cellNum] == value_dic["enemyMan"]:
            # Check if this piece is in the end zone
            if color == "b" and cellNum in blackEndZone:
                # If so, King it
                board[cellNum] = value_dic["enemyKing"]
            elif color == "w" and cellNum in whiteEndZone:
                # If so, King it
                board[cellNum] = value_dic["enemyKing"]

    return board


def landSpace(cellNum, p_Target):
    # This is kinda hard to explain but is needed for determining legal jumps
    target_3 = [5, 6, 7, 13, 14, 15, 21, 22, 23]
    target_5 = [8, 9, 10, 16, 17, 18, 24, 25, 26, 31]

    jumpDif = abs(cellNum - p_Target)
    if cellNum - p_Target > 0:
        jumpDifSign = "-"
    else:
        jumpDifSign = "+"
    # There are three possible jump patterns
    if jumpDif == 3 or jumpDif == 5:
        checkNum = 4
    elif jumpDif == 4:
        if p_Target in target_3:
            if jumpDifSign == "+":
                checkNum = 3
            else:
                checkNum = 5
        elif p_Target in target_5:
            if jumpDifSign == "+":
                checkNum = 5
            else:
                checkNum = 3
    if jumpDifSign == "-":
        checkNum = checkNum * -1
    landSpace = p_Target + checkNum

    return landSpace


# API Functions -------------


def createEnviroment(color):
    # NOTE: This program places white at the TOP of the board
    # To change this, flip the current function as well as the white and black move dictionaries

    returnBoard = gameBoard.copy()  # Make an empty game board

    if color.lower() == "w":
        returnBoard[20:32] = value_dic["ownMan"]
        returnBoard[0:12] = value_dic["enemyMan"]
    else:  # Black
        returnBoard[20:32] = value_dic["enemyMan"]
        returnBoard[0:12] = value_dic["ownMan"]

    return returnBoard


#  Note: There could be a scenario where the random board is already in an end game state
def createRandomEnviroment(color, kingPob):

    numAgent, numPlayer = 0, 0  # NOTE: There can only be a maximum of 12 pieces for either color

    returnBoard = gameBoard.copy()  # Make an empty game board

    indexes = np.arange(0, 32)  # This represents all of the squares
    np.random.shuffle(indexes)  # Randomly shuffle the squares as to not favor one side

    for i in indexes:
        square = random.choice([0, 1, 2])  # 0 = Empty, 1 = Agent, 2 = opponent
        if square == 1 and numAgent < 13:
            # Step 1) Check if we are trying to place a piece in a position where it must be a king
            if color.lower() == "w" and i in blackEndZone:
                returnBoard[i] = value_dic["ownKing"]
            elif color.lower() == "b" and i in whiteEndZone:
                returnBoard[i] = value_dic["ownKing"]
            else:
                # Step 2) Check if we should place a king.
                if random.random() < kingPob:
                    returnBoard[i] = value_dic["ownKing"]
                else:  # Just place a normal piece
                    returnBoard[i] = value_dic["ownMan"]
            numAgent += 1
        elif square == 2 and numPlayer < 13:
            # Step 1) Check if we are trying to place a piece in a position where it must be a king
            if color.lower() == "w" and i in whiteEndZone:    # Inverted because the agent is the opposite color
                returnBoard[i] = value_dic["enemyKing"]
            elif color.lower() == "b" and i in blackEndZone:  # Inverted because the agent is the opposite color
                returnBoard[i] = value_dic["enemyKing"]
            else:
                # Step 2) Check if we should place a king.
                if random.random() < kingPob:
                    returnBoard[i] = value_dic["enemyKing"]
                else:  # Just place a normal piece
                    returnBoard[i] = value_dic["enemyMan"]
            numPlayer += 1
        # Else: Place no piece (stay 0)

    return returnBoard


def getJumps(board, color, player="Agent"):
    availableJumps = []  # Return List
    if player == "Agent":
        # Cycle through the board
        for cellNum in range(len(board)):
            # Current piece is a friendly man ... Check for jumps
            if board[cellNum] == value_dic["ownMan"]:
                # Need to see what possible jumps there could be
                if color == "b":
                    possibleJumps = blackMoves[cellNum]
                else:
                    possibleJumps = whiteMoves[cellNum]
                # Cycle through the cells that this piece could move to
                for p_Target in possibleJumps:
                    # See if one of the cells contains an enemy piece and that piece is not on an edge cell
                    if (board[p_Target] == value_dic["enemyMan"] or board[p_Target] == value_dic["enemyKing"]) \
                            and (p_Target not in edgeCells):
                        # There is a bordering enemy piece, see if it can be jumped
                        possibleLand = landSpace(cellNum, p_Target)
                        if board[possibleLand] == 0:  # Land spot is empty
                            value = value_dic["ownMan"]
                            old_square, remove, new_squre = cellNum, p_Target, possibleLand
                            availableJumps.append([old_square, new_squre, remove, value])
            # Current piece is a friendly king ... Check for jumps
            elif board[cellNum] == value_dic["ownKing"]:
                # Checking the moves for the current piece
                possibleJumps = kingMoves[cellNum]
                # Cycle through the cells that this piece could move to
                for p_Target in possibleJumps:
                    # See if one of the cells contains an enemy piece and that piece is not on an edge cell
                    if (board[p_Target] == value_dic["enemyMan"] or board[p_Target] == value_dic["enemyKing"]) \
                            and (p_Target not in edgeCells):
                        # There is a bordering enemy piece, see if it can be jumped
                        possibleLand = landSpace(cellNum, p_Target)
                        if board[possibleLand] == 0:
                            value = value_dic["ownKing"]
                            old_square, remove, new_squre = cellNum, p_Target, possibleLand
                            availableJumps.append([old_square, new_squre, remove, value])
        return availableJumps
    elif player == "Opponent":
        # Cycle through the board
        for cellNum in range(len(board)):
            # Current piece is a friendly man ... Check for jumps
            if board[cellNum] == value_dic["enemyMan"]:
                # Need to see what possible jumps there could be
                if color == "b":
                    possibleJumps = whiteMoves[cellNum]
                else:
                    possibleJumps = blackMoves[cellNum]
                # Cycle through the cells that this piece could move to
                for p_Target in possibleJumps:
                    # See if one of the cells contains an enemy piece and that piece is not on an edge cell
                    if (board[p_Target] == value_dic["ownMan"] or board[p_Target] == value_dic["ownKing"]) \
                            and (p_Target not in edgeCells):
                        # There is a bordering enemy piece, see if it can be jumped
                        possibleLand = landSpace(cellNum, p_Target)
                        if board[possibleLand] == 0:  # Land spot is empty
                            value = value_dic["enemyMan"]
                            old_square, remove, new_squre = cellNum, p_Target, possibleLand
                            availableJumps.append([old_square, new_squre, remove, value])
            # Current piece is a friendly king ... Check for jumps
            elif board[cellNum] == value_dic["enemyKing"]:
                # Checking the moves for the current piece
                possibleJumps = kingMoves[cellNum]
                # Cycle through the cells that this piece could move to
                for p_Target in possibleJumps:
                    # See if one of the cells contains an enemy piece and that piece is not on an edge cell
                    if (board[p_Target] == value_dic["ownMan"] or board[p_Target] == value_dic["ownKing"]) \
                            and (p_Target not in edgeCells):
                        # There is a bordering enemy piece, see if it can be jumped
                        possibleLand = landSpace(cellNum, p_Target)
                        if board[possibleLand] == 0:
                            value = value_dic["enemyKing"]
                            old_square, remove, new_squre = cellNum, p_Target, possibleLand
                            availableJumps.append([old_square, new_squre, remove, value])
        return availableJumps


def getMoves(board, color, player="Agent"):
    possibleMoves = []
    # We need to cycle through the current game board
    for i in range(len(board)):
        # Find the moves for the Agent
        if player == "Agent":
            if board[i] == value_dic["ownMan"]:  # 'man' belonging to the agent
                # Need to decide which move pool to use
                if color.lower() == 'w':
                    tempSpots = whiteMoves[i]
                else:  # Black
                    tempSpots = blackMoves[i]
                for spot in tempSpots:
                    if board[spot] == 0:  # Spot is not occupied
                        possibleMoves.append([i, spot, value_dic["ownMan"]])  # Old spot, New spot, piece to move
            elif board[i] == value_dic["ownKing"]:  # 'king' belonging to the agent
                tempSpots = kingMoves[i]
                for spot in tempSpots:
                    if board[spot] == 0:  # Spot is not occupied
                        possibleMoves.append([i, spot, value_dic["ownKing"]])  # Old spot, New spot, piece to move
        elif player == "Opponent":
            if board[i] == value_dic["enemyMan"]:  # 'man' belonging to the agent
                # Need to decide which move pool to use. Use the opposite color of the agent
                if color.lower() == 'w':
                    tempSpots = blackMoves[i]
                else:  # Black
                    tempSpots = whiteMoves[i]
                for spot in tempSpots:
                    if board[spot] == 0:  # Spot is not occupied
                        possibleMoves.append([i, spot, value_dic["enemyMan"]])  # Old spot, New spot, piece to move
            elif board[i] == value_dic["ownKing"]:  # 'king' belonging to the agent
                tempSpots = kingMoves[i]
                for spot in tempSpots:
                    if board[spot] == 0:  # Spot is not occupied
                        possibleMoves.append([i, spot, value_dic["enemyKing"]])  # Old spot, New spot, piece to move

    return possibleMoves


def makeJumps(inputState, color, jumpObject, player="Agent"):
    oldSpot = jumpObject[0]
    newSpot = jumpObject[1]
    remove = jumpObject[2]
    value = jumpObject[3]

    board = inputState.copy()

    # Step 1) Make the jump ... because this jump was made internally, we know it is a legal jump
    board[oldSpot] = 0
    board[newSpot] = value
    board[remove] = 0
    # Step 2) Check if the move resulted in a king and update
    board = checkForKing(board, color)
    # Step 3) Check to see if there is another move
    # Per an investigation I did, I strongly believe that the only jumps that could occur after the first jump
    # is from the piece that did the first jump
    return getJumps(board, color, player), board


def makeMoves(inputState, color, moveObject):
    oldSpot = moveObject[0]
    newSpot = moveObject[1]
    value = moveObject[2]

    board = inputState.copy()

    # Step 1) Make the move ... because this move was made internally, we know it is a legal move
    board[oldSpot] = 0
    board[newSpot] = value
    # Step 2) Check if the move resulted in a king and update
    return checkForKing(board, color)  # Returning updated board


def takeStep(board, color):
    # This is where the opponent will make a move / For training this will be a sudo-random move.
    # Step 1: Check if there is a jump and then a move
    jump = True
    actions = getJumps(board, color, player="Opponent")  # First look for a jump
    if len(actions) == 0:
        jump = False
        actions = getMoves(board, color, player="Opponent")  # If no jump, look for a move
    # Choose a random move
    action = random.choice(actions)
    # Step 2: Preform the action
    if jump:
        while len(actions) > 0:  # There is at least one jump available
            actions, board = makeJumps(board, color, action, player="Opponent")
            if len(actions) > 0:
                action = random.choice(actions)
    else:  # Make move
        board = makeMoves(board, color, action)
    # Step 3: Return the new board after the jump was made
    return board


def checkEndGame(board, color):
    '''
    A game can end in two ways:
    1) A player has no pieces
    2) A player can no longer make a move
    Note: A tie "can" occur but is very rare and shouldn't happen using a sudo-random play bot
    '''
    agentWin = False
    playerWin = False

    # Scenario 1: A player has lost all of their pieces
    # If no opponent pieces are found, the agent won
    if (value_dic["enemyMan"] not in board) and (value_dic["enemyKing"] not in board):
        agentWin = True
    # If no agent pieces are found, the opponent won
    elif (value_dic["ownMan"] not in board) and (value_dic["ownKing"] not in board):
        playerWin = True

    # Scenario 2: A player has no valid moves to make

    # If there are no valid moves for the agent, the opponent wins
    if len(getMoves(board, color, player="Agent")) == 0:
        playerWin = True
    # If there are no valid moves for the opponent, the agent wins
    elif len(getMoves(board, color, player="Opponent")) == 0:
        agentWin = True

    # Return Values - These are the rewards given
    if agentWin:
        return 1.0
    elif playerWin:
        return -1.0
    else:
        return 0


def shouldSave(board):
    '''
    This function is to prevent the collection of 'end' state moves
    When a player has less than 3 pieces the scenarios are most likely a decisive win
    OR both players running around the board creating states that may never be used again
    Therefore, we are ignoring these end states
    '''

    agentMan = (board == value_dic["ownMan"]).sum()
    agentKing = (board == value_dic["ownKing"]).sum()
    opponentMan = (board == value_dic["enemyMan"]).sum()
    opponentKing = (board == value_dic["enemyKing"]).sum()

    if agentMan + agentKing < 3:
        return False
    elif opponentMan + opponentKing < 3:
        return False
    else:
        return True