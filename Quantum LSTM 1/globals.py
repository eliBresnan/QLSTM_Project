import numpy as np


# Global Constants #

e = np.e
pi = np.pi

STATE_INPUT_FILE = "States/Initial_State.json"
STATE_OUTPUT_FILE = "States/Train_1.json"

DATA_DIMENSIONS = 8   # Changing this will mess up all the states, don't do it
VARIATIONAL_DEPTH = 1

PARAMETER_SHIFT_ANGLE = pi/2

LEARNING_RATE = .01


# Hard coded ranges for basketball statistics
    # Field Goal %
    # 3 Point %
    # Free Throw %
    # Rebounds
    # Blocks
    # Steals
    # Turn Overs
    # Points
DATA_SCALE = {
    "Mins":
    [
        0,
        0,
        0,
        20,
        0,
        0,
        5,
        50
    ],
    "Maxes":
    [
        100,
        100,
        100,
        80,
        20,
        15,
        30,
        170
    ]
}


# Formulas and operations #

def sin(x):
    return np.sin(x)

def sigmoid(x): 
    if isinstance(x, list):
        for i in range(len(x)):
            x[i] = (e**x[i]) / (1 + (e**x[i]))
        return x
    else:
        return (e**x) / (1 + (e**x))


def tanh(x):
    if isinstance(x, list):
        for i in range(len(x)):
            x[i] = ((e**x[i]) - (e**-x[i]))/ ((e**x[i])+(e**-x[i]))
        return x
    else:
        return ((e**x) - (e**-x))/ ((e**x)+(e**-x))

# Takes value x and the index of which data type
# scales to [0,1] based on hardcoded data range values above
def normalize_input(x,scale_index):
    min = DATA_SCALE["Mins"][scale_index]
    max = DATA_SCALE["Maxes"][scale_index]

    x_norm = (x - min) / (max - min)
    if x_norm < 0 or x_norm > 1:
        print("Data point out of bounds of min and max")
        return
    return x_norm

# scales values from [-1,1] to [0,1]
def scale(x):
    return (x+1)/2
def scale_vector(v):
    return [((x+1)/2) for x in v]

# scales output from [-1,1] to basketball statistics
def scale_for_stats(x,scale_index):
    min = DATA_SCALE["Mins"][scale_index]
    max = DATA_SCALE["Maxes"][scale_index]

    x = (x+1)/2                          # converts from range [-1,1] to [0,1]
    scaled_x = (x * (max - min)) + min   # denormalizes, returns to actual stat
    return  scaled_x


