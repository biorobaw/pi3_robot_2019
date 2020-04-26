#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import SetSpeeds
import numpy as np
from std_msgs.msg import String
import Lab4Grid
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension

from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse

from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock
import threading
import math

FPS_SMOOTHING = 0.9
mutex = Lock()

from Tkinter import *
# Window names
WINDOW1 = "Adjustable Mask - Press Esc to quit"
WINDOW2 = "Detected Blobs - Press Esc to quit"
##########V, N, E, S, W, COST
maze1 = [[0, 1, 0, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1], #starting grid
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]

maxSpeed=6
# Default HSV ranges
# Note: the range for hue is 0-180, not 0-255
minH =   0; minS = 127; minV =   0;
maxH = 180; maxS = 255; maxV = 255;

#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

global sense
sense = (0.0, 0.0, 0.0) 

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)

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
        
        
def Task2(inputCell,inputDir):
    rate = rospy.Rate(10)
    root = Tk()
    global maze1
    gui = Lab4Grid.Application(master=root)
    gui.update_idletasks()
    gui.update()
    curcell = inputCell-1
    dir_Num = inputDir
    dir_Enum = ['N','E','S','W']
    marked = False
    markCell(curcell, dir_Num)
    while not rospy.is_shutdown():
        for i in range (16):
            if (maze1[i][0]==0):
                break
            if i ==16:
                marked = True
            
        if marked ==True:
            break
        
        gui.maze = maze1
        gui.curcell = curcell
        gui.dir = dir_Enum[dir_Num]
        gui.updateGrid()
        gui.update_idletasks() #UPDATING DISPLAY
        gui.update()
        

        dirL = dir_Num
        if(dirL==0):
            dirL=4
        dirR=((dir_Num+1)%4)+1
        
        if(dir_Num==0):
            cellLeft=curcell-1
            cellRight=curcell+1
        elif(dir_Num==1):
            cellLeft=curcell-4
            cellRight=curcell+1
        elif(dir_Num==2):
            cellLeft=curcell+1
            cellRight=curcell-1
        elif(dir_Num==3):
            cellLeft=curcell+4
            cellRight=curcell-4
            
        
        if(maze1[curcell][dir_Num+1]==0): ##if there is no cell in front of us
            print("moving")
            moveCell()
            curcell = nextCell(curcell, dir_Num)
            markCell(curcell, dir_Num)
        elif(maze1[curcell][dirL]==0 or maze1[curcell][dirR]==0):
            if(maze1[curcell][dirL]==0):
                print("left turn")
                Turn(-90)
                dir_Num = dir_Num-1
                if(dir_Num<0):
                    dir_Num=3
            else:
                Turn(90)
                dir_Num = ((dir_Num+1)%4)
        else:
            print("unknown")
            Turn(-90)
            dir_Num = dir_Num-1
            if(dir_Num<0):
                dir_Num=3
        
        
        print(curcell)
        print(dir_Num)
        print(dirL)
        print("endloop")
        #adjustCell()
        rospy.sleep(1)
        
    while not rospy.is_shutdown():
        pass
    return
def adjustCell():
    rate = rospy.Rate(10)
    l = sense[0]*39.3701
    f = sense[1]*39.3701
    r = sense[2]*39.3701
    if(l>8.5 and r>8.5):
        return
    elif(l<r):
        wall = 'l'
        min = l
    else:
        wall = 'r'
        min = r
    SetSpeeds.setspeeds(1,-1)
    while not rospy.is_shutdown():
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701
        if(wall=='l'):
            if(l<min):
                min=l
            if(min+.23<l):
                min2=l
                break
        else:
            if(r<min):
                min=r
            if(min+.23<r):
                min2=r
                break
        rate.sleep()
    min2= min2+.15
    SetSpeeds.setspeeds(-1,1)
    while not rospy.is_shutdown():
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701
        if(wall=='l'):
            if(l<min2):
                min2=l
            if(min2+.23<l):
                break
            #if(min2<min):
            #    break
        else:
            if(r<min2):
                min2=r
            if(min2+.23<r):
                break
            #if(min2<min):
            #    break
        rate.sleep()
            
    SetSpeeds.setspeeds(0,0)

    
