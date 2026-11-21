# hi fam this is an optimized automated program so we can 
# reduce the cost of like weather and power grids and stuff

import socket
import json
HOST = socket.gethostname()
PORT = 8800

def convJsonToList(data):
    loads = {}
    randomEvent = data["random_event"]
    forecast = data["forecast"]
    for i,load in enumerate(data[loads]):
        loads[load[type] + str(i)] = load["load"]
    grid_price = data["grid_price"]
    return randomEvent, forecast, loads, grid_price
    

def sendJSON(s: socket.socket, dataToSend: dict):
    msg = json.dumps(dataToSend).encode("utf-8")
    s.sendall(msg)    

def recvJSON(s: socket.socket):
    msg = s.recv(1024)
    IncData = json.loads(msg.decode("utf-8"))
    return IncData

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST,PORT))
    s.listen()
    conn, addr = s.accept()
    for hour in range(1,25):
        data = convJsonToList(recvJSON(s))
        length = len(data["loads"])
        totalPowerNeeded = sum(data["loads"][i]["load"] for i in range(length))
        print(totalPowerNeeded)  
        """ This is test code (lets hope marmoset connects or smth) """
