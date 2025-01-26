# Audio modules
from tkinter import font
import tkinter
from modules.audio import AudioRecorder, detect_barks, get_templates, playFile, recordFile
from modules.config import Configuration
from modules.shock import Shocker, shock
from modules.templates import TemplateCalibration
from modules.tracking import ShockTracker

# tkinter
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

import time
from pynput.keyboard import Listener
recorder = AudioRecorder()
recorder.start_recording()

root = tk.Tk()
root.title("BarkDetector")
style = ttk.Style()
style.theme_use('darkly') 

tab_control = ttk.Notebook(root) 

tracker = ShockTracker(tab_control)
calibration = TemplateCalibration(tab_control) 
config = Configuration(tab_control) 
shocker = Shocker(tab_control)

# Add tabs for various settings.
tab_control.add(tracker.frame, text ='Tracking') 
tab_control.add(calibration.frame, text ='Templates') 
tab_control.add(config.frame, text ='Config') 
tab_control.add(shocker.frame, text ='Shock') 
tab_control.pack(expand = 1, fill ="both") 

root.geometry("400x300")

calibration.loadTemplates()

timePassed = -round(calibration.maxLength,1)
peaked = False

shockTimer = -1.

def activateShock():
    global shockTimer
    if shockTimer < 0:
        shockTimer = config.shock_countdown
    

def keyPress(key):
    key = str(key)
    if(key.endswith("\'")):
        key = key[1]
    if(key == f"{config.hotkey}"):
        activateShock()

def sendShock():
    tracker.trackBox.insert(0, f"{shocker.operation} [lvl {shocker.intensity}, {shocker.duration} secs] activated.")
    if(shocker.model != "PiShock"):
        shock("OpenShock", shocker.intensity, shocker.duration, shocker.operation)
    if(shocker.model != "OpenShock"):
        shock("PiShock", shocker.intensity, shocker.duration, shocker.operation)

listener = Listener(on_press=keyPress)
listener.start()
try:
    while(True):
        time.sleep(0.05)
        if(shockTimer >= 0):
            if(shockTimer % 1 == 0 and shockTimer != 0):
                tracker.trackBox.insert(0, f"{shockTimer} seconds left until shock.")
            shockTimer = round(shockTimer - 0.05, 2)
            if(shockTimer == 0):
                sendShock()
            

        config.updateConfig()
        shocker.updateConfig()
        timePassed = round(timePassed + 0.05, 2)

        tracker.decibelMeter["value"] = recorder.db/150
        if(recorder.db / 150 > config.soundThreshold * 100):
            peaked = True

        if(peaked and timePassed % 1.5 == 0):
            peaked = False
            num_match = detect_barks(recorder, calibration.templates, calibration.maxLength, config.peak_th)
            if(num_match >= config.check_num):
                tracker.trackBox.insert(0, f"Bark Detected : {{{num_match} / {config.check_num}}} tests passed.")
                if(config.barkMode.get()):
                    sendShock()
                elif(shockTimer > 0):
                    tracker.trackBox.insert(0, f"Shock averted with {shockTimer} seconds left.")
                    shockTimer = -1
            elif(config.speakMode.get()):
                tracker.trackBox.insert(0, f"Non-Bark Detected : {{{num_match} / {config.check_num}}} tests passed.")
                sendShock()
            elif(num_match > 0):
                tracker.trackBox.insert(0, f"Potential Bark Detected : {{{num_match} / {config.check_num}}} tests passed.")
            else:
                tracker.trackBox.insert(0, f"Sound Detected : {{{num_match} / {config.check_num}}} tests passed.")

        
        root.update_idletasks()
        root.update()

except (KeyboardInterrupt, tkinter.TclError) as e:
    recorder.stop_recording()
    exit()