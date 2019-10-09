import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)
lower_blue = np.array([100,50,50])
upper_blue = np.array([140,255,255])
frame1 = None

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.flip(frame,flipCode=1)
    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
    gray = cv2.blur(gray, (5, 5))
    #cv2.imshow("grayscale", gray)

    #retrieve 1st frame
    if frame1 is None:
        frame1 = gray

    else:
        pass
    #creating the mask
    diff = cv2.absdiff(frame1, gray)
    gray = diff
    gray = cv2.medianBlur(gray, 9)
    gray = cv2.threshold(gray, 25, 225, cv2.THRESH_BINARY_INV)[1]
    gray = cv2.dilate(gray, None, iterations=2)
    gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

    #cv2.imshow("diff", gray)

    #background subtraction
    hsv = frame
    hsv = cv2.subtract(hsv,gray)
    hsv = cv2.cvtColor(hsv,cv2.COLOR_BGR2HSV)

    #cv2.imshow("sub", hsv)

    #Colour threshholding
    hsv = cv2.inRange(hsv, lower_blue, upper_blue)

    hsv = cv2.medianBlur(hsv, 9)

    #cv2.imshow("thresh", hsv)

    #find blue object above certain size and draw a box around them
    cnt = cv2.findContours(hsv.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)[1]
    for c in cnt:
        if cv2.contourArea(c) > 800:
            (x, y, w, h) = cv2.boundingRect(c)

            cv2.rectangle(frame, (x, y), (x+w, y+h),(0,0,255), 2)

        else:
            pass
    #Optional drawContours instead of rectangle
    #frame = cv2.drawContours(frame,cnt,-1,(0,0,255),2,cv2.FILLED)

    # Display the resulting frame
    cv2.imshow('final',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()