#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import SetSpeeds
import Lab3Display
import ImageConverter
import numpy as np
from std_msgs.msg import String
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock
from Tkinter import *

import threading

quitFlag=0;
global sense
sense = (0.0, 0.0, 0.0) 

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)

FPS_SMOOTHING = 0.9
mutex = Lock()
# Window names
WINDOW1 = "Adjustable Mask - Press Esc to quit"
WINDOW2 = "Detected Blobs - Press Esc to quit"

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


def Task1():
    ic = ImageConverter.image_converter()
    ic.mutex.acquire()
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
    #print("Create a mask!")
    while not rospy.is_shutdown():
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
        
        
    while not rospy.is_shutdown():
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
            print("hi")
            SetSpeeds.setspeeds(3, -3)
    
        # Check for user input
        c = cv2.waitKey(1)
        if (c == 27 or c == ord('q') or c == ord('Q')): # Esc or Q
            break
    
    SetSpeeds.setspeeds(0, 0)
    
def Task2():
    pass

frame = None
mask = None; frame_with_keypoints = None;
newFrame = False
quitFlag=0; finished = False
def Task3Main():
    global mask; global frame_with_keypoints;
    global newFrame;
    global mutex; global quitFlag;
    rate = rospy.Rate(10)
    root = Tk()
    entry = Lab3Display.Entry_GUI(master=root)
    entry.mainloop()
    entry.destroy()
    minH=[0,0,0]; minS=[0,0,0]; minV=[0,0,0]; maxH=[0,0,0]; maxS=[0,0,0]; maxV=[0,0,0]
    for i in range (3):
        minH[i] = entry.minH[i].get(); minS[i] = entry.minS[i].get(); minV[i] = entry.minV[i].get();
        maxH[i] = entry.maxH[i].get(); maxS[i] = entry.maxS[i].get(); maxV[i] = entry.maxV[i].get();
    
    display = Lab3Display.Application(master=root)
    
    #Call these two lines to update gui
    display.update_idletasks()
    display.update()
 
    
    t3Thread = threading.Thread(target=Task3, args=(display,minH, minS, minV, maxH, maxS, maxV,))

    t3Thread.start()
    while not rospy.is_shutdown(): #GUI must be ran on main thread. Task2 ran on seperate thread.
        try:
            display.updateDisplay()
            display.update_idletasks()
            display.update()
            if(finished==True):
                cv2.destroyAllWindows()
                break
            elif(newFrame==True):
                cv2.imshow(WINDOW1, mask)
                cv2.imshow(WINDOW2, frame_with_keypoints)
                c = cv2.waitKey(1)
                newFrame=False
            rate.sleep()
        except Exception as e:
            #print(e)
            break
        
    quitFlag=1
    display.mainloop()
    root.destroy()
    t3Thread.join()    
    return
    

def Task3(display, minH, minS, minV, maxH, maxS, maxV):
    global sense; global finished
    ic = ImageConverter.image_converter()
    ic.mutex.acquire()
    global frame; global mutex;
    global mask; global frame_with_keypoints;
    global newFrame;
    
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
 
    fps, prev = 0.0, 0.0
        
    while quitFlag==0:
        
        # Calculate FPS
        ic.mutex.acquire()
        now = rospy.get_time()
        fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        frame = ic.cv_image
    
        # Blob detection works better in the HSV color space 
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the given HSV range
        mask = cv2.inRange(frame_hsv, (minH[0], minS[0], minV[0]), (maxH[0], maxS[0], maxV[0]))
        

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)
        
        
        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Write text onto the frame
        cv2.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
        cv2.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    
        
        newFrame=True
        
        
        if(len(keypoints) >0):
            largest = keypoints[0]
            for i in keypoints:
                if i.size>largest.size:
                    largest = i
            print(largest.pt[0])     
            if(largest.pt[0]<200 and largest.pt[0]>100):
                SetSpeeds.setspeeds(0, 0)
                r1 = sense[1]*39.3701
                break
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
            SetSpeeds.setspeeds(-3, 3)
    
        #c = cv2.waitKey(1)
    display.R1 = r1
    
    SetSpeeds.setspeeds(0, 0)
    
    
    while quitFlag==0:
        # Calculate FPS
        ic.mutex.acquire()
        now = rospy.get_time()
        fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
        prev = now
        # Get a frame
        frame = ic.cv_image
    
        # Blob detection works better in the HSV color space 
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the given HSV range
        mask = cv2.inRange(frame_hsv, (minH[1], minS[1], minV[1]), (maxH[1], maxS[1], maxV[1]))

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)
        
        
        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Write text onto the frame
        cv2.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
        cv2.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    

        newFrame=True

        
        if(len(keypoints) >0):
            largest = keypoints[0]
            for i in keypoints:
                if i.size>largest.size:
                    largest = i
            #print(largest.pt[0])     
            if(largest.pt[0]<200 and largest.pt[0]>100):
                SetSpeeds.setspeeds(0, 0)
                r2 = sense[1]*39.3701
                break
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
            SetSpeeds.setspeeds(-3, 3)
        #c = cv2.waitKey(1)
    display.R2 = r2
    
    SetSpeeds.setspeeds(0, 0)
    
    while quitFlag==0:
        # Calculate FPS
        ic.mutex.acquire()
        now = rospy.get_time()
        fps = (fps*FPS_SMOOTHING + (1/(now - prev))*(1.0 - FPS_SMOOTHING))
        prev = now

        # Get a frame
        frame = ic.cv_image
    
        # Blob detection works better in the HSV color space 
        # (than the RGB color space) so the frame is converted to HSV.
        frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        
        # Create a mask using the given HSV range
        mask = cv2.inRange(frame_hsv, (minH[2], minS[2], minV[2]), (maxH[2], maxS[2], maxV[2]))
        

        # Run the SimpleBlobDetector on the mask.
        # The results are stored in a vector of 'KeyPoint' objects,
        # which describe the location and size of the blobs.
        keypoints = detector.detect(mask)
        
        
        # For each detected blob, draw a circle on the frame
        frame_with_keypoints = cv2.drawKeypoints(frame, keypoints, None, color = (0, 255, 0), flags = cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
        
        # Write text onto the frame
        cv2.putText(frame_with_keypoints, "FPS: {:.1f}".format(fps), (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
        cv2.putText(frame_with_keypoints, "{} blobs".format(len(keypoints)), (5, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0))
    
        newFrame=True
        
        
        if(len(keypoints) >0):
            largest = keypoints[0]
            for i in keypoints:
                if i.size>largest.size:
                    largest = i
            if(largest.pt[0]<200 and largest.pt[0]>100):
                SetSpeeds.setspeeds(0, 0)
                r3 = sense[1]*39.3701
                break
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
            SetSpeeds.setspeeds(-3, 3)
    display.R3 = r3

    SetSpeeds.setspeeds(0, 0)
    finished = True
    

def Task4(ic):
    pass


        


        

