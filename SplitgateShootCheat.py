import time

import cv2
import mss
import numpy

from pynput.mouse import Button, Controller

print("cheat is running")

mouse = Controller()

buttonState = False

isRifleShot = False

sniperStreak = 0
sniperLimit = 3
isSniperShot = False


with mss.mss() as sct:
    rifleMonitor = {"top": 540, "left": 960, "width": 1, "height": 3}

    sniperMonitor = {"top": 537, "left": 960, "width": 1, "height": 1}

    while "Screen capturing":

        rifleImg = numpy.array(sct.grab(rifleMonitor))
        rifleCol = rifleImg[0][0]
        # print(rifleCol)

        if rifleCol[0] == 0 and rifleCol[1] == 0 and rifleCol[2] == 255:
            # print("rifle shot")
            isRifleShot = True

        elif rifleCol[0] != 0 or rifleCol[1] != 0:
            # print("rifle NOT shot")
            isRifleShot = False


        # sniperImg = numpy.array(sct.grab(rifleMonitor))
        # sniperCol = sniperImg[2][0]
        # print(sniperCol)
        sniperCol = rifleImg[2][0]

        if sniperCol[0] == 0 and sniperCol[1] == 0 and sniperCol[2] == 255:
            # print("rifle shot")
            sniperStreak += 1

        elif sniperCol[0] != 0 or rifleCol[1] != 0:
            # print("rifle NOT shot")
            isSniperShot = False
            sniperStreak = 0

        if sniperStreak > sniperLimit:
            isSniperShot = True


        if isRifleShot == True or isSniperShot == True:
            if buttonState == False:
                print("button pressed")
                mouse.press(Button.left)
                buttonState = True

        elif isRifleShot == False and isSniperShot == False and buttonState == True:
            print("button released")
            mouse.release(Button.left)
            buttonState = False