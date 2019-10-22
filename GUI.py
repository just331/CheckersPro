from randomPlay import *  # Previously created functions
from tkinter import *  # For gui stuff

startCell = -1
endCell = -1
startMove = True

# TODO: Entering a wrong moves crashes the entire game
# TODO: I need to see if this way of updating the GUI is resulting in a huge recursive problem
# TODO: Player logic looks to be sound except the game will force a jump (good) but chooses it randomly
def playerLogic(cellCount, master, activeGame, agentColor):
    global startCell, endCell  # I know globals are the devil but this is the easier/best solution for this problem
    # Need to change this logic but currently some functions want to know the players color and not the agent color
    if agentColor == "black":
        playerColor = "w"
    else:
        playerColor = "b"
    if startCell == -1 and endCell == -1:
        startCell = cellCount
    else:
        endCell = cellCount
        foundJump, activeGame = checkForJumps(activeGame, "player", agentColor)
        if foundJump:
            startCell, endCell = -1, -1  # Reset temp values
            printGUI(master, activeGame, agentColor)
            agentLogic(master, activeGame, agentColor)
        else:
            user_move = [startCell, endCell]
            validMove = False  # Assume the move is invalid
            # Make sure move is valid
            while(not validMove):
                validMove = checkMove(activeGame, user_move, playerColor)  # Check if the move is valid
                if not validMove:
                    print("You did a bad job...Enter start cell and end cell: '# #'")
                    startCell, endCell = -1, -1  # Reset temp values
                    printGUI(master, activeGame, agentColor)
            # Valid move
            temp_value = activeGame[user_move[0]]  # Collect the piece info at the old cell
            activeGame[user_move[0]] = 0           # Remove the piece from the old cell
            activeGame[user_move[1]] = temp_value  # Move the piece to the new cell
            activeGame = checkForKing(activeGame, agentColor)  # See if this move resulted in a king
            # Print GUI and Reset moves
            startCell, endCell = -1, -1  # Reset temp values
            printGUI(master, activeGame, agentColor)
            agentLogic(master, activeGame, agentColor)


# TODO: I need to see if this way of updating the GUI is resulting in a huge recursive problem
# TODO: Jumps are forced and choose randomly ... Should let agent decide
def agentLogic(master, activeGame, agentColor):
    activeGame = checkForKing(activeGame, agentColor)  # See if these jumps resulted in a king
    foundJump, activeGame = checkForJumps(activeGame, "agent", agentColor)
    if foundJump:
        printGUI(master, activeGame, agentColor)
    else:
        activeGame = chooseMove(activeGame, agentColor)
        activeGame = checkForKing(activeGame, agentColor)  # See if the move resulted in a king
        printGUI(master, activeGame, agentColor)


def printGUI(master, activeGame, agentColor):
    global startMove
    if agentColor == "black" and startMove:
        startMove = False
        agentLogic(master, activeGame, agentColor)

    buttons = []
    n = 8
    cellCount = 0
    blankSquare = True
    for i in range(n):
        for j in range(n):
            if blankSquare:
                button = Button(master, height=5, width=10)
                button.grid(row=i, column=j)
                buttons.append(button)
            else:
                cellText = findTextValue(activeGame, 31-cellCount, agentColor)
                button = Button(master, text=str(cellText), bg="red", height=5, width=10, command=lambda x=i, y=j, cellNum=cellCount:
                    playerLogic(31-cellNum, master, activeGame, agentColor))
                button.grid(row=i, column=j)
                buttons.append(button)
                cellCount += 1
            blankSquare = not blankSquare
        if n % 2 == 0:
            blankSquare = not blankSquare


# TODO: Include a buffer screen for the user to see the flow of the game
# TODO: Have an endGame check using the predefined function
# TODO: Check the jump function because it is not always acting correctly,
#           I think this happenes when there are multiple jumps that can occur
def main():
    # Who will be what color? ... Currently hard coding agent to be black every game (and go first)
    agentColor = 'black'
    activeGame = startGame(agentColor)
    master = Tk()  # Make GUI
    master.title("CheckerPro")  # Name Window
    printGUI(master, activeGame, agentColor)  # Print Start Board and start the actual game
    master.mainloop()  # Keep window open

