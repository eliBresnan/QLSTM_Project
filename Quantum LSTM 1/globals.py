import numpy as np


# Global Constants #

e = np.e
pi = np.pi

STATE_INPUT_FILE = "States/Initial_State.json"
STATE_OUTPUT_FILE = "States/Test.json"
MODEL_FILE_PREFIX = "TrainLR_2."
DATA_INPUT_FILE = "Data/WolvesTeamStats.json"

DATA_DIMENSIONS = 6  # Changing this will mess up all the states, don't do it
VARIATIONAL_DEPTH = 1

PARAMETER_SHIFT_ANGLE = pi/2

LEARNING_RATE = .15
DECAY_RATE = .95
Epoch = 1
def Epoch_Global_Update(iteration=Epoch+1):
    global Epoch 
    Epoch = iteration
def GET_LEARNING_RATE():
    # return LEARNING_RATE*(DECAY_RATE**(Epoch-1))
    return LEARNING_RATE


# Hard coded ranges for basketball statistics
    # Field Goal %
    # 3 Point %
    # Free Throw %
    # Blocks + Rebounds
    # Turn Overs + Steals
    # Points
DATA_SCALE = {
    "Mins":
    [
        0,
        0,
        0,
        20,
        8,
        50
    ],
    "Maxes":
    [
        100,
        100,
        100,
        80,
        40,
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
def normalize_vector(v):
    v_norm = []
    min = None
    max = None
    x_norm = None
    for i in range(DATA_DIMENSIONS):
        min = DATA_SCALE["Mins"][i]
        max = DATA_SCALE["Maxes"][i]
        x_norm = (v[i] - min) / (max - min)
        if x_norm < 0 or x_norm > 1:
            print("Data point out of bounds of min and max")
            return None
        v_norm.append(x_norm)
    return v_norm

# scales values from [-1,1] to [0,1]
def scale_vector(v):
    return [((x+1)/2) for x in v]

# scales output from [-1,1] to basketball statistics
     # converts from range [-1,1] to [0,1]
     # denormalizes, returns to actual stat
def scale_vector_for_stats(v):
    v_scaled = []
    min = None 
    max = None
    for i in range(DATA_DIMENSIONS):
        min = DATA_SCALE["Mins"][i]
        max = DATA_SCALE["Maxes"][i]
        v_scaled.append((((v[i]+1)/2) * (max - min)) + min)
    return v_scaled



