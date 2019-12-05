# Imports
import numpy as np
import random
from enviromentAPI import *
from os import path
import joblib
# --------------------------

# Load Policy
WHITE_v = joblib.load("Pickles/WHITE_v.sav", "rb")
BLACK_v = joblib.load("Pickles/BLACK_v.sav", "rb")
# --------------------------

# This is the parameter to change
num_games = 10000

colors = ["w", "b"]

# Result Values
# Note: Since jumps are rule based we will not include as an action or policy used
WHITE_wins = 0
WHITE_ties = 0
WHITE_num_games = 0
WHITE_policy_used = 0
WHITE_actions_taken = 0
# ----
BLACK_wins = 0
BLACK_ties = 0
BLACK_num_games = 0
BLACK_policy_used = 0
BLACK_actions_taken = 0
# --------------------------

for i in range(num_games):
    print("Loop Number:", i)
    # Choose Agent Color
    if i < num_games//2:
        agentColor = colors[0]
    else:
        agentColor = colors[1]

    state = createEnviroment(agentColor)

    if agentColor == "w":
        WHITE_num_games += 1

        tmp_WHITE_policy_used = 0
        tmp_WHITE_actions_taken = 0
        for wcount in range(1000):  # Checkers game should't go over 1k moves
            # Black Goes first
            state = takeStep(state, agentColor)
            reward = checkEndGame(state, agentColor)
            if reward == 1.0:
                WHITE_wins += 1
                break
            elif reward == -1.0:
                # Agent lost
                break

            # White goes
            # Collect all of the possible actions
            jump = True
            actions = getJumps(state, agentColor)      # First look for a jump
            if len(actions) == 0:
                jump = False
                actions = getMoves(state, agentColor)  # If no jump, look for a move

            # Choose an action
            if not jump:
                tmp_WHITE_actions_taken += 1
                knownStates = []
                for a in actions:
                    temp_state = makeMoves(state, agentColor, a)
                    try:
                        # The temp_state may noy be in v. That is why we need to 'try' this
                        knownStates.append([a, WHITE_v[str(temp_state)]])
                    except:
                        pass
                # We know of at least one of the states available to us
                if len(knownStates) > 0:
                    tmp_WHITE_policy_used += 1
                    allValues = list((map(lambda x: x[1], knownStates)))  # Collect all the values
                    actionIndex = allValues.index(max(allValues))         # Find the index of the max value
                    action = knownStates[actionIndex][0]                  # Find the action that is the max value
                    state = makeMoves(state, agentColor, action)          # Make action
                else:
                    action = random.choice(actions)                       # All states are new, make random move
                    state = makeMoves(state, agentColor, action)          # Make action
            # Have to jump
            else:
                action = random.choice(actions)
                # Double jump logic
                while len(actions) > 0:  # There is at least one jump available
                    actions, state = makeJumps(state, agentColor, action)
                    if len(actions) > 0:
                        action = random.choice(actions)

            # Collect the reward. ONLY to see if the game is over
            reward = checkEndGame(state, agentColor)

            if reward == 1.0:
                WHITE_wins += 1
                break
            elif reward == -1.0:
                # Agent lost
                break
        if wcount == 999:  # Tie
            WHITE_ties += 1
        else:
            WHITE_actions_taken += tmp_WHITE_actions_taken
            WHITE_policy_used += tmp_WHITE_policy_used
    else:
        BLACK_num_games += 1

        tmp_BLACK_policy_used = 0
        tmp_BLACK_actions_taken = 0
        for bcount in range(1000):
            # Black Goes first
            # Collect all of the possible actions
            jump = True
            actions = getJumps(state, agentColor)  # First look for a jump
            if len(actions) == 0:
                jump = False
                actions = getMoves(state, agentColor)  # If no jump, look for a move

            # Choose an action
            if not jump:
                tmp_BLACK_actions_taken += 1
                knownStates = []
                for a in actions:
                    temp_state = makeMoves(state, agentColor, a)
                    try:
                        # The temp_state may noy be in v. That is why we need to 'try' this
                        knownStates.append([a, BLACK_v[str(temp_state)]])
                    except:
                        pass
                # We know of at least one of the states available to us
                if len(knownStates) > 0:
                    tmp_BLACK_policy_used += 1
                    allValues = list((map(lambda x: x[1], knownStates)))  # Collect all the values
                    actionIndex = allValues.index(max(allValues))  # Find the index of the max value
                    action = knownStates[actionIndex][0]  # Find the action that is the max value
                    state = makeMoves(state, agentColor, action)  # Make action
                else:
                    action = random.choice(actions)  # All states are new, make random move
                    state = makeMoves(state, agentColor, action)  # Make action
            # Have to jump
            else:
                action = random.choice(actions)
                # Double jump logic
                while len(actions) > 0:  # There is at least one jump available
                    actions, state = makeJumps(state, agentColor, action)
                    if len(actions) > 0:
                        action = random.choice(actions)

            # Collect the reward. ONLY to see if the game is over
            reward = checkEndGame(state, agentColor)

            if reward == 1.0:
                BLACK_wins += 1
                break
            elif reward == -1.0:
                # Agent lost
                break

            # White goes
            state = takeStep(state, agentColor)
            reward = checkEndGame(state, agentColor)

            if reward == 1.0:
                BLACK_wins += 1
                break
            elif reward == -1.0:
                # Agent lost
                break
        if bcount == 999:  # Tie
            BLACK_ties += 1
        else:
            BLACK_actions_taken += tmp_BLACK_actions_taken
            BLACK_policy_used += tmp_BLACK_policy_used

print("Done with ", num_games, " Tests")
# ----
print("Number of Games as White: ", WHITE_num_games)
print("Number of Wins: ", WHITE_wins)
print("Number of Ties: ", WHITE_ties)
print("White Policy Used: ", WHITE_policy_used)
print("White Actions Taken: ", WHITE_actions_taken)
print("--------")
print("Number of Games as Black: ", BLACK_num_games)
print("Number of wins: ", BLACK_wins)
print("Number of ties: ", BLACK_ties)
print("Black Policy Used: ", BLACK_policy_used)
print("Black Actions Taken: ", BLACK_actions_taken)