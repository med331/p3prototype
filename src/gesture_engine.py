"""
    GestureEngine must analyze a webcam for user gestures
"""
import sys


class GestureEngine:

    def __init__(self):
        self.hands = []
        self.distance_between_hands = sys.maxsize
        self.middle_point = (sys.maxsize, sys.maxsize)

    def process_frame(self):
        # TODO: process frame
        print("Frame processing happened!")


class Hand:

    def __init__(self, x, y, width, height):
        self.x, self.y = x, y
        self.width, self.height = width, height
        # self.middleX, self.middleY = middle_x, middle_y
