# Imports
import numpy as np
import random
from datetime import datetime
from enviromentAPI import *
from os import path
import joblib
# --------------------------

# Parameters
# Total number of runs will be num_saves * num_Episodes_per_Save
num_saves = 20
percent_20 = num_saves//5
num_Episodes_per_Save = 100000
discount = 1              # Currently keeping 1.
epsilon = .1              # Coefficient of exploration. epsilon = 0 is pure greedy, = 1 is pure exploration
# --------------------------

# Hard Coded Globals
colors = ["w", "b"]
type_Episodes = ["Normal", "Random"]
# --------------------------

# Global Storage -- WHITE
if path.exists("Pickles/WHITE_returns.sav"):
    # Load what we've learned
    WHITE_returns = joblib.load("Pickles/WHITE_returns.sav", "rb")
else:
    # If the returns dictionary does not exists, then, initialize returns to the dictionary created in simulations
    WHITE_returns = joblib.load("Pickles/WHITE_returns_starting.sav", "rb")

if path.exists("Pickles/WHITE_v.sav"):
    # Load what we've learned
    WHITE_v = joblib.load("Pickles/WHITE_v.sav", "rb")
else:
    # If the v dictionary does not exists, then, initialize v to the dictionary created in simulations
    WHITE_v = joblib.load("Pickles/WHITE_v_starting.sav", "rb")
# --------------------------
# Global Storage -- BLACK
if path.exists("Pickles/BLACK_returns.sav"):
    # Load what we've learned
    BLACK_returns = joblib.load("Pickles/BLACK_returns.sav", "rb")
else:
    # If the returns dictionary does not exists, then, initialize returns to the dictionary created in simulations
    BLACK_returns = joblib.load("Pickles/BLACK_returns_starting.sav", "rb")

if path.exists("Pickles/BLACK_v.sav"):
    # Load what we've learned
    BLACK_v = joblib.load("Pickles/BLACK_v.sav", "rb")
else:
    # If the v dictionary does not exists, then, initialize v to the dictionary created in simulations
    BLACK_v = joblib.load("Pickles/BLACK_v_starting.sav", "rb")
# --------------------------

