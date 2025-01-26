import tkinter as tk
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# Config modules
import ruamel.yaml

class Configuration:
    def __init__(self, tab_control):
        # Read config file
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open('config.yaml') as f:
            self.config = yaml.load(f)

        self.peak_th = self.config['threshold']
        self.check_num = self.config['check_num']
        self.hotkey = self.config['hotkey']
        self.shock_countdown = self.config['shock_countdown']
        self.soundThreshold = self.config['sound_threshold']

        self.frame = ttk.Frame(tab_control) 

        self.thresholdLabel = tk.Label(self.frame, text="Template Threshold [0, 1]", anchor="w")
        self.thresholdLabel.place(x=25, y=15, width=150, height=25)

        self.neededLabel = tk.Label(self.frame, text="Templates Needed [0, infin)", anchor="w")
        self.neededLabel.place(x=25, y=75, width=150, height=25)

        self.hotkeyLabel = tk.Label(self.frame, text="Shock Hotkey", anchor="w")
        self.hotkeyLabel.place(x=200, y=15, width=250, height=25)

        self.countdownLabel = tk.Label(self.frame, text="Shock Countdown", anchor="w")
        self.countdownLabel.place(x=200, y=75, width=250, height=25)

        self.thresholdLabel = tk.Label(self.frame, text="Sound Threshold [0, 1]", anchor="w")
        self.thresholdLabel.place(x=25, y=135, width=150, height=25)

        vcmd = (self.frame.register(self.thresholdCallback))
        self.templateThresholdCheck = tk.Entry(self.frame, validate='all', validatecommand=(vcmd, '%P')) 
        self.templateThresholdCheck.insert(0, self.peak_th)
        self.templateThresholdCheck.place(x=25, y=40, width=75, height=25)

        ccmd = (self.frame.register(self.checkCallback))
        self.templateNumCheck = tk.Entry(self.frame, validate='all', validatecommand=(ccmd, '%P')) 
        self.templateNumCheck.insert(0, self.check_num)
        self.templateNumCheck.place(x=25, y=100, width=75, height=25)

        self.hotkeyEntry = tk.Entry(self.frame) 
        self.hotkeyEntry.insert(0, self.hotkey)
        self.hotkeyEntry.place(x=200, y=40, width=75, height=25)

        scmd = (self.frame.register(self.shockCallback))
        self.shockNumCheck = tk.Entry(self.frame, validate='all', validatecommand=(scmd, '%P')) 
        self.shockNumCheck.insert(0, self.shock_countdown)
        self.shockNumCheck.place(x=200, y=100, width=75, height=25)

        vcmd = (self.frame.register(self.thresholdCallback))
        self.soundThresholdCheck = tk.Entry(self.frame, validate='all', validatecommand=(vcmd, '%P')) 
        self.soundThresholdCheck.insert(0, self.soundThreshold)
        self.soundThresholdCheck.place(x=25, y=160, width=75, height=25)

        self.barkMode = tk.IntVar(value=self.config["shock_on_bark"])
        self.checkBark = tk.Checkbutton(self.frame, text="Shock on Bark", variable=self.barkMode)
        self.checkBark.place(x=25, y=210)

        self.speakMode = tk.IntVar(value=self.config["shock_on_speak"])
        self.checkSpeak = tk.Checkbutton(self.frame, text="Shock on Speak", variable=self.speakMode)
        self.checkSpeak.place(x=200, y=210)



    def updateConfig(self):
        yaml = ruamel.yaml.YAML()
        yaml.preserve_quotes = True
        with open('config.yaml') as f:
            self.config = yaml.load(f)

        self.config["shock_on_bark"] = (self.barkMode.get() == True)
        self.config["shock_on_speak"] = (self.speakMode.get() == True)

        if(self.templateThresholdCheck.get() == ""):
            self.peak_th = self.config["threshold"]
        else:
            self.peak_th = float(self.templateThresholdCheck.get())
            self.config["threshold"] = self.peak_th

        if(self.soundThresholdCheck.get() == ""):
            self.soundThreshold = self.config["sound_threshold"]
        else:
            self.soundThreshold = float(self.soundThresholdCheck.get())
            self.config["sound_threshold"] = self.soundThreshold

        if(self.templateNumCheck.get() == ""):
            self.check_num = self.config["check_num"]
        else:
            self.check_num = int(self.templateNumCheck.get())
            self.config["check_num"] = self.check_num

        if(self.shockNumCheck.get() == ""):
            self.shock_countdown = self.config["shock_countdown"]
        else:
            self.shock_countdown = max(float(self.shockNumCheck.get()), 0.25)
            self.config["shock_countdown"] =  self.shock_countdown
        
        if(self.hotkeyEntry.get() == "" or len(self.hotkeyEntry.get()) > 1):
            self.hotkey = self.config['hotkey']
        else:
            self.hotkey = self.hotkeyEntry.get()
            self.config['hotkey'] = self.hotkey

        with open("config.yaml", "w") as f:
            yaml.dump(self.config, f)


    def thresholdCallback(self, P):
        try:
            if  P == "" or 0 <= float(P) <= 1:
                return True
            else:
                return False
        except ValueError:
            return False

    def checkCallback(self, P):
        if  (P == "" or  (str.isdigit(P) and int(P) > 0)):
            return True
        else:
            return False

    def shockCallback(self, P):
        try:
            if  P == "" or 0 <= float(P):
                return True
            else:
                return False
        except ValueError:
            return False  