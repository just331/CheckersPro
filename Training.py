# Imports
import numpy as np
import random
from enviromentAPI import *
from os import path
import pickle
# --------------------------

# Parameters
# Total number of runs will be num_saves * num_Episodes_per_Save
num_saves = 10
percent_20 = num_saves//5
num_Episodes_per_Save = 1#1000000
discount = 1              # Not sure what we should do here. Currently keeping 1.
epsilon = .1              # Coefficient of exploration. epsilon = 0 is pure greedy, = 1 is pure exploration
# --------------------------

# Hard Coded Globals
colors = ["w", "b"]
type_Episodes = ["Normal", "Random"]
# --------------------------

# Global Storage
if path.exists("Pickles/returns.pkl"):
    # Load what we've learned
    returns = pickle.load(open("Pickles/returns.pkl", "rb"))
else:
    # If the returns dictionary does not exists, then, initialize returns to the dictionary created in simulations
    returns = pickle.load(open("Pickles/returns_starting.pkl", "rb"))

if path.exists("Pickles/v.pkl"):
    # Load what we've learned
    v = pickle.load(open("Pickles/v.pkl", "rb"))
else:
    # If the v dictionary does not exists, then, initialize v to the dictionary created in simulations
    v = pickle.load(open("Pickles/v_starting.pkl", "rb"))
# --------------------------

# I want to periodically save results and v in case of a crash
for x in range(num_saves):
    # Decide if this save cycle should be a normal start or a random start
    if x < percent_20:
        type_Episode = type_Episodes[1]
    else:
        type_Episode = type_Episodes[0]

    # run through n number of episodes, for this save iteration
    for i in range(num_Episodes_per_Save):
        # Choose the agent's color for this episode
        agentColor = random.choice(colors)
        # start a new episode
        if type_Episode == "Normal":
            state = createEnviroment(agentColor)
        else:  # type_Episodes == "Random"
            state = createRandomEnviroment(agentColor, random.random())
            # Checking if the random board created was already in an "end game" state. If so, skip this iteration
            if checkEndGame(state, agentColor) != 0:
                #print("End Game Board")  # Printing to see how often this occurs
                continue

        # Temporary Storage
        episode_state = []
        episode_action = []
        episode_reward = []
        episode_state.append(state)  # Start State

        while True:
            # Collect all of the possible actions
            jump = True
            actions = getJumps(state, agentColor)      # First look for a jump
            if len(actions) == 0:
                jump = False
                actions = getMoves(state, agentColor)  # If no jump, look for a move

            # Choose an action
            # Check for policy, only if the action is a move -- we may need to optimize this
            if not jump and random.random() < epsilon:
                knownStates = []
                for a in actions:
                    temp_state = makeMoves(state, agentColor, a)
                    try:
                        # The temp_state may noy be in v. That is why we need to 'try' this
                        knownStates.append([a, v[str(temp_state)]])
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

            episode_action.append(action)
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

        # Calculate g -- This may need to be revised / optimized
        g = 0
        for tg in range(len(episode_reward) - 1, -1, -1):
            g = discount * g + episode_reward[tg]
            # print("Itteration: ", tg, "\nIndex: ", episode_state.index(episode_state[tg]))
            if episode_state.index(episode_state[tg]) == tg:
                if str(episode_state[tg]) in returns:
                    returns[str(episode_state[tg])].append(g)
                else:
                    returns[str(episode_state[tg])] = [g]
                v[str(episode_state[tg])] = sum(returns[str(episode_state[tg])]) / \
                                       len(returns[str(episode_state[tg])])

    # End of this save iteration, therefore we need to save
    # --- Save values ---
    with open('Pickles/returns.pkl', 'wb') as handle_r:
        pickle.dump(returns, handle_r)

    with open('Pickles/v.pkl', 'wb') as handle_v:
        pickle.dump(v, handle_v)
    # --------------------------

# Printing
#print("\nv")
#print_dict(v)
# for tempKey in v:
#     if v[tempKey] != -1 and v[tempKey] != 1:
#         print(v[tempKey])
# --------------------------

# Save again just to make sure before we close the program
# --- Save values ---
with open('Pickles/returns.pkl', 'wb') as handle_r:
    pickle.dump(returns, handle_r)

with open('Pickles/v.pkl', 'wb') as handle_v:
    pickle.dump(v, handle_v)
# --------------------------