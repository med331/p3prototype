import cv2


class Algorithm:  # abstract class
    def __init__(self, identifier='frame'):
        self.frame = None
        self.identifier = identifier

    def _process(self, frame):  # the "_" in the name means this method should be treated as protected!
        ''' abstract method, the one you should implement '''
        raise NotImplementedError

    def process_frame(self, frame):
        self.frame = self._process(frame)
        return self.frame

    def display_current_frame(self):
        cv2.imshow(self.identifier, self.frame)
