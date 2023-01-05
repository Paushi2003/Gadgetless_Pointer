import cv2
import mediapipe
import numpy as np

# from autopy.mouse import LEFT_BUTTON,RIGHT_BUTTON
import time
from math import sqrt

import pyautogui
import math
from plyer.utils import platform
from plyer import notification
from flask import Flask



#TO track the functions happening
process=[]
f1= 1#f1 pointer control
f2= 2#f2 left click
f3= 3#f3 right click
f4= 4#f4 drag and drop
f5= 5#f5 scrolling down
f6= 6#f6 scrolling up
f7= 7#Exit

flag=0

cap = cv2.VideoCapture(0)

# Initializing mediapipe
initHand = mediapipe.solutions.hands

# Object of mediapipe with "arguments for the hands module"
mainHand = initHand.Hands(max_num_hands=1,min_detection_confidence=0.8, min_tracking_confidence=0.8)

# Object to draw the connections between each finger index
draw = mediapipe.solutions.drawing_utils

# Outputs the high and width of the screen (1920 x 1080)
wScr, hScr = pyautogui.size()

pX, pY = 0, 0  # Previous x and y location
cX, cY = 0, 0  # Current x and y location

click=0

wCam, hCam = 640, 480
frameR = 100 # Frame Reduction
smoothening = 7

def handLandmarks(colorImg):
    landmarkList = []  # Default values if no landmarks are tracked

    # Object for processing the video input
    landmarkPositions = mainHand.process(colorImg)

    # Stores the out of the processing object (returns False on empty)
    landmarkCheck = landmarkPositions.multi_hand_landmarks

    if landmarkCheck:  # Checks if landmarks are tracked
        for hand in landmarkCheck:  # Landmarks for each hand

            # Loops through the 21 indexes and outputs their landmark coordinates (x, y, & z)
            for index, landmark in enumerate(hand.landmark):

                # Draws each individual index on the hand with connections
                draw.draw_landmarks(img, hand, initHand.HAND_CONNECTIONS)

                h, w, c = img.shape  # Height, width and channel on the image

                # Converts the decimal coordinates relative to the image for each index
                centerX, centerY = int(landmark.x * w), int(landmark.y * h)

                landmarkList.append([index, centerX, centerY])  # Adding index and its coordinates to a list

    return landmarkList

def findDistance(p1, p2, draw=True, r=15, t=3):
    x1, y1 = lmList[p1][1:]
    x2, y2 = lmList[p2][1:]
    cx, cy = (x1 + x2) // 2, (y1 + y2) // 2

    if draw:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), t)
        cv2.circle(img, (x1, y1), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), r, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (cx, cy), r, (0, 0, 255), cv2.FILLED)
    length = math.hypot(x2 - x1, y2 - y1)

    return length

def fingers(landmarks):
    fingerTips = []  # To store 4 sets of 1s or 0s
    tipIds = [4, 8, 12, 16, 20]  # Indexes for the tips of each finger

    # Check if thumb is up
    if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
        fingerTips.append(1)
    else:
        fingerTips.append(0)

    for id in range(1, 5):

        # Checks to see if the tip of the finger is higher than the joint
        if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

    return fingerTips

#***def paint():
    #Yet to enable paint function

def right_click():
    pyautogui.click(button='right')
    notification.notify(
        message='Right clicking...'
    )
    time.sleep(.3)

def left_click():
    pyautogui.click(button='left')
    notification.notify(
        message='Left clicking...'
    )
    time.sleep(.3)


app = Flask(__name__)

