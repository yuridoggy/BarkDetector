This program is made for activating a shock collar if a bark is not detected within a certain time after a button press (or voice command).

It works with both OpenShock and PiShock, utilizing their public API's.

The program is currently set by default to use the PAUSE BREAK key as a hotkey, which can be changed in it's configuration file. This is meant to be triggered by VoiceAttack, a free speech recognition software meant to start the shock countdown.

# Documentation

## Setting up the Software

Inside this project is the uncompiled version of this project, with main.py. The compiled version is available for download [here](https://www.patreon.com/posts/bark-detector-v1-120159942).

Once you have the project downloaded/compiled, a window will pop up that looks like this.

From here, we can move on to setting it up to detect your barks.

## Templates

Heading over to the templates tab, you'll be greeted by a file display and various settings.

The open folder will just open the directory where files will be stored, and refresh is if you are manually adding .wav files there.

Play and Delete File function based on selecting existing files in the display, but currently there are none there.

The Record button will allow you to easily create your own bark template. Upon clicking it, the bar below will turn blue, and you will have one second to bark/make a noise. (This seems sort, but it's plenty of time.)

After you do that, a new file will pop up. Make sure to click on it and press play to make sure you're happy with it.

If you aren't happy with it, or it's been cut off, delete it. From here, you want to record a few of these so the program has more to work off of. I personally suggest 6.

## Config

Opening up the config tab you will be greeted with various settings.

From here, the settings on the left are regarding the sensitivity of bark detection, where the right is regarding the shocking aspect.

**Template Threshold**
- This is how accurate your bark has to be compared to the template files you just recorded.
- I suggest 0.6 for a start, increasing or decreasing based on microphone quality and testing.
- The Tracking tab will show how many are triggered. If you are barking and if the number of templates triggering is lower than expected, decrease the threshold. If it is giving you false positives, increase it.

**Templates Needed**
- As opposed to Threshold, this regards how many templates must be matched for a bark to be detected.
- Depending on the "types" of barks that are in your templates, this can be a variety of numbers. If you just bark one way, I would suggest setting this to 1 or 2 below the number of templates.

**Shock Hotkey**
- By default this is Key.pause, as it's a key not many people press by accident. This is the key that starts the countdown to a shock. You can change this to any key, but if you use something like the Home key, you need to add Key. before it.

**Shock Countdown**
- Number of seconds before a shock is triggered upon pressing the hotkey. If set to 0, it's instant.

**Shock Intensity**
- From 0-100, the intensity of the selected operation. Only whole numbers.
- Work up from low, if you haven't used a shock collar before.

**Duration**
- From 0.3-15 on PiShock, 0.3-30 on OpenShock. The number of seconds that a shock/operation will last upon being triggered. Accepts decimals.

**Operation**
- Default is shock, but can be set to Vibrate or Beep if you want to do something lighter. Changes the shock to either vibrate or make a beeping noise on the shock collar.

**Model**
- Default is both, but can be set to only PiShock or OpenShock. Sends a signal to either of their servers depending on which one.

## OpenShock / PiShock
Once you've gone through all the above, you'll need to open up config.yaml in order to set up the API keys for either OpenShock or Pishock. You can open this file with a notepad editor, and it contains all of the above's default settings. Change them here if you want them to be those values on startup.

The highlighted sections are what we're interested in. The yellow for OpenShock, and red for PiShock.

**OpenShock**

For OpenShock, you'll need an API key and Shocker ID.

You can get the API key [here](https://openshock.app/#/dashboard/tokens). Simply copy the token and paste it between the quotation marks.

For "ShockerIds", you can put multiple shockers. It will send signals to all of them. To get them, go [here](https://openshock.app/#/dashboard/shockers/own) and select your shocker. Click edit.

A menu will pop up. Simply copy the ID shown and paste it between the quotation marks. To add more, add a comma and paste another ID.

Make sure to save the file!

**PiShock**

For Username, you just want to put in the username you log into PiShock with. It can also be found [here](https://pishock.com/#/account).

For me, it would be Atra.

[Here](https://pishock.com/#/account), you can also generate an API key. Copy it and paste it into the config.

The last thing we need is the code. From [here](https://pishock.com/#/control), click Share.

Click **+ CODE** from the screen you see, and you will get the code.
