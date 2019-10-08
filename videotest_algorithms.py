import cv2
import datetime
from algorithm import Algorithm


class StefAlgorithm1(Algorithm):
    ''' Steffan's initial canny edge-detection algorithm '''

    def __init__(self, identifier='frame'):
        '''just calling parent constructor'''
        super().__init__(identifier=identifier)

    def _process(self, frame):
        # (simple) operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.Canny(gray, 60, 75)
        return cv2.bilateralFilter(gray, 9, 75, 75)


class YTAlgorithm1(Algorithm):
    ''' a motion-detection algorithm I found on the interwebs, which I then altered a bit: https://www.youtube.com/watch?v=5jKj6dRKaZc '''

    def __init__(self, identifier='frame'):
        super().__init__(identifier=identifier)
        self.first_frame = None
        self.identifier = 'Unoccupied'

    def _process(self, frame):
        # make each frame greyscale wich is needed for threshold
        greyscale_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        gaussian_frame = cv2.GaussianBlur(greyscale_frame, (21, 21), 0)
        # uses a kernal of size(21,21) // has to be odd number to to ensure there is a valid integer in the centre
        # and we need to specify the standerd devation in x and y direction wich is the (0) if only x(sigma x) is specified
        # then y(sigma y) is taken as same as x. sigma = standerd deveation(mathmetics term)

        # uses a kernal of size(5,5)(width,height) wich goes over 5x5 pixel area left to right
        blur_frame = cv2.blur(gaussian_frame, (5, 5))
        # does a calculation and the pixel located in the centre of the kernal will become
        # a new value(the sum of the kernal after the calculations) and then it moves to the right one and has a new centre pixel
        # and does it all over again..untill the image is done, obv this can cause the edges to not be changed, but is very minute

        greyscale_image = blur_frame
        # greyscale image with blur etc wich is the final image ready to be used for threshold and motion detecion

        if self.first_frame is None:
            self.first_frame = greyscale_image
            # first frame is set for background subtraction(BS) using absdiff and then using threshold to get the foreground mask
            # foreground mask (black background anything that wasnt in image in first frame but is in newframe over the threshold will
            # be a white pixel(white) foreground image is black with new object being white...there is your motion detection
        else:
            pass

        frame_delta = cv2.absdiff(self.first_frame, greyscale_image)
        # calculates the absolute diffrence between each element/pixel between the two images, first_frame - greyscale (on each element)

        # edit the ** thresh ** depending on the light/dark in room, change the 100(anything pixel value over 100 will become 255(white))
        thresh = cv2.threshold(frame_delta, 100, 255, cv2.THRESH_BINARY)[1]
        # threshold gives two outputs retval,threshold image. using [1] on the end i am selecting the threshold image that is produced

        thresh = cv2.dilate(thresh, None, iterations=2)
        # dilate = dilate,grow,expand - the effect on a binary image(black background and white foregorund) is to enlarge/expand the white
        # pixels in the foreground wich are white(255), element=Mat() = default 3x3 kernal matrix and iterartions=2 means it
        # will do it twice

        # find all contours (represented as outlines in the final frame), using CHAIN_APPROX_SIMPLE to save on memory usage
        contours, hierarchy = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # update the frame text to display the number of entities outlines by contours in the frame
        entities_in_frame = len(contours)
        if entities_in_frame > 0:
            self.identifier = str(entities_in_frame) + ' entities in frame'

        # return the final rendered contours
        return cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)

    def display_current_frame(self):
        ''' draws text and timestamp on video feed '''

        # frame is the image on wich the text will go. 0.5 is size of font, (0,0,255) is R,G,B color of font, 2 on end is LINE THICKNESS! OK :)
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(self.frame, '{+} Room Status: %s' % (self.identifier),
                    (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
        cv2.putText(self.frame, datetime.datetime.now().strftime('%A %d %B %Y %I:%M:%S%p'),
                    (10, self.frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)  # frame.shape[0] = hieght, frame.shape[1] = width,ssssssssssssss

        # show the processed frame
        cv2.imshow('Camera Feed', self.frame)