while True:
    check, img = cap.read()  # Reads frames from the camera
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Changes the format of the frames from BGR to RGB
    lmList = handLandmarks(imgRGB)
    # cv2.rectangle(img, (75, 75), (640 - 75, 480 - 75), (255, 0, 255), 2)

    if len(lmList) != 0:
        x1, y1 = lmList[8][1:]  # Gets index 8s x and y values (skips index value because it starts from 1)
        x2, y2 = lmList[4][1:]  # Gets index 12s x and y values
        x3, y3 = lmList[16][1:]  # Gets index 16s x and y values

        finger = fingers(lmList)  # Calling the fingers function to check which fingers are up

        if finger[1] == 1 and finger[0] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:  # Checks to see if the pointing finger is down and thumb finger is up

            # Converts the width of the window relative to the screen width
            X = np.interp(x1, (75, 640 - 340), (0, wScr))

            # Converts the height of the window relative to the screen height
            Y = np.interp(y1, (75, 480 - 280), (0, hScr))

            cX = pX + (X - pX) / smoothening  # Stores previous x locations to update current x location
            cY = pY + (Y - pY) / smoothening  # Stores previous y locations to update current y location

            # Function to move the mouse to the x3 and y3 values (wSrc inverts the direction)
            pyautogui.moveTo(wScr - cX, cY)

            cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
            # Stores the current x and y location as previous x and y location for next loop
            pX, pY = cX, cY

            #
            process.append(f1)

            if not(f1==process[len(process)-1] and f1==process[len(process)-2]) :
                # notification.notify(
                #     message='Pointer control...'
                # )
                # process.append(f1)
                pass


        if finger[1] == 1 and finger[2] == 1 and finger[0] == 0 and finger[3] == 0 and finger[4] == 0:  # Checks to see if the pointer finger is up and thumb finger is up
            #pyautogui.dragTo(X, Y, button='left')
            #autopy.mouse.toggle(down=True)
            #pyautogui.mouseDown(button='right', x=wScr-cX,y =cY)
            #time.sleep(0.3)
            # process.append(f4)
            # if not(f4==process[len(process)-1] and f4==process[len(process)-2]) :
            #     notification.notify(
            #         message='Drag...'
            #     )
            #     process.append(f4)
            pass


        # if finger[1] == 1 and finger[2] == 0:  # Checks to see if the pointer finger is up and thumb finger is up
        #     autopy.mouse.toggle(down=False) # Left click

        # Left clicking
        if finger[1] == 1 and finger[0] == 1 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:  # Checks to see if the pointer finger is down and thumb finger is up
             pyautogui.click(button='left', interval=0.25, clicks=1)
             # if not (f3 == process[len(process) - 1] and f3 == process[len(process) - 2]):
             #     notification.notify(
             #         message='Right clicking...'
             #     )
             #     process.append(f3)

        #Left clicking
        if finger[0] == 1 and finger[1] == 0 and finger[2] == 0 and finger[3] == 0 and finger[4] == 0:  # Checks to see if the pointer finger is down and thumb finger is up
             right_click()
             # if not (f2 != process[len(process) - 1] and f2 != process[len(process) - 2]):
             #     notification.notify(
             #         message='Left clicking...'
             #     )
             #     process.append(f2)

        # if finger[3] == 1 and finger[1] == 1 and finger[2] == 1 and finger[0] == 0 and finger[4] == 0:
        #       #pyautogui.screenshot()
        #     pass


        indexfingertip_x, indexfingertip_y= lmList[4][1:]
        thumbfingertip_x, thumbfingertip_y= lmList[8][1:]

        # Distance_x = sqrt(
        #     (indexfingertip_x - thumbfingertip_x) ** 2 + (indexfingertip_x - thumbfingertip_x) ** 2)
        # Distance_y = sqrt(
        #     (indexfingertip_y - thumbfingertip_y) ** 2 + (indexfingertip_y - thumbfingertip_y) ** 2)
        #
        # if Distance_x < 5 or Distance_x < -5:
        #     if Distance_y < 5 or Distance_y < -5:
        #         click = click + 1
        #         if click % 5 == 0:
        #             print("single click")
        #             autopy.mouse.click(delay=0.2)

        length = findDistance(4, 8)
        if length < 30:
            cv2.circle(img, (x1, y1),
                       15, (255, 0, 0), cv2.FILLED)
            #autopy.mouse.toggle(down=True)
            left_click()

        #To Scroll down
        if finger[0]==1 and finger[1]==1 and finger[2]==1 and finger[3]==1 and finger[4]==1:
            pyautogui.scroll(-50)
            # if not (f5 == process[len(process) - 1] and f5 == process[len(process) - 2]):
            #     notification.notify(
            #     message='Scrolling down...'
            #      )
            #     process.append(f5)

        # To Scroll up
        if finger[0]==0 and finger[1]==0 and finger[2]==0 and finger[3]==0 and finger[4]==0:
            pyautogui.scroll(50)
            # if not (f6 == process[len(process) - 1] and f6 == process[len(process) - 2]):
            #     notification.notify(
            #     message='Scrolling up...'
            #     )
            #     process.append(f6)

            #pyautogui.prompt("Scrolling Up...")


        if finger[0]==0 and finger[1]==1 and finger[2]==0 and finger[3]==0 and finger[4]==1:
            # if not (f7 == process[len(process) - 1] and f7 == process[len(process) - 2]):
            #     notification.notify(
            #     message='Exit'
            #     )
            #     process.append(f7)
            pyautogui.hotkey('ctrl', 'F2')


        #*** if finger[1] == 1 and finger[2] == 1:  # Checks to see if the pointer finger and middle finger are up
        #     autopy.mouse.toggle() # click and drag

    # if __name__ == '__main__':
    #     app

    cv2.imshow("Webcam", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break