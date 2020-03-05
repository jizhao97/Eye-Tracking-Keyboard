import cv2
import numpy as np
import gazeTracking as gt
import eyeTrackingKeyboard as kb
import time

cap = cv2.VideoCapture(0)

histV = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
histH = np.array([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
timeScale = np.array([0.5, 0.5, 0.5, 0.6, 0.6, 0.7, 0.9, 1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.6])

topBound = 0
botBound = 0
leftBound = 0
rightBound = 0

top = None
bot = None
midh = None
midv = None
right = None
left = None

lastVdir = 0
lastHdir = 0
doneInit = False

first = True
lastButton = None

try:
    file = open("calibration.txt", 'r')
    line = file.read().splitlines()
    print(line)
    top = float(line[0])
    bot = float(line[1])
    midh = float(line[2])
    midv = float(line[3])
    right = float(line[4])
    left = float(line[5])
    file.close()
except:
    print("Calibration file invalid")


gui = kb.GUI()


while True:
    k = cv2.waitKey(1) & 0xFF
    _, img = cap.read()

    vL, hL, vR, hR, bR, bL = gt.gaze_position(img)

    if vL == 0 or vR == 0:
        continue

    vRatio = (vL + vR) / 2
    hRatio = (hL + hR) / 2

    histV = np.append(histV, vRatio)
    histH = np.append(histH, hRatio)

    if len(histV) > 15:
        histV = np.delete(histV, 0)

    if len(histH) > 15:
        histH = np.delete(histH, 0)

    smaV = np.mean(histV * timeScale)
    smaH = np.mean(histH * timeScale)

    cv2.putText(img, "vertRatio:" + str(int(smaV)), (50, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
    cv2.putText(img, "horRatio:" + str(int(smaH)), (50, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

    if bL == True and not (bR == True and bL == True):
        cv2.putText(img, "LeftBlink", (50, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        while bL == True:
            _, img2 = cap.read()
            _, _, _, _, bR, bL = gt.gaze_position(img2)
        gui.button_click(lastButton, -1, False)

    if bR == True and not (bR == True and bL == True):
        cv2.putText(img, "RightBlink", (250, 300), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        while bR == True:
            _, img2 = cap.read()
            _, _, _, _, bR, bL = gt.gaze_position(img2)
        gui.button_click(lastButton, 1, False)

    if k == ord('w'):
        top = smaV
        print(top)
    elif k == ord('s'):
        bot = smaV
        print(bot)
    elif k == ord('a'):
        left = smaH
        print(left)
    elif k == ord('d'):
        right = smaH
    elif k == ord('f'):
        midh = smaH
        midv = smaV
        print(midh)


    if top is not None and bot is not None and left is not None and right is not None and midh is not None and midv is not None:
        #print("done init")
        doneInit = True

        if topBound == 0:
            topBound = midv + abs(top - midv) * 0.5
            botBound = midv - abs(bot - midv) * 0.5
            rightBound = midh + abs(right - midh) * 0.5
            leftBound = midh - abs(left - midh) * 0.5

    if doneInit:
        if smaV > topBound:
            lastVdir = smaV - topBound
            cv2.putText(img, "up", (50, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        elif smaV >= botBound:
            lastVdir = 0
            cv2.putText(img, "mid", (50, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            lastVdir = smaV - botBound
            cv2.putText(img, "down", (50, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        if smaH > rightBound:
            lastHdir = smaH - rightBound
            cv2.putText(img, "right", (200, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        elif smaH >= leftBound:
            lastHdir = 0
            cv2.putText(img, "mid", (200, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        else:
            lastHdir = smaH - leftBound
            cv2.putText(img, "left", (200, 250), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)

        if abs(lastVdir * 1.2) > abs(lastHdir):
            if lastVdir > 0:
                lastButton = 1
            elif lastVdir < 0:
                lastButton = 7
        else:
            if lastHdir > 0:
                lastButton = 5
            elif lastHdir < 0:
                lastButton = 3

        if lastVdir == 0 and lastHdir == 0:
            lastButton = 4

        if lastButton != None and first == False:
            gui.button_click(lastButton, 0, True)

        first = False;

    cv2.imshow("cap", img)

    if k == ord('q'):
        gui.callback()
        break

    elif k == ord('p'):
        while True:
            k = cv2.waitKey(1) & 0xFF
            if k == ord('p'):
                break;

file = open("calibration.txt", 'w')
file.write(str(top) + '\n')
file.write(str(bot) + '\n')
file.write(str(midh) + '\n')
file.write(str(midv) + '\n')
file.write(str(right) + '\n')
file.write(str(left))
file.close()

cap.release()
cv2.destroyAllWindows()
