'''
Currently there is a small issue where a blank state is being created for basically every iteration
this does not really effect the program but is something we should look at if we have time
'''

import pandas as pd
import numpy as np
import re
import joblib
from enviromentAPI import *

'''
Important Note:
when parsing the historical data, the cell numbers were [1-32]
Our logic represents the board with cell numbers [0-31]
Therefore, we need to subtract 1 from the historical data
'''
historicalData = pd.read_pickle("Pickles/games_df.p")

discount = 1
returns = {}
v = {}


def getMoveObject(a, s):
    a = a.split('-')
    # Fixing the 1 difference between historical and our data
    # print(action)
    for i in range(len(a)):
        try:
            a[i] = int(a[i]) - 1
        except:
            return []  # Issue with the historical data
    # Make 'move' object
    return [a[0], a[1], s[a[0]]]


def getJumpObject(a, s, c, player):
    a = a.split('x')
    # Fixing the 1 difference between historical and our data
    # print(action)
    for i in range(len(a)):
        try:
            a[i] = int(a[i]) - 1
        except:
            return []  # Issue with the historical data
    # Need to make jump while considering the possibilities of a double
    for j in range(len(a)):
        if j != len(a) - 1:
            oldCell = a[j]
            newCell = a[j + 1]
            remove = findRemove(s, c, oldCell, newCell, player=player)
            value = s[a[j]]
            return [oldCell, newCell, remove, value]


# This function is for finding what cell was jumped given the start and stop cells of the jumping piece
def findRemove(state, color, oldCell, newCell, player):
    possibleJumps = getJumps(state, color, player)
    for jump in possibleJumps:
        if (oldCell == jump[0]) and (newCell == jump[1]):
            return jump[2]


# run through the number of episodes - as white
for index, row in historicalData.iterrows():

    # Step 1: Play as white for every game
    state = createEnviroment('w')

    # See if we won
    if row["Winner"] == "White":
        finalReward = 1
    elif row["Winner"] == "Draw":
        finalReward = 0
    else:
        finalReward = -1

    # Temporary Storage
    episode_state = []
    episode_state.append(state)  # Start State

    actionNumber = 0
    skip = False
    while True:
        # Step 1: Take a step in the environment. Black always goes first and we are always playing as white
        try:
            action = row["BlackMoves"][actionNumber]
        except:
            # If we can not collect a move we can assume there is no move. This would be because the game is over
            break

        if re.search(r'-', action):  # This is a move
            moveObject = getMoveObject(action, state)
            # Error collecting the move object. Abort
            if len(moveObject) == 0:
                skip = True
                break
            state = makeMoves(state, "w", moveObject)
        # if not move, then jump
        else:
            jumpObject = getJumpObject(action, state, "w", "Opponent")
            # Error collecting the jump object. Abort
            if len(jumpObject) == 0:
                skip = True
                break
            # Make jump returns the new state AFTER checking for kings
            discard, state = makeJumps(state, "w", jumpObject, player="Opponent")

        # Step 2: Collect the "agent's" move
        try:
            action = row["WhiteMoves"][actionNumber]
        except:
            # If we can not collect a move we can assume there is no move. This would be because the game is over
            break

        if re.search(r'-', action):  # This is a move
            moveObject = getMoveObject(action, state)
            # Error collecting the move object. Abort
            if len(moveObject) == 0:
                skip = True
                break
            state = makeMoves(state, "w", moveObject)
        # if not move, then jump
        else:
            jumpObject = getJumpObject(action, state, "w", "Agent")
            # Error collecting the jump object. Abort
            if len(jumpObject) == 0:
                skip = True
                break
            # Make jump returns the new state AFTER checking for kings
            discard, state = makeJumps(state, "w", jumpObject, player="Agent")

        # Step 3: Save the state
        episode_state.append(str(state))

        # Step 4: Move to next move
        actionNumber += 1

    if not skip:
        # Step 6: Assign the rewards to the actions
        episode_reward = np.zeros(len(episode_state))
        episode_reward[len(episode_reward)-1] = finalReward
        # Step 7: Calculate g -- This may need to be revised / optimized
        g = 0
        for tg in range(len(episode_reward) - 1, -1, -1):
            g = discount * g + episode_reward[tg]
            # print("Iteration: ", tg, "\nIndex: ", episode_state.index(episode_state[tg]))
            if episode_state.index(episode_state[tg]) == tg:
                if str(episode_state[tg]) in returns:
                    returns[str(episode_state[tg])][0] += g  # Sum
                    returns[str(episode_state[tg])][1] += 1  # Count
                else:
                    returns[str(episode_state[tg])] = [g, 1]
                v[str(episode_state[tg])] = returns[str(episode_state[tg])][0] / returns[str(episode_state[tg])][1]

