#!/usr/bin/env python
from __future__ import print_function

import roslib
import sys
import rospy
import cv2
import Lab3Tasks
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock
from Tkinter import *


class image_converter:
  mutex = Lock()
  cv_image = cv2.imdecode(np.zeros((320,240,3), np.uint8),cv2.IMREAD_COLOR)
  def __init__(self):
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/pi3_robot_2019/r1/cam/image/compressed",CompressedImage,self.callback)

  def callback(self,data):
    try:  
      np_arr = np.fromstring(data.data, np.uint8)
      self.cv_image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
      self.cv_image = cv2.flip(self.cv_image,-1)
      if(self.mutex.locked()):
          self.mutex.release()
      
    except CvBridgeError as e:
      print(e)


#==========================GUI STUFF================
class Application(Frame):
    function = ""
    def FForward(self):
        #root.destroy()
        self.function = "FG"
        self.quit()

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=200)
        self.QUIT.pack(ipady=200)

        self.forward = Button(self)
        self.forward["text"] = "FaceForward",
        self.forward["command"] = self.FForward

        self.forward.pack({"side": "left"})
        self.forward.pack(ipadx=200)
        self.forward.pack(ipady=200)

        self.forward.pack({"side": "left"})
           

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
def main(args):
  ic = image_converter()
  rospy.init_node('image_converter', anonymous=True)
  rate = rospy.Rate(10) # 10hz
  try:
    root = Tk()
    app = Application(master=root)
    app.mainloop()
    root.destroy()
    if(app.function ==""):
        print("pass")
        pass

    elif(app.function =="FG"):
        Lab3Tasks.faceForward(ic)
        
  except KeyboardInterrupt:
    print("Shutting down")
  cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)