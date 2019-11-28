from unittest import TestCase
from src.gesture_engine import GestureEngine
import cv2


class TestGestureEngine(TestCase):

    def test_process_frame(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 800)
        cap.set(4, 600)
        while True:
            frame = cap.read()[1]
            frame2 = GestureEngine().process_frame(frame)
            cv2.imshow('Frame', frame2)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.fail()
