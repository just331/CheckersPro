'''
Neural Network:
    Board can be represented by an 8x4 matrix
    Each cell can have the value of [-3, -1.5, 0, 1, +1.5]
Output (two ideas):
    A single move (what piece to move and to what spot)
    Same format as input (with a single change to 1 cell)
Training:
    Need to convert the current dataframe
    (state, move) - (state, move) - (state, move) … winner
    We are providing the state and the move taken. It can then learn from this?
'''