def moveCell():
    rate = rospy.Rate(10)
    c = abs(11*32/circumference)
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    lDis=0
    rDis=0
    f = sense[1]*39.3701
    k=1
    while (rDis-rInit<c and lDis-lInit<c):
        encod =  get_encoder().result
        lDis = encod[0]
        rDis = encod[1]
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701
        fronterror = (f-4)*2
        if(fronterror>maxSpeed):
             fronterror = maxSpeed

        if(l>9 and r>9):#IF NO WALLS, JUST GO FORWARD
            SetSpeeds.setspeeds(fronterror,fronterror)
        elif(l<r):
            wallerror = (l-4.25)*k
            if(wallerror>2):
                wallerror=2
            elif(wallerror<-2):
                wallerror=-2
            if(wallerror>0):
                SetSpeeds.setspeeds(fronterror-wallerror,fronterror)
            else:
                SetSpeeds.setspeeds(fronterror,fronterror+(wallerror*.5))
        else:
            wallerror = (r-4.25)*k
            if(wallerror>2):
                wallerror=2
            elif(wallerror<-2):
                wallerror=-2
            if(wallerror>0):
                SetSpeeds.setspeeds(fronterror,fronterror-wallerror)
            else:
                SetSpeeds.setspeeds(fronterror+(wallerror*.5),fronterror)
        if(f<5.5):
            break
        rate.sleep()
    SetSpeeds.setspeeds(0,0)
    return

def markCell(curcell, dir_Num):
    global maze1
    if(maze1[curcell][0]==1):
        return
    maze1[curcell][0]=1
    l = sense[0]*39.3701
    f = sense[1]*39.3701
    r = sense[2]*39.3701
    dir_Enum = ['N','E','S','W']
    wallL= dir_Num
    if(wallL==0):
        wallL=4
    wallF=dir_Num+1
    wallR=((dir_Num+1)%4)+1
    
    if(l<8):
        maze1[curcell][wallL]=1
    if(f<9):
        maze1[curcell][wallF]=1
    if(r<8):
        maze1[curcell][wallR]=1
        
def nextCell(curcell, dir_Num):

    dir_Enum = ['N','E','S','W']
    if(dir_Num ==0):
        return curcell-4
    elif(dir_Num==1):
        return curcell+1
    elif(dir_Num==2):
        return curcell+4
    elif(dir_Num==3):
        return curcell-1
    else:
        print("something horrible has happened")
        return -1
    
    
def Turn(Degrees): 
    rate = rospy.Rate(10)
    if(Degrees >0):
        maxSpeedL=3
        maxSpeedR=-3
    else:
        maxSpeedL=-3
        maxSpeedR=3
    c = 2*math.pi*(width/2) * (abs(Degrees)*1.00/360)*(32/circumference) #circumference of circle times how many rotations
    encod =  get_encoder().result                              #times how many inches per tick
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    while (r-rInit<(c-3) or l-lInit<(c-3)):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        satSpeed = c - ((r-rInit)*(circumference/32))
        satSpeed = satSpeed*.25
        if satSpeed>abs(maxSpeedL):
            satSpeedL = maxSpeedL
            satSpeedR = maxSpeedR
        else:
            satSpeedL=satSpeed
            satSpeedR=satSpeed
            if(Degrees >0):
                satSpeedR= satSpeedR*-1
            else:
                satSpeedL= satSpeedL*-1
        SetSpeeds.setspeeds(satSpeedL,satSpeedR)
        rate.sleep()
    print("Done!")
    print((r-rInit)*(circumference/32))
    print(c)
        
    SetSpeeds.setspeeds(0,0)
    
    
    
def startGridGUI():
    pass

def Test():
    root = Tk()
    gui = Lab4Grid.Application(master=root2)
    gui.update_idletasks()
    gui.update()

    print("blah")
  
    print("blah")
    i = 0
    while not rospy.is_shutdown():
        gui.maze = maze1
        if(i%2):
            gui.maze = maze2
        gui.updateGrid()
        gui.update_idletasks()
        gui.update()
        rospy.sleep(1)
        i= i +1
    
    return
    
    


        

