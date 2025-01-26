import requests
import ruamel.yaml

import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

yaml = ruamel.yaml.YAML()
yaml.preserve_quotes = True
with open('config.yaml') as f:
    config = yaml.load(f)

shockDict = {
    "PiShock": {
        "url": "https://do.pishock.com/api/apioperate",
        "headers": {
            "Content-Type": "application/json",
            "accept": "application/json"
        },
        "Shock": "0",
        "Vibrate": "1",
        "Beep": "2",
    },
    "OpenShock": {
        "url": "https://api.openshock.app/2/shockers/control",
        "headers": {
            "Content-Type": "application/json",
            "OpenShockToken":config["OpenShockToken"],
            "accept": "application/json"
        },
        "Shock": "Shock",
        "Vibrate": "Vibrate",
        "Beep": "Sound",
        "e": "Stop"
    }
}


class Shocker:
    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control) 

        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open('config.yaml') as f:
            self.config = yaml.load(f)

        self.intensity = self.config['intensity']
        self.duration = self.config['duration']

        self.frame = ttk.Frame(tab_control) 

        self.intensityLabel = tk.Label(self.frame, text="Intensity", anchor="w")
        self.intensityLabel.place(x=25, y=15, width=150, height=25)

        self.durationLabel = tk.Label(self.frame, text="Duration", anchor="w")
        self.durationLabel.place(x=25, y=75, width=150, height=25)

        self.hotkeyLabel = tk.Label(self.frame, text="Operation", anchor="w")
        self.hotkeyLabel.place(x=200, y=15, width=250, height=25)

        self.durationLabel = tk.Label(self.frame, text="Model", anchor="w")
        self.durationLabel.place(x=200, y=75, width=150, height=25)


        vcmd = (self.frame.register(self.intensityCallback))
        self.intensityCheck = tk.Entry(self.frame, validate='all', validatecommand=(vcmd, '%P')) 
        self.intensityCheck.insert(0, self.intensity)
        self.intensityCheck.place(x=25, y=40, width=75, height=25)

        ccmd = (self.frame.register(self.durationCallback))
        self.durationCheck = tk.Entry(self.frame, validate='all', validatecommand=(ccmd, '%P')) 
        self.durationCheck.insert(0, self.duration)
        self.durationCheck.place(x=25, y=100, width=75, height=25)

        self.operationVar = tk.StringVar(self.frame)
        self.operationVar.set(self.config["operation"])
        options = ["Shock", "Vibrate", "Beep"]
        self.dropdown = tk.OptionMenu(self.frame, self.operationVar, *options)
        self.dropdown.place(x=200, y=40, width=75, height=25)

        self.modelVar = tk.StringVar(self.frame)
        self.modelVar.set(self.config["model"])
        options = ["OpenShock", "PiShock", "Both"]
        self.modeldrop = tk.OptionMenu(self.frame, self.modelVar, *options)
        self.modeldrop.place(x=200, y=100, width=75, height=25)


    def updateConfig(self):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open('config.yaml') as f:
            self.config = yaml.load(f)

        if(self.intensityCheck.get() == ""):
            self.intensity = self.config["intensity"]
        else:
            self.intensity = int(self.intensityCheck.get())
            self.config["intensity"] = self.intensity

        if(self.durationCheck.get() == ""):
            self.duration = self.config["duration"]
        else:
            self.duration = int(self.durationCheck.get())
            self.config["duration"] = self.duration

        self.operation = self.operationVar.get()
        self.config["operation"] = self.operation
        self.model = self.modelVar.get()
        self.config["model"] = self.model
        
        with open("config.yaml", "w") as f:
            yaml.dump(self.config, f)


    def intensityCallback(self, P):
        try:
            if  P == "" or 0 <= float(P) <= 100:
                return True
            else:
                return False
        except ValueError:
            return False

    def durationCallback(self, P):
        try:
            if  P == "" or 0.3 <= float(P) <= 15:
                return True
            else:
                return False
        except ValueError:
            return False



# Operations are "Shock", "Vibrate", "Beep", and "Stop"
# Duration is in seconds
def shock(shocker, intensity, duration, operation):
    data = {}
    if(shocker == "PiShock"):
        data = {
            "Intensity":intensity,
            "Duration":duration,
            "Code":config["Code"],
            "Apikey":config["Apikey"],
            "Op":shockDict[shocker][operation],
            "Hold":False,
            "Username":config["Username"],
            "Name":"Shock Bot"
        }
    if(shocker == "OpenShock"):
        data = {"shocks":[]}
        for i in config["ShockerIds"]:
            data["shocks"].append({})
            data["shocks"][-1]["id"] = i
            data["shocks"][-1]["type"] = shockDict[shocker][operation]
            data["shocks"][-1]["intensity"] = intensity
            data["shocks"][-1]["duration"] = duration * 1000

    # print(data)
    try:
        response = requests.post(shockDict[shocker]["url"], headers=shockDict[shocker]["headers"], json=data)
    except Exception:
        pass

# print(shock("PiShock", 3, 3, 'v'))