import cv2
from algorithm import Algorithm


class StefAlgorithm1(Algorithm):
    def __init__(self, identifier='frame'):
        '''just calling parent constructor'''
        super().__init__(identifier=identifier)

    def _process(self, frame):
        # (simple) operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.Canny(gray, 60, 75)
        return cv2.bilateralFilter(gray, 9, 75, 75)
