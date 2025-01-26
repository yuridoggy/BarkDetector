import os
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from modules.audio import get_templates, playFile, recordFile

class TemplateCalibration:
    def __init__(self, tab_control):
        self.frame = ttk.Frame(tab_control) 

        self.calBox = tk.Listbox(self.frame)
        self.calBar = tk.Scrollbar(self.calBox)
        self.calBar.pack(side=RIGHT, fill=BOTH)
        self.calBar.config(command = self.calBox.yview) 
        self.calBox.place(x=25, y=15, width=225, height=235)
        self.calBox.config(yscrollcommand = self.calBar.set) 

        self.templates, self.maxLength = get_templates()

        self.fileBtn = tk.Button(self.frame, text = 'Open Folder', command = self.openSrc) 
        self.fileBtn.place(x=275, y=15, width=75)

        self.loadBtn = tk.Button(self.frame, text = 'Refresh', command = self.loadTemplates) 
        self.loadBtn.place(x=275, y=40, width=75)

        self.playBtn = tk.Button(self.frame, text = 'Play File', command = self.playTemplate) 
        self.playBtn.place(x=275, y=65, width=75)

        self.delBtn = tk.Button(self.frame, text = 'Delete File', command = self.delTemplate) 
        self.delBtn.place(x=275, y=90, width=75)

        self.recBtn = tk.Button(self.frame, text = 'Record', command = self.recordTemplate) 
        self.recTime = ttk.Progressbar(self.frame)
        self.recTime.place(x=275, y=140, width=75)
        self.recBtn.place(x=275, y=115, width=75)

    def loadTemplates(self):
        self.calBox.delete(0, self.calBox.size())
        for filename in os.listdir('templates/'):
            if(filename.endswith('.wav')):
                self.calBox.insert(0, filename)
        self.templates, self.maxLength = get_templates()
    

    def delTemplate(self):
        filename = self.calBox.get(self.calBox.curselection())
        target_name = f"templates/{filename}"
        os.remove(target_name)
        self.loadTemplates()

    def playTemplate(self):
        filename = self.calBox.get(self.calBox.curselection())
        target_name = f"templates/{filename}"
        playFile(target_name)

    def openSrc(self):
        path = "templates"
        path = os.path.realpath(path)
        os.startfile(path)

    def recordTemplate(self):
        self.recTime["value"] = 100
        self.frame.update()
        recordFile()
        self.loadTemplates()
        self.recTime["value"] = 0
        self.frame.update()