import json

signals = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]


def calc_stats(dict):
    outdict = {"games":[]}
    for key in dict.keys():
        ft_a = 0
        ft_m =0
        fg_a = 0
        fg_m=0
        tp_a = 0
        tp_m =0 
        blk_reb = 0
        to_stl = 0
        for player in dict[key]["stats"]:
            fg_m += player[0]
            fg_a += player[1]
            tp_m += player[2]
            tp_a+= player[3]
            ft_m += player[4]
            ft_a += player[5]
            blk_reb += player[6]+player[7]
            to_stl += player[8]+player[9]
        tpP = 100*tp_m/tp_a
        fgP = 100*fg_m/fg_a
        ftP = 100*ft_m/ft_a
        outdict["games"].append({
            "Date":key,
            "Stats":[
                fgP,
                tpP,
                ftP,
                blk_reb,
                to_stl,
                dict[key]["pts"]
            ]
        })
    with open("s.json","w") as file:
        json.dump(outdict,file,indent=4)
        file.close()
    return

def extract():

    dict = {}
    temp_date = None

    with open("RawData.txt","r") as file:
        line = file.readline()
        while line !="":

            line = line.split()
            if line[0] in signals:

                temp_date = f"{line[0]} {line[1]}"
                if temp_date not in dict:
                    dict[temp_date] = {
                        "pts":None,
                        "stats":[]
                        }
                    
                file.readline()
                file.readline()
                file.readline()
                if file.readline().split()[0] == "W":
                    dict[temp_date]["pts"] = int(file.readline().split()[0])
                else:
                    dict[temp_date]["pts"] = int(file.readline().split()[1])

                line = file.readline().split()
                dict[temp_date]["stats"].append([
                    int(line[1]),
                    int(line[2]),
                    int(line[4]),
                    int(line[5]),
                    int(line[7]),
                    int(line[8]),
                    int(line[10]),
                    int(line[12]),
                    int(line[13]),
                    int(line[15])
                ])
            line = file.readline()

        file.close()

    # with open("s.json",'w') as file:
    #     json.dump(dict,file,indent=4)
    #     file.close()
    
    return

def format():
    with open("s.json") as jsond:
        dict = json.load(jsond)
        jsond.close()
    
    outdict = {
        "Dates":[],
        "Indexes":{},
        "Stats":[]
    }
    
    j = 0
    for i in range(len(dict["games"])-1,-1,-1):
        outdict["Dates"].append(dict["games"][i]["Date"])
        outdict["Indexes"].update({dict["games"][i]["Date"]:j})
        outdict["Stats"].append(dict["games"][i]["Stats"])
        j += 1
    with open("WolvesTeamStats.json","w") as file:
        json.dump(outdict,file,indent=4)
        file.close()
    return
format()

# def turn_to_dict(textFile):
#     state = 0
#     date = None
#     points = None
#     words = None
#     game = []
#     dict = {"games":[]}
#     with open(textFile, "r") as file:
#         line = file.readline()
#         while line != "":

#             if line == "\n":
#                 dict["games"].append({
#                     "date":date,
#                     "pts":points,
#                     "game":game,
#                 })
#                 game = []
#                 state = 0
#             elif state == 0:
#                 date = line.split()
#                 date = f"{date[0]} {date[1]}"
#                 state = 1
#             elif state == 1:
#                 points = line
#                 state = 2
#             else:
#                 words = line.split()
#                 game.append([
#                     int(words[0]),
#                     int(words[1]),
#                     int(words[3]),
#                     int(words[4]),
#                     int(words[6]),
#                     int(words[7]),
#                     int(words[9]),
#                     int(words[11]),
#                     int(words[12]),
#                     int(words[14]),
#                     ])
#             line = file.readline()

#         file.close()

#     calculate_stats(dict)

def calculate_stats(dict):
    outdict = {}
    for game in dict["games"]:
        threes_made = 0
        threes_attempted = 0
        fg_made = 0
        fg_attempted = 0
        ft_made = 0
        ft_attempted = 0
        blks_and_reb = 0
        to_and_stl = 0
        for player in game["game"]:
            fg_made += player[0]
            fg_attempted += player[1]
            threes_made += player[2]
            threes_attempted += player[3]
            ft_made += player[4]
            ft_attempted += player[5]
            blks_and_reb += player[6]+player[7]
            to_and_stl += player[8]+player[9]

        threeP = 100*threes_made/threes_attempted
        fgP = 100*fg_made/fg_attempted
        ftP = 100*ft_made/fg_attempted
        outdict[game["date"]] = [fgP,threeP,ftP,blks_and_reb,to_and_stl,game["pts"]]

    integrate(outdict)


def integrate(outdict=None):
    if outdict==None:
        with open("Ready.json") as json_data:
            outdict = json.load(json_data)
            json_data.close()
    dates=outdict.keys()
    values=outdict.values()
    wolves = None
    with open("WolvesTeamStats.json") as full_data:
        wolves = json.load(full_data)
        full_data.close()
    # wolves["Dates"] = [dates[i] for i in range(len(dates)-1,-1,-1)]+wolves["Data"]
    ind = len(wolves["Stats"])
    for d in dates:
        dict = {d:ind}
        dict.update(wolves["Date_Indexes"])
        wolves["Date_Indexes"] = dict
        ind+=1
    wolves["Stats"] += values
    with open("WolvesTeamStats.json",'w') as file:
        json.dump(wolves,file,indent=4)
        file.close()

# integrate()
#turn_to_dict("RawData.txt")
