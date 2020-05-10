#!/usr/bin/env python
# license removed for brevity
import rospy
import math

from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse
import SetSpeeds 
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension

#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)



#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
sensorwidth = 3
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

sense = (0.0, 0.0, 0.0) 

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)
def Task2():
    rate =rospy.Rate(10)
    global sense
    while not rospy.is_shutdown():
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701 
        rate.sleep()
        print("Not Solved Yet")
        return

def Task3():
    rate =rospy.Rate(10)
    global sense
    while not rospy.is_shutdown():
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701 
        rate.sleep()
        print("Not Solved Yet")
        return
        


            
    
    
    
