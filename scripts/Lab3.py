#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import Lab3Tasks
import SetSpeeds
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock
from Tkinter import *

def on_shutdown():
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0)
    rate.sleep()

#==========================GUI STUFF================
class Application(Frame):
    function = ""
    def Task1(self):
        self.function = "Task1"
        self.quit()
    def Task2(self):
        self.function = "Task2"
        self.quit()
    def Task3(self):
        self.function = "Task3"
        self.quit()
    def Task4(self):
        self.function = "Task4"
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT    \n"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=0, column=0,ipadx=150, ipady=150, sticky="ew")

        
        self.T1 = Button(self)
        self.T1["text"] = "Task1\n(Goal Facing)"
        self.T1.grid(row=0, column=1,ipadx=150, ipady=150, sticky="ew")
        self.T1["command"] =  self.Task1
        
        self.T2 = Button(self)
        self.T2["text"] = "Task2\n(Motion to Goal)"
        self.T2.grid(row=0, column=2,ipadx=150, ipady=150, sticky="ew")

        self.T2["command"] =  self.Task2
        
        self.T3 = Button(self)
        self.T3["text"] = "Task3\n(Triangulation)"
        self.T3.grid(row=1, column=0,ipadx=150, ipady=150, sticky="ew")

        self.T3["command"] =  self.Task3
         
         
        self.T4 = Button(self)
        self.T4["text"] = "Task4\n(Bug Algorithm)"
        self.T4.grid(row=1, column=1,ipadx=150, ipady=150, sticky="ew")

        self.T4["command"] =  self.Task4
           

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
def main(args):
    pass

if __name__ == '__main__':
    
    try:
        rospy.init_node('image_converter', anonymous=True)
        rospy.on_shutdown(on_shutdown)
        rate = rospy.Rate(10) # 10hz
        root = Tk()
        app = Application(master=root)
        app.mainloop()
        root.destroy()
        if(app.function ==""):
            print("pass")
            pass

        elif(app.function =="Task1"):
            Lab3Tasks.Task1()
            pass
        elif(app.function =="Task2"):
            Lab3Tasks.Task2()
            pass
        elif(app.function =="Task3"):
            Lab3Tasks.Task3Main()
            pass
        elif(app.function =="Task4"):
            Lab3Tasks.Task4()
            pass
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        #print(e)
        on_shutdown()
        #pass

    