import cv2
import datetime
import numpy as np
from algorithm import *


class StefAlgorithm1(Algorithm):
    ''' Steffan's initial canny edge-detection algorithm '''

    def __init__(self, identifier='frame'):
        '''just calling parent constructor'''
        super().__init__(identifier=identifier)

    def _process(self, frame):
        # (simple) operations on the frame
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.Canny(gray, 60, 75)
        return (cv2.bilateralFilter(gray, 9, 75, 75), [])


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
        contours = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[1]

        # update the frame text to display the number of entities outlines by contours in the frame
        entities_in_frame = len(contours)
        if entities_in_frame > 0:
            self.identifier = str(entities_in_frame) + ' entities in frame'

        # return the final rendered contours
        return (cv2.drawContours(frame, contours, -1, (0, 255, 0), 3), [])

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


class StefVideotest1(Algorithm):
    def __init__(self, identifier='frame'):
        super().__init__(identifier=identifier)
        self.frame1 = None

    def _process(self, frame):
        frame = cv2.flip(frame, flipCode=1)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        gray = cv2.blur(gray, (5, 5))

        #cv2.imshow("grayscale", gray)

        # retrieve 1st frame
        if self.frame1 is None:
            self.frame1 = gray

        else:
            pass
        # Creating mask
        diff = cv2.absdiff(self.frame1, gray)
        mask = diff

        #cv2.imshow("subtract", mask)

        mask = cv2.threshold(mask, 50, 225, cv2.THRESH_BINARY_INV)[1]
        mask = cv2.medianBlur(mask, 9)
        mask = cv2.dilate(mask, None, iterations=5)

        #cv2.imshow("thresh", mask)

        # background subtraction
        gray = cv2.subtract(gray, mask)

        #cv2.imshow("test", gray)

        cnt = cv2.findContours(gray.copy(), cv2.RETR_CCOMP,
                               cv2.CHAIN_APPROX_TC89_KCOS)[1]
        for c in cnt:
            if cv2.contourArea(c) > 800:
                (x, y, w, h) = cv2.boundingRect(c)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)
            else:
                pass

        # Optional drawContours instead of rectangle
        #frame = cv2.drawContours(frame,cnt,-1,(0,0,255),2,cv2.FILLED)

        return (frame, [])


class StefVideotest2(Algorithm):
    def __init__(self, identifier='frame'):
        super().__init__(identifier=identifier)
        self.lower_blue = np.array([100, 50, 50])
        self.upper_blue = np.array([140, 255, 255])
        self.frame1 = None

    def _process(self, frame):
        frame = cv2.flip(frame, flipCode=1)
        # Our operations on the frame come here
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)
        gray = cv2.blur(gray, (5, 5))
        #cv2.imshow("grayscale", gray)

        # retrieve 1st frame
        if self.frame1 is None:
            self.frame1 = gray

        else:
            pass
        # creating the mask
        diff = cv2.absdiff(self.frame1, gray)
        gray = diff
        gray = cv2.medianBlur(gray, 9)
        gray = cv2.threshold(gray, 25, 225, cv2.THRESH_BINARY_INV)[1]
        gray = cv2.dilate(gray, None, iterations=2)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        #cv2.imshow("diff", gray)

        # background subtraction
        hsv = frame
        hsv = cv2.subtract(hsv, gray)
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2HSV)

        #cv2.imshow("sub", hsv)

        # Colour threshholding
        hsv = cv2.inRange(hsv, self.lower_blue, self.upper_blue)

        hsv = cv2.medianBlur(hsv, 9)

        #cv2.imshow("thresh", hsv)

        # find blue object above certain size and draw a box around them
        cnt = cv2.findContours(hsv.copy(), cv2.RETR_CCOMP,
                               cv2.CHAIN_APPROX_TC89_KCOS)[1]
        for c in cnt:
            if cv2.contourArea(c) > 800:
                (x, y, w, h) = cv2.boundingRect(c)

                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 255), 2)

            else:
                pass
        # Optional drawContours instead of rectangle
        #frame = cv2.drawContours(frame,cnt,-1,(0,0,255),2,cv2.FILLED)

        return (frame, []) # object processing not yet implemented
