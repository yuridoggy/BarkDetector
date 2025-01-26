import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

class ShockTracker:
    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control) 

        # style="bar.Horizontal.TProgressbar"
        self.decibelMeter = ttk.Progressbar(self.frame)
        self.decibelMeter.place(x=25, y=230, width=350)

        # List box for Bark Tracking, displaying details about when a bark is detected, as well as the welcome message.
        self.trackBox = tk.Listbox(self.frame)
        self.trackBar = tk.Scrollbar(self.trackBox)
        self.trackBar.pack(side=RIGHT, fill=BOTH)
        self.trackBar.config(command = self.trackBox.yview) 
        self.trackBox.place(x=25, y=15, width=350, height=200)
        self.trackBox.config(yscrollcommand = self.trackBar.set) 

        self.trackBox.insert(0, "Welcome to BarkDetector!")
        self.trackBox.insert(1, "This is a project made by Atra (yuridoggy) on BlueSky.")
