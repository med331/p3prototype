import sys
import cv2
import numpy as np


class GestureEngine:
    """
        THE CLASS THAT DETECTS HAND MOVEMENTS AND GESTURES
    """

    def __init__(self):
        self.hands = []                                 # list to hold the observed Hand objects in the frame
        self.is_holding_turtle = False                  # if it looks like the turtle is being held
        self.middle_point = (sys.maxsize, sys.maxsize)  # the middle point between the two hands
        self.two_hands_in_frame = False                 # whether or not there are exactly two hands in the frame

    def process_frame(self, frame):

        centers = []  # list to hold object centers

        frame = cv2.flip(frame, flipCode=1)  # flip the frame

        # convert to HSV
        hsv = frame
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

        # Colour threshholding
        lower_blue = np.array([38, 50, 50])
        upper_blue = np.array([75, 255, 255])
        hsv = cv2.inRange(hsv, lower_blue, upper_blue)

        hsv = cv2.medianBlur(hsv, 9)  # filter out noise

        hsv = cv2.dilate(hsv, None, iterations=3)

        # find green object above certain size and draw a box around them
        cnt = cv2.findContours(hsv.copy(), cv2.RETR_CCOMP,
                               cv2.CHAIN_APPROX_TC89_KCOS)[1]

        new_hands = []
        for c in cnt:
            if cv2.contourArea(c) > 800:

                (x, y, w, h) = cv2.boundingRect(c)
                x = x - 50  # offset hand positions to the middle of the screen
                new_hands.append(Hand(x, y, w, h))

                M = cv2.moments(c)
                cx = int(M['m10'] / M['m00'])
                cy = int(M['m01'] / M['m00'])
                centers.append([cx, cy])

                # shapes only used while debugging:
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        self.hands = sorted(new_hands, key=lambda elem: elem.x, reverse=False)  # place hands from left to right
        self.two_hands_in_frame = len(self.hands) == 2

        if len(centers) >= 2:

            dx = centers[0][0] - centers[1][0]
            dy = centers[0][1] - centers[1][1]
            d = np.sqrt(dx * dx + dy * dy)

            col = (0, 0, 255)
            if d < 220 and dy < 25:
                col = (0, 255, 0)
                self.is_holding_turtle = True
            else:
                self.is_holding_turtle = False

            cv2.line(frame, (centers[0][0], centers[0][1]), (centers[1][0], centers[1][1]), col, 5)
            cv2.circle(frame, (int((centers[0][0] + centers[1][0]) / 2),
                               int((centers[0][1] + centers[1][1]) / 2)), 10, col, -1)
            self.middle_point = (int((centers[0][0] + centers[1][0]) / 2),
                                 int((centers[0][1] + centers[1][1]) / 2))

        return frame  # return the processed frame. This is only done for debugging purposes.


class Hand:
    """
        THE CLASS THAT REPRESENTS HANDS IN THE VIDEO FRAME
    """

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y                    # the x- and y coordinates of the hand
        self.width, self.height = width, height  # width and height is not used out of testing
