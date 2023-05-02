import cv2 as cv
import os
import numpy as np

# Checker board size
CHESS_BOARD_DIM = (9, 7)

# The size of Square in the checker board.
SQUARE_SIZE = 20  # millimeters

#termination criteria for k-means algorithm
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)#epsilon parameter (min change req to stop algo) and no. of iterations


calib_data_path = "calib_data"
CHECK_DIR = os.path.isdir(calib_data_path)

#creating directory if not exists
if not CHECK_DIR:
    os.makedirs(calib_data_path)
    print(str(calib_data_path)+' Directory is created')

else:
    print(str(calib_data_path)+' Directory already Exists.')

# preparing object points, obj_3D is 2D array with 3 cols
obj_3D = np.zeros((CHESS_BOARD_DIM[0] * CHESS_BOARD_DIM[1], 3), np.float32)

#modifying the first 2 columns of obj_3D with x,y values
obj_3D[:, :2] = np.mgrid[0 : CHESS_BOARD_DIM[0], 0 : CHESS_BOARD_DIM[1]].T.reshape(
    -1, 2
)
obj_3D *= SQUARE_SIZE
print(obj_3D)

# Arrays to store object points and image points from all the images.
obj_points_3D = []  # 3d point in real world space
img_points_2D = []  # 2d points in image plane.

# The images directory path
image_dir_path = "images_cam"

files = os.listdir(image_dir_path)
for file in files:
    print(file)
    imagePath = os.path.join(image_dir_path, file)
    

    image = cv.imread(imagePath)
    grayScale = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    ret, corners = cv.findChessboardCorners(image, CHESS_BOARD_DIM, None)
    if ret == True:
        obj_points_3D.append(obj_3D)
        corners2 = cv.cornerSubPix(grayScale, corners, (3, 3), (-1, -1), criteria)#refined corner positions
        img_points_2D.append(corners2) 

        img = cv.drawChessboardCorners(image, CHESS_BOARD_DIM, corners2, ret) #drawing refined corners on board

cv.destroyAllWindows()
# h, w = image.shape[:2]
ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(
    obj_points_3D, img_points_2D, grayScale.shape[::-1], None, None
)
print("calibrated")

print("dumping data into one file using numpy ")
#stores arrays into a compressed file  (camera matrix: focal length, principal point and other intrinsic parameters, distortion coefficients, rotational vec, translational vecs)
np.savez(
    str(calib_data_path)+'/MultiMatrix',
    camMatrix=mtx,
    distCoef=dist,
    rVector=rvecs,
    tVector=tvecs,
)

print("-------------------------------------------")

print("loading stored data\n \n \n")

data = np.load(str(calib_data_path)+'/MultiMatrix.npz')

camMatrix = data["camMatrix"]
distCof = data["distCoef"]
rVector = data["rVector"]
tVector = data["tVector"]

print("loaded calibration data successfully")