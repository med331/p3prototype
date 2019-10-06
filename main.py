import cv2
from videotest_algorithms import *

cap = cv2.VideoCapture(0)
cap.set(3, 800)
cap.set(4, 600)


# TODO: CHANGE ALGORITHM HERE
ALGORITHM_IN_USE = StefAlgorithm1()


while(True):
    # capture frame-by-frame
    frame = cap.read()[1]

    # process the frame
    processed = ALGORITHM_IN_USE.process_frame(frame)

    # the processed frame can be further developed here...

    # display the resulting frame
    ALGORITHM_IN_USE.display_current_frame()

    # wait for keyboard interrupt
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# when everything's done, release the capture
cap.release()
cv2.destroyAllWindows()
