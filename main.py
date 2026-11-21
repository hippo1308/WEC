# hi fam this is an optimized automated program so we can 
# reduce the cost of like weather and power grids and stuff

import socket
import json
HOST = "127.0.0.1"
PORT = 8800
batteryCharge = 0
generator = 0

event = ""
forecast = ""
buildings = []
price = 0
hour = 0

def convJsonToList(data):
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
        i += 1



def reactToForecast():  #Based on current battery charge, time of day, and predicted weather, run the generator
    global generator
    global hour
    totalPowerNeeded = sum(buildings[i]["load"] for i in range(len(buildings)))
    available_charge = max(0, int(100-batteryCharge))
    
    #dont charge if hour is 20 or higher, #dont charge if the event is generator 
    if hour>=22 or event == "generator_failure":
        generator= 0
        # at this point (>22 hours) demand is low
        # use solar power and battery charge
        distributePower(200, "solar") 
        distributePower(batteryCharge, "battery") 
   
    #available charge to be filled is 100-battery charge
    
    #if the forcast is cloudy, estimate the stored eng saving, and account for accuracy

    if forecast == "cloudy_weather":
        cloudy_prob = 0.75
    else:
        cloudy_prob = 0.25

    solarLoad = sum(i["load"] for i in buildings if i['type'] != "lecture_hall")

    #electriicity needed from the battery if cloudy 
    cloudyNeed = totalPowerNeeded

    #electricity when no clouudy
    noCloudyNeed = totalPowerNeeded- min(200, solarLoad)

    estimated_price = price

    for i in range(available_charge):
        numberOfUnit = batteryCharge + i +1

        if numberOfUnit <= noCloudyNeed:
            probUsed = 1.0
        elif numberOfUnit <= cloudyNeed:
            probUsed = cloudy_prob

        else:
            break

        expectedSavings = probUsed*estimated_price

        if expectedSavings>1.0:
            generator +=1
        else:
            break
    return generator

def eventRestrictions():
    if price < 1: #if grid price is below a dollar, use the grid and ditch the battery
        if event == "cloudy_weather":
            distributePower(100000,"grid")
        else:
            distributePower(200, "solar")
            distributePower(100000,"grid")
    # if cloudy weather, solar panel cant be used
        # redistribute --> use battery mostly
    elif event == "cloudy_weather":
        distributePower(batteryCharge,"battery")
        distributePower(100000,"grid")    
        
    # if "generator_failure" Generator can't be used
        # redistribute --> use mostly solar and battery
    elif event == "generator_failure":
        distributePower(200, "solar")     
        if batteryCharge > 0: 
            #use battery for the rest
            distributePower(batteryCharge, "battery")
        else:
            #use grid
            distributePower(10000, "grid")
        
    # if battery failure, battery can't be used
    elif event == "battery_failure":
        # redistribute --> use solar + grid
        distributePower(200, "solar")
        distributePower(100000,"grid")
    
    # if grid failure, grid can't be used
        #redistribute --> solar + battery
    elif event == "grid_failure":
        distributePower(200, "solar")
        distributePower(batteryCharge, "battery")


def compresscurrentData():
    global buildings
    dataToSend = {"buildings":[]}
    for building in buildings:
        dataToSend["buildings"].append({"solar":building["solar"], "battery": building["battery"], "grid": building["grid"]})
    dataToSend["generator"] = generator
    return dataToSend


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST,PORT))
    print("socket connected!!!", flush = True)
    conn, addr = s.accept()
    for hour in range(24):
        convJsonToList(recvJSON(s))
        eventRestrictions()
        batteryCharge += generator
        generator = 0
        sendJSON(s,compresscurrentData())
        

