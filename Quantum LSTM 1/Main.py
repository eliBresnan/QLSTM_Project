
# from qiskit_ibm_runtime import QiskitRuntimeService

# service = QiskitRuntimeService(channel="ibm_quantum",
#                                 token = '0d04369be7950f54eaf9f9eba8ea9ac798942f66e8664b74a886f9bb210992e2a613969515173b3e6d189cda7b48fa672741ebe1484466664a1a562a63dc4c76')


from lstm import QLSTM_Cell as Cell
from globals import *
from circuit import VQC

import json

import sys

# Check for fatal errors
if DATA_DIMENSIONS != 8:
    print("The dimensions of data in the globals file is not 8.\nThis may cause errors with loading states and may erase state data.")
    answer = input("Type 'Yes' if you would like to continue >> ")
    if answer != 'Yes':
        print("Program Terminated")
        sys.exit()

def open_json(file):
    with open(file) as json_data:
        dict = json.load(json_data)
        json_data.close()
    return dict

def write_to_json(dict,filepath):
    with open(filepath,'w') as file:
        json.dump(dict,file,indent=4)
        file.close()




def train():

    # load initial state
    model_state = open_json(STATE_INPUT_FILE)
    model = Cell(model_state)

    # preparing epoch data
    wolves_data = open_json('Data/WolvesTeamStats.json')
    epoch = []
    for game in wolves_data["Lists"][:-1]:
        norm_game = [normalize_input(game[i],i) for i in range(DATA_DIMENSIONS)]
        epoch.append(norm_game)
    
    # run model and save state
    losses = model.train_epoch(epoch)
    state_after_train = model.get_state()
    state_after_train["Training_Loss"] = losses
    state_after_train["Prediction"] = [scale_for_stats(state_after_train["Output"][i],i) for i in range(DATA_DIMENSIONS)]
    write_to_json(state_after_train,STATE_OUTPUT_FILE)

    return

def main():

    train()
    return


main()


# **This is for converting data dictionaries to vectors**

# dict = open_json("Data/WolvesTeamStats.json")
# list = []

# for game in dict["Games"]:
#     glist = []
#     glist.append(game["Stats"]["FG%"])
#     glist.append(game["Stats"]["3P%"])
#     glist.append(game["Stats"]["FT%"])
#     glist.append(game["Stats"]["REB"])
#     glist.append(game["Stats"]["BLK"])
#     glist.append(game["Stats"]["STL"])
#     glist.append(game["Stats"]["TO"])
#     glist.append(game["Stats"]["PTS"])
#     list.append(glist)

# dict["Lists"] = list
# write_to_json(dict,"Data/WolvesTeamStats.json")
