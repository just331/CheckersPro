import numpy as np
import random
from enviromentAPI import *
from os import path
import pickle

# Parameters
num_Episodes = 10000
type_Episodes = "Normal"  # Other possible type is "Random"
discount = 1  # Not sure what we should do here

# Hard Coded Globals
colors = ["w", "b"]

# Global Storage
if path.exists("returns.pkl"):
    returns = pickle.load(open("returns.pkl", "rb"))
else:
    returns = {}
if path.exists("v.pkl"):
    v = pickle.load(open("v.pkl", "rb"))
else:
    v = {}


# run through n number of episodes
for i in range(num_Episodes):
    # Choose the agent's color for this episode
    agentColor = random.choice(colors)
    # start a new episode
    if type_Episodes == "Normal":
        state = createEnviroment(agentColor)
    else:  # type_Episodes == "Random"
        state = createRandomEnviroment(agentColor, random.random())
        # Checking if the random board created was already in an "end game" state. If so, skip this iteration
        if checkEndGame(state, agentColor) != 0:
            print("End Game Board")  # Printing to see how often this occurs
            continue

    # Temporary Storage
    episode_state = []
    episode_action = []
    episode_reward = []
    episode_state.append(state)  # Start State

    while True:
        # get a random action from the environment
        jump = True
        actions = getJumps(state, agentColor)      # First look for a jump
        if len(actions) == 0:
            jump = False
            actions = getMoves(state, agentColor)  # If no jump, look for a move
        # Choose a random move
        action = random.choice(actions)

        if jump:
            while len(actions) > 0:  # There is at least one jump available
                actions, state = makeJumps(state, agentColor, action)
                if len(actions) > 0:
                    action = random.choice(actions)
        else:  # Make move
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

#print("\nv")
#print_dict(v)
# for tempKey in v:
#     if v[tempKey] != -1 and v[tempKey] != 1:
#         print(v[tempKey])

# --- Save values ---
with open('returns.pkl', 'wb') as handle_r:
    pickle.dump(returns, handle_r)

with open('v.pkl', 'wb') as handle_v:
    pickle.dump(v, handle_v)


# NOTES:
# Sudo Random - Look ahead for double jumps and prioritize those
# Prioirtize getting a king from making a different move
# If an agent makes a move, we should report the state after the player? or only after the agnet?
# I think after opponent
# Try to reduce state space
# During play, look for state, if state is not found try looking for an all 'lower case' of the same state

# So it looks like numpy is auto adding \n but that doesn't seem to be a problem