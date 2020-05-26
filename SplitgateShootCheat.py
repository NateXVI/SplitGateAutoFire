import tkinter as tk
import time
from PIL import ImageGrab
import numpy as np
from pynput.mouse import Button, Controller

print("Cheat Started")

# Enables or disables the cheat
isCheatRunning = True

# When true, mouse is pressed
buttonState = False

mouse = Controller()

# Counts number of times mouse is clicked
clicks = 0

# Class that is used to check and see if a gun should be fired
class GunCheck:
    def __init__(self, x=0.5, y=0.5, allowance = 0):
        # Scalar values that determine where on the screen the creen the color is being checked
        # Default is the center of the screen
        self.x = x
        self.y = y

        # True when the color of the screen when it is equal to self.color
        self.isShot = False

        # If false, the weapon will not be checked
        self.enabled = True

        # Color that the screen is compared to
        self.color = [255,0,0]

        # How many millisecons after the gun is not aiming at an enemy that it will still shoot
        self.allowance = allowance

        # The last time that the gun was aiming at an enemy
        self.time = 0

    # Method that checks to see if the gun should be shot
    def check(self, image):
        if (self.enabled):
            x = int(len(image[0]) * self.x)
            y = int(len(image) * self.y)
            # print(len(image[0]), len(image), x,y)
            screenColor = image[y][x]

            if (screenColor[0] == self.color[0] and screenColor[1] == self.color[1] and screenColor[2] == self.color[2]):
                self.isShot = True
                self.time = int(round(time.time() * 1000))
            else:
                # self.isShot = False
                if (int(round(time.time() * 1000)) - self.time >= self.allowance):
                    self.isShot = False
        else:
            self.shot = False

    # Toggles if the gun is enabled or disabled
    def toggle(self):
        self.enabled = not self.enabled
        return self.enabled

    # Changes the gunChecks allowance
    def setAllowance(self, allowance):
        self.allowance=float(allowance)
        # print(type(allowance))


# Defining each of the gun checks
rifle = GunCheck(0.5, 0.5, 10)
sniper = GunCheck(y=0.503)
pistol = GunCheck(y=0.5125)
shotgun = GunCheck(0.509, 0.535)
smg = GunCheck(0.5135,0.476,500)


# Function that checks each gun and then determines if the mouse should be clicked
def runCheat():
    global isCheatRunning
    global buttonState
    global clicks
    global rifle
    global sniper
    global pistol
    global shotgun
    global smg

    if isCheatRunning:
        # Capture the screen and then turn it into an array
        screen = ImageGrab.grab()
        screen = np.asarray(screen)

        # Check each of the weapons (if the weapon is enabled)
        rifle.check(screen)
        sniper.check(screen)
        pistol.check(screen)
        shotgun.check(screen)
        smg.check(screen)

        # If any of the weapons should be shot...
        if (rifle.isShot or sniper.isShot or pistol.isShot or shotgun.isShot or smg.isShot):
            # ... and the mouse is not pressed, then press the mouse in and add 1 to clicks
            if (not buttonState):
                buttonState = True
                mouse.press(Button.left)
                clicks += 1

        else:
            # If none of the guns should be shot and the mouse is pressed then release the mouse
            if (buttonState):
                buttonState = False
                mouse.release(Button.left)

    # If the cheat is not enabled...
    else:
        # ...and the mouse is pressed, then release the mouse
        if (buttonState):
                buttonState = False
                mouse.release(Button.left)

# Function that runs the cheat, and then reschedules it to be ran in 10ms
def cheatLoop():
    runCheat()
    root.after(10, cheatLoop)
    # print(smg.allowance, rifle.allowance)


# Toggles if the cheat is on or off and changes the text at the top of the app
def toggleCheat():
    global isCheatRunning
    isCheatRunning = not isCheatRunning

    if isCheatRunning:
        cheatStatusLabel['text'] = "CHEAT RUNNING"

    else:
        cheatStatusLabel['text'] = "CHEAT NOT RUNNING"


# Make a window
root = tk.Tk()
root.geometry = "100x800"
root.resizable(width=False, height=False)
root.title("Splitgate Auto-fire Cheat")

# Create lables that says if the cheat is enabled or not, and makes the button that toggles the cheat 
cheatStatusLabel = tk.Label(root, text="CHEAT RUNNING", padx=1, pady=3)
toggleCheatButton = tk.Button(root, text="TOGGLE CHEAT", command=toggleCheat,padx=60, pady=3)

# Makes the check button for the rifle, and the slider that changes its allowance
rifleCheckbutton = tk.Checkbutton(root, text="RIFLE", command=rifle.toggle)
rifleCheckbutton.select()
rifleSlider = tk.Scale(root,from_=0,to=1000, length=200, orient=tk.HORIZONTAL, label="RIFLE ALLOWANCE (ms)",command=rifle.setAllowance)
rifleSlider.set(0)

# Makes the check button for the sniper
sniperCheckbutton = tk.Checkbutton(root, text="SNIPER", command=sniper.toggle)
sniperCheckbutton.select()

# Makes the check button for the pistol
pistolCheckbutton = tk.Checkbutton(root, text="PISTOL", command=pistol.toggle)
pistolCheckbutton.select()

# Makes the check button for the shotgun
shotgunCheckbutton = tk.Checkbutton(root, text="SHOTGUN", command=shotgun.toggle)
shotgunCheckbutton.select()

# Makes the check button for the SMG, and the slider that changes its allowance
smgCheckbutton = tk.Checkbutton(root, text="SMG", command=smg.toggle)
smgCheckbutton.select()
smgSlider = tk.Scale(root,from_=0,to=1000, length=200, orient=tk.HORIZONTAL, label="SMG ALLOWANCE (ms)",command=smg.setAllowance)
smgSlider.set(500)

# Places all the lable, buttons, and sliders on the app
cheatStatusLabel.pack()
toggleCheatButton.pack()
rifleCheckbutton.pack()
sniperCheckbutton.pack()
pistolCheckbutton.pack()
shotgunCheckbutton.pack()
smgCheckbutton.pack()
rifleSlider.pack()
smgSlider.pack()

# runs the cheat
cheatLoop()

# tkinter app loop that keeps the app running
root.mainloop()
