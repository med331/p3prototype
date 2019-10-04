import numpy as np
import cv2

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.threshold(gray,50,255, cv2.THRESH_BINARY)[1]
    gray = cv2.bilateralFilter(gray, 9, 75, 75)

    # Display the resulting frame
    cv2.imshow('frame',gray)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()