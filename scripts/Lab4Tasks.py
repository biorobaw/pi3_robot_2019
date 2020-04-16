#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import SetSpeeds
import numpy as np
from std_msgs.msg import Int8MultiArray
from std_msgs.msg import String
import Lab4Grid

from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock
import threading
FPS_SMOOTHING = 0.9
mutex = Lock()

from Tkinter import *
# Window names
WINDOW1 = "Adjustable Mask - Press Esc to quit"
WINDOW2 = "Detected Blobs - Press Esc to quit"
maze = [[0, 1, 1, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1], #starting grid
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]

maze2 = [[0, 1, 1, 1, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1], #starting grid
            [0, 1, 1, 1, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]

# Default HSV ranges
# Note: the range for hue is 0-180, not 0-255
minH =   0; minS = 127; minV =   0;
maxH = 180; maxS = 255; maxV = 255;

# These functions are called when the user moves a trackbar
def onMinHTrackbar(val):
    # Calculate a valid minimum red value and re-set the trackbar.
    global minH
    global maxH
    minH = min(val, maxH - 1)
    cv2.setTrackbarPos("Min Hue", WINDOW1, minH)

def onMinSTrackbar(val):
    global minS
    global maxS
    minS = min(val, maxS - 1)
    cv2.setTrackbarPos("Min Sat", WINDOW1, minS)

def onMinVTrackbar(val):
    global minV
    global maxV
    minV = min(val, maxV - 1)
    cv2.setTrackbarPos("Min Val", WINDOW1, minV)

def onMaxHTrackbar(val):
    global minH
    global maxH
    maxH = max(val, minH + 1)
    cv2.setTrackbarPos("Max Hue", WINDOW1, maxH)

def onMaxSTrackbar(val):
    global minS
    global maxS
    maxS = max(val, minS + 1)
    cv2.setTrackbarPos("Max Sat", WINDOW1, maxS)

def onMaxVTrackbar(val):
    global minV
    global maxV
    maxV = max(val, minV + 1)
    cv2.setTrackbarPos("Max Val", WINDOW1, maxV)


def faceForward(ic):
    #image_converter.cvimage
    # Initialize the SimpleBlobDetector
    params = cv2.SimpleBlobDetector_Params()
    detector = cv2.SimpleBlobDetector_create(params)

    # Attempt to open a SimpleBlobDetector parameters file if it exists,
    # Otherwise, one will be generated.
    # These values WILL need to be adjusted for accurate and fast blob detection.
    #You Will need to change the path
    fs = cv2.FileStorage("src/robot_client/scripts/params.yaml", cv2.FILE_STORAGE_READ); #yaml, xml, or json
    if fs.isOpened():
        detector.read(fs.root())
    else:
        print("WARNING: params file not found! Creating default file.")
    
        fs2 = cv2.FileStorage("paramstemp.yaml", cv2.FILE_STORAGE_WRITE)
        detector.write(fs2)
        fs2.release()
    
    fs.release()

    # Create windows
    cv2.namedWindow(WINDOW1)
    cv2.namedWindow(WINDOW2)

    # Create trackbars
    cv2.createTrackbar("Min Hue", WINDOW1, minH, 180, onMinHTrackbar)
    cv2.createTrackbar("Max Hue", WINDOW1, maxH, 180, onMaxHTrackbar)
    cv2.createTrackbar("Min Sat", WINDOW1, minS, 255, onMinSTrackbar)
    cv2.createTrackbar("Max Sat", WINDOW1, maxS, 255, onMaxSTrackbar)
    cv2.createTrackbar("Min Val", WINDOW1, minV, 255, onMinVTrackbar)
    cv2.createTrackbar("Max Val", WINDOW1, maxV, 255, onMaxVTrackbar)

    fps, prev = 0.0, 0.0
    print("Create a mask!")
    while True:
        # Calculate FPS
        ic.mutex.acquire()
        now = rospy.get_time()
        fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        #frame = camera.read()
        frame = ic.cv_image
    
        # Blob detection works better in the HSV color space 
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the given HSV range
        mask = cv2.inRange(frame_hsv, (minH, minS, minV), (maxH, maxS, maxV))
        

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)
        
        
        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
        # Write text onto the frame
        cv2.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
        cv2.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    
        # Display the frame
        cv2.imshow(WINDOW1, mask)
        cv2.imshow(WINDOW2, frame_with_keypoints)
    
        # Check for user input
        c = cv2.waitKey(1)
        if (c == 27 or c == ord('q') or c == ord('Q')): # Esc or Q
            break
        
        
    while True:
        # Calculate FPS
        ic.mutex.acquire()
        now = rospy.get_time()
        fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        #frame = camera.read()
        frame = ic.cv_image
    
        # Blob detection works better in the HSV color space 
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the given HSV range
        mask = cv2.inRange(frame_hsv, (minH, minS, minV), (maxH, maxS, maxV))
        

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)
        
        
        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Write text onto the frame
        cv2.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
        cv2.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    
        # Display the frame
        cv2.imshow(WINDOW1, mask)
        cv2.imshow(WINDOW2, frame_with_keypoints)
        
        
        if(len(keypoints) >0):
            largest = keypoints[0]
            for i in keypoints:
                if i.size>largest.size:
                    largest = i
            print(largest.pt[0])     
            if(largest.pt[0]<200 and largest.pt[0]>100):
                SetSpeeds.setspeeds(0, 0)
            elif(largest.pt[0] <100):
                e = 160 - largest.pt[0]
                e = e/160
                e = 3*e
                SetSpeeds.setspeeds(-e, e)
            elif(largest.pt[0] >200):
                e = largest.pt[0] -160
                e = e/160
                e = 3*e
                SetSpeeds.setspeeds(e, -e)
            
            
        else:
            SetSpeeds.setspeeds(3, -3)
    
        # Check for user input
        c = cv2.waitKey(1)
        if (c == 27 or c == ord('q') or c == ord('Q')): # Esc or Q
            break
    
    SetSpeeds.setspeeds(0, 0)
        
        
