#!/usr/bin/env python

import rospy

import SetSpeeds
import Lab4Grid
#import ImageConverter #if camera is used
#import cv2
##for sensors
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
##

##for encoders
from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse
##

## if camera is used
from threading import Thread, Lock
##
import threading
import math

from Tkinter import *

##########Visted, N, E, S, W, Cost
startmaze = [[0, 1, 0, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1], #starting grid
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]

#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

cellMoved=0; quitFlag=0;#cell moved is a global flag that tells the gui to update the grid

sense = (0.0, 0.0, 0.0) 

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)

def Task2Main(inputCell,inputDir):
    rate = rospy.Rate(10)
    root = Tk()
    global startmaze; global cellMoved; global quitFlag
    gui = Lab4Grid.Application(master=root)
    t2Thread = threading.Thread(target=Task2, args=(gui,inputCell,inputDir,))
    t2Thread.start()
    while not rospy.is_shutdown(): #GUI must be ran on main thread. Task2 ran on seperate thread.
        try:
            if(cellMoved==1): #If the orientation of the robot has changed, update
                gui.updateGrid() #this line changes the grid
                cellMoved=0     #Set flag to 0
            gui.update_idletasks()#these lines
            gui.update() #update the gui
            rate.sleep()
        except Exception as e:
            #print(e)
            break
            
    quitFlag=1
    t2Thread.join()

def Task2(gui,inputCell,inputDir):
    global cellMoved; global quitFlag
    rate = rospy.Rate(10)
    curcell = inputCell-1 #list index is 0-15, not 1-16
    dir_Num = inputDir #The input Direction is a value 0-3 which will 
    dir_Enum = ['N','E','S','W'] #match up with this Enumerator.
    while quitFlag == 0:
        gui.maze = startmaze
        gui.curcell = curcell
        gui.dir = dir_Enum[dir_Num]
        cellMoved=1
        rate.sleep()
        return
    
def Task2SingleThread(inputCell,inputDir):
    rate = rospy.Rate(10)
    root = Tk()
    global startmaze
    gui = Lab4Grid.Application(master=root)
    gui.update_idletasks()
    gui.update()
    curcell = inputCell-1
    dir_Num = inputDir
    dir_Enum = ['N','E','S','W']
    while not rospy.is_shutdown():
        gui.maze = startmaze
        gui.curcell = curcell
        gui.dir = dir_Enum[dir_Num]
        gui.updateGrid() #mark this flag
        gui.update_idletasks()
        gui.update()
        rate.sleep()
        break
        
    gui.mainloop()
    return


        

