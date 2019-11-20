import numpy as np
import random
from enviromentAPI import *

# Parameters
num_Episodes = 100
type_Episodes = "Normal"  # Other possible type is "Random"
discount = 1  # Not sure what we should do here

# Hard Coded Globals
colors = ["w", "b"]

# Global Storage
returns = {}
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

        if jump:  # Need to make this function and also implement a double jump logic
            state = makeJumps()
        else:  # Make move
            state = makeMoves(state, agentColor, action)

        # Collect the reward. ONLY to see if the game is over
        reward = checkEndGame(state, agentColor)

        episode_action.append(action)
        episode_state.append(state)

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

    # Calculate g
    g = 0
    for tg in range(len(episode_reward) - 1, -1, -1):
        g = discount * g + episode_reward[tg]
        if episode_state.index(episode_state[tg]) == tg:
            if episode_state[tg] in returns:
                returns[episode_state[tg]].append(g)
            else:
                returns[episode_state[tg]] = [g]
            v[episode_state[tg]] = sum(returns[episode_state[tg]]) / \
                                   len(returns[episode_state[tg]])

print("\nv")
print_dict(v)

# TODO: Save the global storage

