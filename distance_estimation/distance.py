#!/usr/bin/env python
import cv2 as cv
import numpy as np
from cv2 import aruco   

#providing path to collected data from camera caliberation
calib_data_path = "calib_data/MultiMatrix.npz"

calib_data = np.load(calib_data_path)
print(calib_data.files)

cam_mat = calib_data["camMatrix"]
dist_coef = calib_data["distCoef"]
r_vectors = calib_data["rVector"]
t_vectors = calib_data["tVector"]

MARKER_SIZE = 19 #in cm

# id,marker pairs having 4x4 aruco markers 
marker_dict = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_ARUCO_ORIGINAL)
#parameters for detection
param_markers =  cv.aruco.DetectorParameters_create()



#creating camera object and index==0 as only one camera connected
cap = cv.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break
    gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  #converting to gray scale
    marker_corners, marker_IDs, reject = aruco.detectMarkers(
        gray_frame, marker_dict, parameters=param_markers
    )
    if marker_corners:
        #getting rotational and translational vectors for all markers
        rVec,tVec,_= aruco.estimatePoseSingleMarkers(marker_corners,MARKER_SIZE,cam_mat,dist_coef)
        total_markers=range(0,marker_IDs.size)
        for ids, corners ,i in zip(marker_IDs, marker_corners,total_markers):
            #draw border
            cv.polylines(
                frame, [corners.astype(np.int32)], True, (0, 255, 255), 4, cv.LINE_AA
            )
            corners = corners.reshape(4, 2)  #reshape array to 4x2 (4 corners and coords)
            corners = corners.astype(int)
            top_right = corners[0].ravel()
            top_left = corners[1].ravel()
            bottom_right = corners[2].ravel()
            bottom_left = corners[3].ravel()
            
             # Calculating the distance of the 3D vector, tvec[i][0][0] represents component of vector along x-axis
            distance = np.sqrt(
                tVec[i][0][2] ** 2 + tVec[i][0][0] ** 2 + tVec[i][0][1] ** 2
            )
            #drawing axes on markers (x:red, y:green , z:blue)
            #point = cv.drawFrameAxes(frame, cam_mat, dist_coef, rVec[i], tVec[i],6 , 6)
            #display id, distance on top_right corner
            cv.putText(
                frame,
                'id: '+ str(ids[0])+  '  Dist:'+ str(round(distance, 2)),
                tuple(top_right),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 255, 0),
                2,
                cv.LINE_AA,
            )
            #displaying x,y coordinates on bottom right corner
            cv.putText(
                frame,
                'x: '+str(round(tVec[i][0][0],1))+' y: '+str(round(tVec[i][0][1],1)) ,
                tuple(bottom_right),
                cv.FONT_HERSHEY_PLAIN,
                1.0,
                (0, 0, 255),
                2,
                cv.LINE_AA,
            )
    cv.imshow("frame", frame)
    #quit window
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()


