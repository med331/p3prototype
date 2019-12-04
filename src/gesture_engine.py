"""
    GestureEngine must analyze a webcam for user gestures
"""
import sys
import cv2
import numpy as np


class GestureEngine:

    def __init__(self):
        self.hands = []
        self.is_holding_turtle = False
        self.middle_point = (sys.maxsize, sys.maxsize)
        self.two_hands_in_frame = len(self.hands) == 2

    def process_frame(self, frame):
        frame = cv2.flip(frame, flipCode=1)
        centers = []
        # Our operations on the frame come here
        # background subtraction
        hsv = frame
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

        # Colour threshholding
        lower_blue = np.array([38, 50, 50])
        upper_blue = np.array([75, 255, 255])
        hsv = cv2.inRange(hsv, lower_blue, upper_blue)

        hsv = cv2.medianBlur(hsv, 9)

        hsv = cv2.dilate(hsv, None, iterations=3)

        #cv2.imshow("thresh", hsv)

        # find blue object above certain size and draw a box around them
        cnt = cv2.findContours(hsv.copy(), cv2.RETR_CCOMP,
                               cv2.CHAIN_APPROX_TC89_KCOS)[1]
        for c in cnt:
            if cv2.contourArea(c) > 800:

                (x, y, w, h) = cv2.boundingRect(c)
                self.hands.append(Hand(x, y, w, h))
                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centers.append([cx, cy])
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            else:
                pass
        if len(centers) >= 2:
            dx = centers[0][0] - centers[1][0]
            dy = centers[0][1] - centers[1][1]
            d = np.sqrt(dx * dx + dy * dy)
            col = (0, 0, 255)
            if d < 250 and dy < 25:
                col = (0, 255, 0)
                self.is_holding_turtle = True
            else:
                self.is_holding_turtle = False
                col = (0, 0, 255)
            cv2.line(frame, (centers[0][0], centers[0][1]), (centers[1][0], centers[1][1]), col, 5)
            cv2.circle(frame, (int((centers[0][0] + centers[1][0]) / 2), int((centers[0][1] + centers[1][1]) / 2)), 10,
                       col, -1)
            self.middle_point = (int((centers[0][0] + centers[1][0]) / 2),
                                 int((centers[0][1] + centers[1][1]) / 2))

        return frame


class Hand:

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
