#!/usr/bin/env python

import sys
import os
import rospy
from geometry_msgs.msg import Twist
sys.path.append(os.path.abspath("/home/pi/drivers"))
import MyServos

def setSpeedsVW(twist):
  rospy.loginfo("speed vw: %d   %d",twist.linear.x, twist.angular.z )
  MyServos.setSpeedsVW_MPS(twist.linear.x, twist.angular.z)
  
def startController():
  rospy.init_node('pi3_robot_2019_motion_controller')
  rospy.Subscriber("/b1/speed_cmd",Twist,setSpeedsVW)
  rospy.spin()
  
if __name__ == '__main__':
  try:
    MyServos.setSpeeds(0,0)
    startController()
    MyServos.setSpeeds(0,0)
  except:
    MyServos.setSpeeds(0,0)
  
