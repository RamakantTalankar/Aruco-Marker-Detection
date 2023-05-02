import cv2 as cv
import os

CHESS_BOARD_DIM = (9, 7)

n = 0  # image_counter

# checking if  images dir exists 
image_dir_path = "images_cam"

CHECK_DIR = os.path.isdir(image_dir_path)
# if directory does not exist create
if not CHECK_DIR:
    os.makedirs(image_dir_path)
    print(str(image_dir_path)+' Directory is created')
else:
    print(str(image_dir_path)+' Directory already Exists.')

#termination criteria for k-means algorithm
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001) #epsilon parameter (min change req to stop algo) and no. of iterations


def detect_checker_board(image, grayImage, criteria, boardDimension):
    ret, corners = cv.findChessboardCorners(grayImage, boardDimension)
    if ret == True:
        corners1 = cv.cornerSubPix(grayImage, corners, (3, 3), (-1, -1), criteria)  #refined corner positions
        image = cv.drawChessboardCorners(image, boardDimension, corners1, ret) #drawing circles on refined corners

    return image, ret


cap = cv.VideoCapture(0)

while True:
    _, frame = cap.read()
    copyFrame = frame.copy()
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    image, board_detected = detect_checker_board(frame, gray, criteria, CHESS_BOARD_DIM)
    # displaying saved images count
    cv.putText(
        frame,
        'saved_img :'+ str(n),
        (30, 40),
        cv.FONT_HERSHEY_PLAIN,
        1.4,
        (0, 255, 0),
        2,
        cv.LINE_AA,
    )

    cv.imshow("frame", frame)
    cv.imshow("copyFrame", copyFrame)

    key = cv.waitKey(1)

    if key == ord("q"):
        break
    if key == ord("s") and board_detected == True:
        # storing the checker board image
        cv.imwrite(str(image_dir_path)+'/image'+str(n)+'.png', copyFrame)

        print('saved image number' +str(n))
        n += 1  # incrementing the image counter
cap.release()
cv.destroyAllWindows()

print("Total saved Images:", n)
