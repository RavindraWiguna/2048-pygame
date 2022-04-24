import cv2
import numpy as np


def nothing(x):
    pass

#to create windows with trackbar needed
def showTrackbar():
    #Create Trackbar
    cv2.namedWindow("Colors")
    cv2.createTrackbar("R", "Colors", 33, 255, nothing)
    cv2.createTrackbar("G", "Colors", 74, 255, nothing)
    cv2.createTrackbar("B", "Colors", 18, 255, nothing)


showTrackbar()
isRunning = True
last_name = ""
cur_name = ""
while isRunning:
    b = cv2.getTrackbarPos("B", "Colors")
    g = cv2.getTrackbarPos("G", "Colors")
    r = cv2.getTrackbarPos("R", "Colors")

    frame = np.full((128, 128, 3), (b, g, r), np.uint8)
    last_name = cur_name
    cur_name = f'{hex(r)[2:]}{hex(g)[2:]}{hex(b)[2:]}'
    cv2.imshow("hai", frame)
    k = cv2.waitKey(1) & 0xFF
    #to close the loop
    if k == 27:
        cv2.destroyAllWindows()
        break
    else:
        cv2.destroyWindow(last_name)

    print(cur_name)