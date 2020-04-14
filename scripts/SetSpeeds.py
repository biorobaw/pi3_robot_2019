#!/usr/bin/env python
# license removed for brevity
import rospy
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String




#============================Creates publisher to send speeds=================
#rospy.init_node('lab2', anonymous=True)
pub = rospy.Publisher('pi3_robot_2019/r1/speed_vw', Twist, queue_size=1, latch = True)
#rate = rospy.Rate(10) # 10hz

#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

speedvw = Twist()

 
  
def setspeeds(l,r):
        print(l)
        print(r)
        speedvw.linear.x= (l+r)/2
        speedvw.angular.z=(r-l)/width
        pub.publish(speedvw)
        
def setspeedsvw(v,w):
        speedvw.linear.x= v
        speedvw.angular.z=w
        pub.publish(speedvw)
    
    

