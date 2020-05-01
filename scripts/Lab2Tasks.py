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

global sense
sense = (0.0, 0.0, 0.0) 

def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)
def Task2():
    pass
def Task3():
    print("here")
    rate =rospy.Rate(10)
    global sense
    maxspeed = 5
    k=.5

    while not rospy.is_shutdown():
        
        print("trying")
        l = sense[0]*39.3701
        f = sense[1]*39.3701
        r = sense[2]*39.3701
        print("left: " +str(l) +" front: " +str(f) + "right: " +str(r))
        fronterror = (f-4)*k
        if(fronterror>maxspeed):
             fronterror = maxspeed
        
        if(l<r):
            wallerror = (l-4)*k
            if(wallerror>0):
                  SetSpeeds.setspeeds(fronterror-wallerror,fronterror)
            else:
                SetSpeeds.setspeeds(fronterror,fronterror+wallerror)
        else:
            wallerror = (r-4)*k
            if(wallerror>0):
                   SetSpeeds.setspeeds(fronterror,fronterror-wallerror)
            else:
                SetSpeeds.setspeeds(fronterror+wallerror,fronterror)
        if(f<=5 or fronterror<.5):
            SetSpeeds.setspeeds(0,0)
            if(l<r):
                Turn(90)
            else:
                Turn(-90)
            
        
        rate.sleep()
        
        
        
def Turn(Degrees): 
    print("here")
    #linSpeed = X/Y
    rate = rospy.Rate(10)
    if(Degrees >0):
        SetSpeeds.setspeeds(3,-3)
    else:
        SetSpeeds.setspeeds(-3,3)
    
    c = 2*math.pi*(width/2) * (abs(Degrees)*1.00/360)*(32/circumference) #circumference of circle times how many rotations
    encod =  get_encoder().result                              #times how many inches per tick
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    
    TIME = rospy.get_time()
    while (r-rInit<c and l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        rate.sleep()
    SetSpeeds.setspeeds(0,0)


            
    
    
    
