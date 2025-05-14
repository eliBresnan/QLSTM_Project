
# from qiskit_ibm_runtime import QiskitRuntimeService

# service = QiskitRuntimeService(channel="ibm_quantum",
#                                 token = '0d04369be7950f54eaf9f9eba8ea9ac798942f66e8664b74a886f9bb210992e2a613969515173b3e6d189cda7b48fa672741ebe1484466664a1a562a63dc4c76')



from lstm import QLSTM_Cell as Cell
from globals import *

from datetime import datetime
import json

#import sys

# Check for fatal errors
# if DATA_DIMENSIONS != 8:
#     print("The dimensions of data in the globals file is not 8.\nThis may cause errors with loading states and may erase state data.")
#     answer = input("Type 'Yes' if you would like to continue >> ")
#     if answer != 'Yes':
#         print("Program Terminated")
#         sys.exit()

def open_json(file):
    with open(file) as json_data:
        dict = json.load(json_data)
        json_data.close()
    return dict

def write_to_json(dict,filepath):
    with open(filepath,'w') as file:
        json.dump(dict,file,indent=4)
        file.close()


# data = open_json(DATA_INPUT_FILE)
# model_state = open_json(STATE_INPUT_FILE)
# model = Cell(model_state)
data = None
model_state = None
model = None


def main():
    
    global data
    global model_state
    global model

    data = open_json(DATA_INPUT_FILE)
    model_state = open_json(STATE_INPUT_FILE)
    model = Cell(model_state)

    
    train(1,50,4)
    #train(1,3,3)
    return

# 
def train(batch_size,batches,epochs):

    if model_state["Epoch_Iterations"] == 0:
        model_state["Epoch_Dates"] = data["Dates"][:(batch_size*batches)]
    else:
        Epoch_Global_Update(model_state["Epoch_Iterations"]+1) 

    # initialize
    targets = None
    target_indexes = None 
    target_dates = None
    output = None
    loss = None
    losses = []

    start_time = datetime.now()

    input_dates = model_state["Epoch_Dates"][0:batch_size]
    input_indexes = [data["Indexes"][date] for date in input_dates]
    input_batch = [normalize_vector(data["Stats"][index]) for index in input_indexes]

    b = 1
    # train batch
    while b < batches:

        print(f"************** Training batch {b} of {batches-1} *****************")


        # optimize
        target_dates = [model_state["Epoch_Dates"][b*batch_size + x] for x in range(batch_size)]
        target_indexes = [data["Indexes"][date] for date in target_dates]
        targets = [normalize_vector(data["Stats"][index]) for index in target_indexes]

        model.parameter_shift(input_batch,targets[0], skip_trivial=(b>3))

        # step forward in time series
        output = scale_vector(model.run_cell(input_batch))
        b+=1
        input_batch = targets

        # Calculate loss at each step
        loss = sum((output[x]-input_batch[0][x])**2 for x in range(DATA_DIMENSIONS))
        losses.append(loss)
    
    end_time = datetime.now()
    minutes_passed = (60*end_time.hour + end_time.minute + (1/60)*end_time.second) - (60*start_time.hour + start_time.minute + (1/60)*start_time.second)

    model_state["Training_Minutes"] += minutes_passed
    model_state["Losses"].append(losses)
    model_state["Epoch_Iterations"] += 1
    model_state["Prediction"] = scale_vector_for_stats(model.run_cell(input_batch))   
    save_state()

    print(f"---------------------> Epoch {model_state["Epoch_Iterations"]} Complete <--------------------")
    if epochs > 1:
        Epoch_Global_Update()
        train(batch_size,batches,epochs-1) 

    return

def save_state(iterative_op_files = True):

    new_state = model.get_state()
    model_state.update(new_state)
    write_to_json(model_state,f"States/{MODEL_FILE_PREFIX}{model_state["Epoch_Iterations"]}.json" if iterative_op_files else STATE_OUTPUT_FILE)

    return


main()

    


