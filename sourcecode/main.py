import keyboard
import numpy as np
from mss import mss
import cv2
import pyautogui

#scans a template image across the monitor screenshot capture and detects a correlation/match and clicks on the detection image
def imageDetect():
    print("\nrunning the program...")
    print("to quit the program press q\nto pause the program press p")
    sct = mss()
    threshold = .75
    is_paused = False
    monitor = {'top': 0, 'left': 0, 'width': 955, 'height': 540}
    dot_img = cv2.imread("dot.png", cv2.IMREAD_UNCHANGED)
    width = dot_img.shape[1]
    height = dot_img.shape[0]

    while True:
        scr_img = np.array(sct.grab(monitor))
        match = cv2.matchTemplate(scr_img, dot_img, cv2.TM_CCOEFF_NORMED)  # uses template matching correlation coefficient to find a match
        __ , max_val, __, max_loc = cv2.minMaxLoc(match)
        yloc,xloc = np.where(match >= threshold)
        if len(xloc) != 0 and len(yloc) != 0:
            xvalue = xloc[0] + 20                     # added 20 pixels to properly click the dots
            yvalue = yloc[0] + 20
            print("coordinates match found:({},{})".format(xvalue,yvalue))
        else:
            xvalue = None
            yvalue = None
        if max_val >= threshold:
             cv2.rectangle(scr_img, max_loc, (max_loc[0] + width, max_loc[1] + height), (0, 255, 255), 2)   # draw the image on the screen for the frame shown
        cv2.imshow('Screen', scr_img)
        cv2.waitKey(25)
        if xvalue and yvalue and not is_paused:
            pyautogui.click(x=xvalue,y=yvalue)
        if keyboard.is_pressed('q'):
            exit()
        if keyboard.is_pressed('p'):
            if is_paused:
                is_paused = False
            else:
                is_paused = True
def main():
    print("Welcome to image detection V1!\nTo start the program press s")
    keyboard.wait('s')
    imageDetect()

if __name__ == "__main__":
    main()
