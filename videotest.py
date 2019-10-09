import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)
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
    #Creating mask
    diff = cv2.absdiff(frame1, gray)
    mask = diff

    #cv2.imshow("subtract", mask)

    mask = cv2.threshold(mask, 50, 225, cv2.THRESH_BINARY_INV)[1]
    mask = cv2.medianBlur(mask, 9)
    mask = cv2.dilate(mask, None, iterations=5)

    #cv2.imshow("thresh", mask)

    #background subtraction
    gray = cv2.subtract(gray,mask)

    #cv2.imshow("test", gray)

    cnt = cv2.findContours(gray.copy(), cv2.RETR_CCOMP, cv2.CHAIN_APPROX_TC89_KCOS)[1]
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