# I want to periodically save results and v in case of a crash
for x in range(num_saves):
    print("Save iteration:", x, " @ ", datetime.now())
    # Decide if this save cycle should be a normal start or a random start
    if x > num_saves-percent_20-1:
        type_Episode = type_Episodes[1]
        print("Random Start")
    else:
        type_Episode = type_Episodes[0]
        print("Normal Start")

    skipped = 0  # Internal testing metric

    # run through n number of episodes, for this save iteration
    for i in range(num_Episodes_per_Save):
        if (i == 10000) or (i == 20000) or (i == 30000) or (i == 40000) or (i == 50000) or (i == 60000) or (i == 70000) \
                    or (i == 80000) or (i == 90000):
            print("Sub iteration:", i, " @ ", datetime.now())

        # Choose the agent's color for this episode
        if i < num_Episodes_per_Save // 2:
            agentColor = colors[0]
        else:
            agentColor = colors[1]

        # start a new episode
        if type_Episode == "Normal":
            state = createEnviroment(agentColor)
        else:  # type_Episodes == "Random"
            state = createRandomEnviroment(agentColor, random.random())
            # Checking if the random board created was already in an "end game" state. If so, skip this iteration
            if checkEndGame(state, agentColor) != 0:
                continue

        # Temporary Storage
        episode_state = []
        episode_reward = []
        if shouldSave(state):
            episode_state.append(str(state))

        # Agent is playing as white - white goes 2nd
        if agentColor == "w":
            firstMove = True
            for moveNum_w in range(1000):
                if firstMove:
                    firstMove = False
                    # Black goes first
                    state = takeStep(state, agentColor)
                    reward = checkEndGame(state, agentColor)
                    # Have to append here so we can know what action resulted in a loss,
                    # if not a loss it'll be a zero just like if we appended before hand. This may need to be changed
                    if reward != 0:
                        episode_reward.append(reward)
                        break
                else:
                    # Collect all of the possible actions
                    jump = True
                    actions = getJumps(state, agentColor)      # First look for a jump
                    if len(actions) == 0:
                        jump = False
                        actions = getMoves(state, agentColor)  # If no jump, look for a move

                    # Choose an action
                    # Check for policy, only if the action is a move -- we may need to optimize this
                    if not jump and random.random() > epsilon:
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
                            allValues = list((map(lambda x: x[1], knownStates)))  # Collect all the values
                            actionIndex = allValues.index(max(allValues))         # Find the index of the max value
                            action = knownStates[actionIndex][0]                  # Find the action that is the max value
                            state = makeMoves(state, agentColor, action)          # Make action
                        else:
                            action = random.choice(actions)                       # All states are new, make random move
                            state = makeMoves(state, agentColor, action)          # Make action
                    # If we are making a jump, we are using enforced logic
                    elif jump:
                        # Currently we are randomly choosing a jump, not looking for maximum number of jumps
                        action = random.choice(actions)
                        # Double jump logic
                        while len(actions) > 0:  # There is at least one jump available
                            actions, state = makeJumps(state, agentColor, action)
                            if len(actions) > 0:
                                action = random.choice(actions)
                    else:  # Exploring and no jump available
                        action = random.choice(actions)
                        state = makeMoves(state, agentColor, action)

                    # Collect the reward. ONLY to see if the game is over
                    reward = checkEndGame(state, agentColor)

                    if shouldSave(state):
                        episode_state.append(str(state))

                    if reward != 0:  # Either a win or loss
                        episode_reward.append(reward)
                        break
                    else:  # Game is not over, need to take a step
                        state = takeStep(state, agentColor)
                        reward = checkEndGame(state, agentColor)
                        # Have to append here so we can know what action resulted in a loss,
                        # if not a loss it'll be a zero just like if we appended before hand. This may need to be changed
                        episode_reward.append(reward)
                        if reward != 0:  # Either a win or loss
                            break
            if moveNum_w == 999:
                print("Tie")
                episode_reward.append(0.0)
        # Agent is playing as black - black goes 1st
        else:
            for moveNum_b in range(1000):
                # Collect all of the possible actions
                jump = True
                actions = getJumps(state, agentColor)  # First look for a jump
                if len(actions) == 0:
                    jump = False
                    actions = getMoves(state, agentColor)  # If no jump, look for a move

                # Choose an action
                # Check for policy, only if the action is a move -- we may need to optimize this
                if not jump and random.random() > epsilon:
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
                        allValues = list((map(lambda x: x[1], knownStates)))  # Collect all the values
                        actionIndex = allValues.index(max(allValues))  # Find the index of the max value
                        action = knownStates[actionIndex][0]  # Find the action that is the max value
                        state = makeMoves(state, agentColor, action)  # Make action
                    else:
                        action = random.choice(actions)  # All states are new, make random move
                        state = makeMoves(state, agentColor, action)  # Make action
                # If we are making a jump, we are using enforced logic
                elif jump:
                    # Currently we are randomly choosing a jump, not looking for maximum number of jumps
                    action = random.choice(actions)
                    # Double jump logic
                    while len(actions) > 0:  # There is at least one jump available
                        actions, state = makeJumps(state, agentColor, action)
                        if len(actions) > 0:
                            action = random.choice(actions)
                else:  # Exploring and no jump available
                    action = random.choice(actions)
                    state = makeMoves(state, agentColor, action)

                # Collect the reward. ONLY to see if the game is over
                reward = checkEndGame(state, agentColor)

                if shouldSave(state):
                    episode_state.append(str(state))

                if reward != 0:  # Either a win or loss
                    episode_reward.append(reward)
                    break
                else:  # Game is not over, need to take a step
                    state = takeStep(state, agentColor)
                    reward = checkEndGame(state, agentColor)
                    # Have to append here so we can know what action resulted in a loss,
                    # if not a loss it'll be a zero just like if we appended before hand. This may need to be changed
                    episode_reward.append(reward)
                    if reward != 0:  # Either a win or loss
                        break
            if moveNum_b == 999:
                print("Tie")
                episode_reward.append(0.0)
        # Calculate g -- This may need to be revised / optimized
        updated_episode_reward = np.zeros(len(episode_state))
        # There is at least 1 recorded state
        if len(updated_episode_reward) > 0:
            updated_episode_reward[len(updated_episode_reward)-1] = episode_reward[len(episode_reward)-1]
            g = 0
            for tg in range(len(updated_episode_reward) - 1, -1, -1):
                g = discount * g + updated_episode_reward[tg]
                if agentColor == "w":
                    if episode_state.index(episode_state[tg]) == tg:
                        if str(episode_state[tg]) in WHITE_returns:
                            WHITE_returns[str(episode_state[tg])][0] += g  # Sum
                            WHITE_returns[str(episode_state[tg])][1] += 1  # Count
                        else:
                            WHITE_returns[str(episode_state[tg])] = [g, 1]
                        WHITE_v[str(episode_state[tg])] = WHITE_returns[str(episode_state[tg])][0] / \
                                                          WHITE_returns[str(episode_state[tg])][1]
                else:
                    if episode_state.index(episode_state[tg]) == tg:
                        if str(episode_state[tg]) in BLACK_returns:
                            BLACK_returns[str(episode_state[tg])][0] += g  # Sum
                            BLACK_returns[str(episode_state[tg])][1] += 1  # Count
                        else:
                            BLACK_returns[str(episode_state[tg])] = [g, 1]
                        BLACK_v[str(episode_state[tg])] = BLACK_returns[str(episode_state[tg])][0] / \
                                                          BLACK_returns[str(episode_state[tg])][1]
        else:
            skipped += 1

    print("Finished Save Iteration")
    print("Number Skipped: ", skipped)
    # This section enables checkpoint saving. Slows down training when enabled
    # # --- Save values ---
    # joblib.dump(WHITE_returns, 'Pickles/WHITE_returns.sav')
    #
    # joblib.dump(WHITE_v, 'Pickles/WHITE_v.sav')
    # # ----
    # joblib.dump(BLACK_returns, 'Pickles/BLACK_returns.sav')
    #
    # joblib.dump(BLACK_v, 'Pickles/BLACK_v.sav')
    # # --------------------------

print("Saving")
# --- Save values ---
joblib.dump(WHITE_returns, 'Pickles/WHITE_returns.sav')

joblib.dump(WHITE_v, 'Pickles/WHITE_v.sav')
# ----
joblib.dump(BLACK_returns, 'Pickles/BLACK_returns.sav')

joblib.dump(BLACK_v, 'Pickles/BLACK_v.sav')
# --------------------------
print("Training Finished - No Errors")
