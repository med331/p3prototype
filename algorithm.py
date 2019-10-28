import cv2
from math import sqrt


class Algorithm:  # abstract class
    def __init__(self, identifier='frame'):
        self.frame = None
        self.identifier = identifier
        # the implemented algorithm must maintain a list of all objects in the frame
        self.objects_in_frame = []

    def _update_state(self, objects_in_frame):
        self.objects_in_frame = objects_in_frame

    def _process(self, frame):  # the "_" in the name means this method should be treated as protected!
        ''' abstract method, the one you should implement '''
        raise NotImplementedError

    def process_frame(self, frame):
        self.frame, objects = self._process(frame)
        self._update_state(objects)
        return self.frame

    def display_current_frame(self):
        cv2.imshow(self.identifier, self.frame)


class FrameObject:
    ''' WARNING. NOT YET TESTED '''

    def __init__(self, x, y, w, h, **kwargs):
        self.coordinates = (x, y)
        self.dimesions = (w, h)
        self.is_hand = kwargs.is_hand or False

    def __le__(self, value):
        return True if self.w * self.h < value.w * value.h else False

    def __lt__(self, value):
        return True if self.w * self.h <= value.w * value.h else False

    def __eq__(self, value):
        same_coordinates = self.x == value.x and self.y == value.y
        same_dimensions = self.w == value.w and self.h == value.h
        same_hand = self.is_hand == value.is_hand
        return True if same_coordinates and same_dimensions and same_hand else False

    def __ne__(self, value):
        return not self == value # invokes __eq__

    def __ge__(self, value):
        return True if self.w * self.h >= value.w * value.h else False

    def get_distance_to(self, value):
        ''' NOT TESTED. PROBABLY DOESN'T WORK '''
        return sqrt((value.x - (self.x + self.w)) * 2 + (value.y - (self.y + self.h)) * 2)