#!/usr/bin/env python
import roslib
import sys
import rospy
import cv2
import numpy as np
from sensor_msgs.msg import Image
from sensor_msgs.msg import CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from threading import Thread, Lock


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
      
    