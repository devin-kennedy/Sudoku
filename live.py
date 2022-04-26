import cv2 as cv
import numpy as np
import import_board

cap = cv.VideoCapture(0)

state = False

while True:
    _, frame = cap.read()

    cv.imshow("Frame", frame)

    if cv.waitKey(1) & 0xFF == ord("s"):
        cv.imwrite("fullscreen.png", frame)
        state = True
        break
    elif cv.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv.destroyAllWindows()

if state:
    import_board.impt_board(saved=False)
