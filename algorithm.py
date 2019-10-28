import cv2


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