print("Moving")
# ------------------------------------------------------------------------

# run through the number of episodes -as black
for index, row in historicalData.iterrows():

    # Step 1: Play as black for every game
    state = createEnviroment('b')

    # See if we won
    if row["Winner"] == "Black":
        finalReward = 1
    elif row["Winner"] == "Draw":
        finalReward = 0
    else:
        finalReward = -1

    # Temporary Storage
    episode_state = []
    episode_state.append(state)  # Start State

    actionNumber = 0
    skip = False
    while True:
        # Step 1: Make the "agent's" move
        try:
            action = row["BlackMoves"][actionNumber]
        except:
            # If we can not collect a move we can assume there is no move. This would be because the game is over
            break

        if re.search(r'-', action):  # This is a move
            moveObject = getMoveObject(action, state)
            if len(moveObject) == 0:
                skip = True
                break
            state = makeMoves(state, "b", moveObject)
        # if not move, then jump
        else:
            jumpObject = getJumpObject(action, state, "b", "Agent")
            if len(jumpObject) == 0:
                skip = True
                break
            # Make jump returns the new state AFTER checking for kings
            discard, state = makeJumps(state, "b", jumpObject, player="Agent")

        # Step 2: Save the state
        # print(state)
        episode_state.append(str(state))

        # Step 3: Take a step in the environment
        try:
            action = row["WhiteMoves"][actionNumber]
        except:
            # If we can not collect a move we can assume there is no move. This would be because the game is over
            break

        if re.search(r'-', action):  # This is a move
            moveObject = getMoveObject(action, state)
            if len(moveObject) == 0:
                skip = True
                break
            state = makeMoves(state, "b", moveObject)
        # if not move, then jump
        else:
            jumpObject = getJumpObject(action, state, "b", "Opponent")
            if len(jumpObject) == 0:
                skip = True
                break
            # Make jump returns the new state AFTER checking for kings
            discard, state = makeJumps(state, "b", jumpObject, player="Opponent")

        # Step 4: Move to next move
        actionNumber += 1

    if not skip:
        # Step 6: Assign the rewards to the actions
        episode_reward = np.zeros(len(episode_state))
        episode_reward[len(episode_reward)-1] = finalReward
        # Step 7: Calculate g -- This may need to be revised / optimized
        g = 0
        for tg in range(len(episode_reward) - 1, -1, -1):
            g = discount * g + episode_reward[tg]
            # print("Iteration: ", tg, "\nIndex: ", episode_state.index(episode_state[tg]))
            if episode_state.index(episode_state[tg]) == tg:
                if str(episode_state[tg]) in returns:
                    returns[str(episode_state[tg])][0] += g  # Sum
                    returns[str(episode_state[tg])][1] += 1  # Count
                else:
                    returns[str(episode_state[tg])] = [g, 1]
                v[str(episode_state[tg])] = returns[str(episode_state[tg])][0] / returns[str(episode_state[tg])][1]

joblib.dump(returns, 'Pickles/returns_starting.sav')

joblib.dump(v, 'Pickles/v_starting.sav')