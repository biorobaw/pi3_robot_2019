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


#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

speedvw = Twist()


#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

def SShape(R1, R2, Y):
    halfcircum1 = R1*math.pi
    halfcircum2 = R2*math.pi
    
    V1 = (halfcircum1+halfcircum2)/Y
    W1= -V1/R1
    W2= V1/R2
    
    c1 = abs((halfcircum1+2.1)*32/circumference)
    c2 = abs((halfcircum1-2.1)*32/circumference)
    
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    
    l=0
    r=0
    print("V: "+str(V1) +"W: " +str(W1))
    SetSpeeds.setspeedsvw(V1,W1)
    print("speedsset")
    TIME = rospy.get_time()    
    while (r-rInit<c2 and l-lInit<c1):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
                
    print(r-rInit)
    print("c2: "+str(c2))
    print(l-lInit)
    print("c1: "+str(c1))
    
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
        
    c1 = abs((halfcircum2+2.1)*32/circumference)
    c2 = abs((halfcircum2-2.1)*32/circumference)
    print("V: "+str(V1) +"W: " +str(W2))
    
    SetSpeeds.setspeedsvw(V1, W2)
    while (r-rInit<c1 and l-lInit<c2):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]   
    TIME = rospy.get_time() - TIME
    SetSpeeds.setspeedsvw(0,0)
    print("TIME: " +str(TIME)) 
    print(r-rInit)
    print("c1: "+str(c1))
    print(l-lInit)
    print("c2: "+str(c2))
    
def Forward(X, Y): 
    linSpeed = X/Y
    SetSpeeds.setspeeds(linSpeed,linSpeed)
    
    c = abs(X*32/circumference)
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    
    TIME = rospy.get_time()
    while (r-rInit<c and l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
    TIME = rospy.get_time() - TIME
    SetSpeeds.setspeeds(0,0)
    print("Time: " + str(TIME))

def Orientation(Degrees, Seconds, rate): 
    #linSpeed = X/Y
    #rate = rospy.Rate(10)
    SetSpeeds.setspeedsvw(0,Degrees*math.pi/(180*Seconds))
    
    c = 2*math.pi*(width/2) * (Degrees*1.00/360)*(32/circumference) #circumference of circle times how many rotations
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
    TIME = rospy.get_time() - TIME
    SetSpeeds.setspeeds(0,0)
    print(r-rInit)
    print(l-lInit)
    print(c)
    print("Time: " + str(TIME))
   
    
    
    
    

    