def Task2(rospy):
    #rospy.init_node('Task2', anonymous=True)
    #rate = rospy.Rate(10)
    #pub = rospy.Publisher('/Grid', Int8MultiArray, queue_size=0, latch = True)
    #msg = Int8MultiArray()
    
    #msg.layout.dim = [MultiArrayDimension(), MultiArrayDimension()]
    
    #msg.layout.data_offset = 0
    #dim = MultiArrayDimension()
    
    #msg.layout.dim[0].label = 'rows'
    #msg.layout.dim[0].size = 16
    #msg.layout.dim[0].stride = 96
    #msg.layout.dim[1].label = 'columns'
    #msg.layout.dim[1].size = 6
    #msg.layout.dim[1].stride = 6    
    #msg.data = np.reshape(maze,[96])
   
    print("sending")
    #for i in range(100):
    #    pub.publish(msg)
    #while not rospy.is_shutdown():
    #    pub.publish(msg)
    #    rate.sleep()
        
    #pub.publish(msg)
    #rate.sleep()
    #pub.publish(msg)
    #print("sent")
        
    #return msg
    
    #t = threading.Thread(target=startGridGUI)
    #t.daemon = True
    #t.start()
    root2 = Tk()
    app2 = Lab4Grid.Application(master=root2)
    #app2.mainloop()
    app2.update_idletasks()
    app2.update()

    print("blah")
    #while not rospy.is_shutdown():
    #    pass
    #t.join()
    print("blah")
    
    while not rospy.is_shutdown():
        app2.maze = maze2
        app2.updateGrid()
        app2.update_idletasks()
        app2.update()
        rospy.sleep(1)
    
    return

def startGridGUI():
    pass
    
    
    


        

