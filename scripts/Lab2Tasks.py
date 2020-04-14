#!/usr/bin/env python
# license removed for brevity
import rospy
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse
import SetSpeeds 
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension


#============================Creates publisher to send speeds=================
pub = rospy.Publisher('pi3_robot_2019/r1/speed_vw', Twist, queue_size=1, latch = True)



#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)



#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

global sense
sense = (0.0, 0.0, 0.0) 
print("Type: " +str(type(sense[0])))

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)
    
def wallfollow1(rospy):
    rate =rospy.Rate(10)
    print("trying")
    global sense
    maxspeed = 5
    k=.5

    while not rospy.is_shutdown():
        
        print("trying")
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701
        print("left: " +str(l) +" front: " +str(f) + "right: " +str(r))
        fronterror = (f-5)*k
        if(fronterror>maxspeed):
             fronterror = maxspeed
            
        if(l<r):
            wallerror = (l-5)*k
            if(wallerror>0):
                  SetSpeeds.setspeeds(fronterror-wallerror,fronterror)
            else:
                SetSpeeds.setspeeds(fronterror,fronterror+wallerror)
        else:
            wallerror = (r-5)*k
            if(wallerror>0):
                   SetSpeeds.setspeeds(fronterror,fronterror-wallerror)
            else:
                SetSpeeds.setspeeds(fronterror+wallerror,fronterror)        
        rate.sleep()

            
    
    
    
