import matplotlib.pyplot as plt

import math

import json

def compare_two(model1_file,model2_file,model3_file):

    with open(model1_file) as json_data:
        model1 = json.load(json_data)
        json_data.close()

    with open(model2_file) as json_data:
        model2 = json.load(json_data)
        json_data.close()

    with open(model3_file) as json_data:
        model3 = json.load(json_data)
        json_data.close()


    epochs = model1["Epoch_Iterations"]

    y_1 = []
    y_2 = []
    y_3 = []
    for i in range(epochs):
        y_1 += model1["Losses"][i]
        y_2 += model2["Losses"][i]
        y_3 += model3["Losses"][i]

    step = epochs/len(y_1)
    x_vals=[(1+(i*step))/2 for i in range(len(y_1))]

   
    plt.plot(x_vals,y_1, label = "Pi/4")
    plt.plot(x_vals,y_2, label = "Pi/3")
    plt.plot(x_vals,y_3, label = "Pi/2")
    plt.xlabel("Epoch")
    plt.ylabel("Data Loss")
    plt.title("Comparison of Paramter Shift angle")
    plt.legend()
    plt.ylim(0,.4)
    plt.xlim(.5,2.6)
    plt.show()


compare_two("States/Train_1.5.json","States/Train_2.5.json","States/Train_3.5.json")