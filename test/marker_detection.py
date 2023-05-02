#!/usr/bin/env python
import cv2 as cv
import numpy as np
from cv2 import aruco   

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
        for ids, corners in zip(marker_IDs, marker_corners):
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

            #display id on top_right corner
            cv.putText(
                frame,
                'id: '+str(ids[0]),
                tuple(top_right),
                cv.FONT_HERSHEY_PLAIN,
                1.3,
                (0, 255, 0),
                2,
                cv.LINE_AA,
            )
        #     cv.putText(frame, str(marker_IDs),
        # (corners[0], corners[1] - 15),
        # cv.FONT_HERSHEY_SIMPLEX,
        # 0.5, (0, 255, 0), 2,cv.LINE_AA)
    cv.imshow("frame", frame)
    #quit window
    key = cv.waitKey(1)
    if key == ord("q"):
        break
cap.release()
cv.destroyAllWindows()


