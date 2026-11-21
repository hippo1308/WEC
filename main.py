# hi fam this is an optimized automated program so we can 
# reduce the cost of like weather and power grids and stuff

import socket
import json
HOST = "127.0.0.1"
PORT = 8800
batteryCharge = 0
generator = 0

def convJsonToList(data):
    loads = {}
    global event
    global forecast
    global buildings
    global price
    event = data["random_event"]
    forecast = data["forecast"]
    price = data["grid_price"]
    buildings = []
    for building in data["loads"]:
        buildings.append({"type":building["type"], "load":building["load"] ,"solar":0,"battery":0,"grid":0,"met":False})
    

def sendJSON(s: socket.socket, dataToSend: dict):
    msg = json.dumps(dataToSend).encode("utf-8")
    s.sendall(msg)    

def recvJSON(s: socket.socket):
    msg = s.recv(1024)
    IncData = json.loads(msg.decode("utf-8"))
    return IncData

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print("socket connected!!!", flush = True)
    conn, addr = s.accept()
    for hour in range(24):
        data = convJsonToList(recvJSON(s))
        event = data[0]
        forecast = data[1]
        price = data[3]
        loads = data[2]
        length = len(data[2]["loads"])
        totalPowerNeeded = sum(loads[i]["load"] for i in range(length))
        print(totalPowerNeeded)  
        """ This is test code (lets hope marmoset connects or smth) """


def distributePower(max, pType):
    buildingNum = len(buildings)
    i = 0
    toDistribute = max
    while ((toDistribute) and (i < buildingNum)):
        if(((pType == "solar") and (buildings[i]["type"] != "lecture_hall")) or (pType != "solar")):
            #Distribute Solar until 200 cap is reached
            if (buildings[i]["met"] == False):
                buildingLoad = buildings[i]["load"] - buildings[i]["solar"] - buildings[i]["battery"] - buildings[i]["grid"]
                if buildingLoad < toDistribute:
                    buildings[i][pType] = buildingLoad
                    buildings[i]["met"] = True
                    toDistribute -= buildingLoad
                else:
                    buildings[i][pType] = toDistribute
                    toDistribute = 0

def reactToForecast():
    if forecast == c


def eventRestrictions():
    if grid < 1: #if grid is below a dollar, use the grid and ditch the battery
        if event == "cloudy_weather":
            distributePower(100000,"grid")
        else:
            distributePower(200, "solar")
            distributePower(100000,"grid")
    # if cloudy weather, solar panel cant be used
        # redistribute --> use battery mostly
    if event == "cloudy_weather":
        distributePower(batteryCharge,"battery")
        distributePower(100000,"grid")    
        
    # if "generator_failure" Generator can't be used
        # redistribute --> use mostly solar and battery
    if event == "generator_failure":
        distributePower(200, "solar")     
        if batteryCharge > 0: 
            #use battery for the rest
            distributePower(100000, "battery")
        else:
            #use generator
            distributePower(, "grid")
             
    elif grid < 1:
        #use grid
        distributePower(100000,"grid")

        
    # if battery failure, battery can't be used
    if event == "battery_failure":
        distributePower(200, "solar")
        distributePower(100000,"grid")
        
   
        # redistribute --> use solar
    # if grid failure, grid can't be used
        #redistribute

    if event == "g"

