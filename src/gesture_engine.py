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

    def convert(self, r, g, b):
        r, g, b = r / 255.0, g / 255.0, b / 255.0

        mx = max(r, g, b) # Assign the max and min
        mn = min(r, g, b)
        df = mx - mn
        # Determining the h value
        if mx == mn:
            h = 0
        elif mx == r:
            h = (60 * ((g - b) / df) + 360) % 360
        elif mx == g:
            h = (60 * ((b - r) / df) + 120) % 360
        elif mx == b:
            h = (60 * ((r - g) / df) + 240) % 360
        # Determining the value
        if mx == 0:
            s = 0
        else:
            s = df / mx
        v = mx # Assigning the v value
        # Modifying HSV to be compatible with Open CV
        v = v * 255
        s = s * 255
        h = h / 2
        hsv = (h, s, v)
        return hsv

    def colorthresh(self,img,loh,los,lov,uph,ups,upv):
        x = 0
        y = 0
        height, width = img.shape[:2] # Retrieving the image size
        # Running through the image
        for h in range(height - 1):
            for w in range(width - 1):
                # Convert to Binary
                # Set pixel value to 255 if the right HSV value is detected
                if loh <= img.item(x, y, 0) <= uph and los <= img.item(x, y, 1) <= ups and lov <= img.item(x, y, 2) <= upv:
                    img[x,y] = 255
                else:
                    img[x, y] = 0
                if y >= width - 1:
                    y = 0
                y += 1
            x += 1
            if x >= height - 1:
                x = 0
        return img

    def medfilter(self, picture, size):
        (imH, imW) = picture.shape[:2]
        kerH = size
        kerW = size
        kerR = kerH // 2
        out = np.zeros(picture.shape)
        window = [0] * (kerW * kerH) # Making an array to store pixel currently run through the kernel
        # Run through the image
        for x in range(kerR, imW-kerR):
            for y in range(kerR, imH-kerR):
                i = 0
                # Run through the kernel
                for m in range(kerW):
                    for n in range(kerH):
                        # Assign pixels from the kernel to window
                        window[i] = picture[y-kerH+n][x-kerW+m]
                        if i == len(window)-1:
                            i = 0
                        else:
                            i += 1
                # Sorting and finding the median
                window.sort()
                l = len(window)
                if l % 2 == 0:
                    median1 = window[l // 2]
                    median2 = window[l // 2 - 1]
                    median = (median1 + median2) / 2
                else:
                    median = window[l // 2]
                out[y][x] = median
        return out

    def dilation(self, picture, size):
        (imH, imW) = picture.shape[:2]
        kerH = size
        kerW = size
        kerR = kerH // 2
        out = np.zeros(picture.shape)
        window = [0] * (kerW * kerH)
        # Run through the image
        for x in range(kerR, imW-kerR):
            for y in range(kerR, imH-kerR):
                i = 0
                for m in range(kerW):
                    for n in range(kerH):
                        # Assign pixels from the kernel to window
                        window[i] = picture[y - kerH + n][x - kerW + m]
                        if i == len(window) - 1:
                            i = 0
                        else:
                            i += 1
                # Perform the hit action if a pixel with the value of 255 is detected in the window
                for h in window:
                    if h == 255:
                        out[y][x] = 255
                        break
                    out[y][x] = 0
        return out

    def process_frame(self, frame):
        centers = []  # list to hold object centers
        frame = cv2.flip(frame, flipCode=1)  # flip the frame
        # convert to HSV
        x = 0
        y = 0
        height, width = frame.shape[:2]
        hsv = frame.copy()
        for h in range(height - 1):
            for w in range(width - 1):
                b = hsv.item(x, y, 0)
                g = hsv.item(x, y, 1)
                r = hsv.item(x, y, 2)
                hsv[x,y] = self.convert(r, g, b)
                if y >= width - 1:
                    y = 0
                y += 1
            x += 1
            if x >= height - 1:
                x = 0
        # Color threshholding
        hsv = self.colorthresh(hsv, 38, 50, 50, 75, 255, 255)
        # Processing the image with filtering and dilation
        hsv = cv2.cvtColor(hsv, cv2.COLOR_BGR2GRAY)
        hsv = self.medfilter(hsv, 7)
        hsv = self.dilation(hsv, 5)
        hsv = self.dilation(hsv, 5)
        hsv = self.dilation(hsv, 5)
        hsv = cv2.normalize(hsv, dst=None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
        # find green object above certain size and draw a box around them
        cnt = cv2.findContours(hsv.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)[1]

        new_hands = []
        for c in cnt:
            if cv2.contourArea(c) > 800:

                (x, y, w, h) = cv2.boundingRect(c)
                x = x - 50  # offset hand positions to the middle of the screen
                new_hands.append(Hand(x, y, w, h))

                # calculate the center point of the rectangle
                cx = x - int(w / 2)
                cy = y - int(h / 2)
                centers.append([cx, cy])

                # shapes only used while debugging:
                cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

        self.hands = sorted(new_hands, key=lambda elem: elem.x, reverse=False)  # place hands from left to right
        self.two_hands_in_frame = len(self.hands) == 2

        if len(centers) == 2:

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
