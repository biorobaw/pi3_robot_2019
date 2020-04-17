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

    
def Distance(X, Y): 
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

def Orientation(Degrees, Seconds): 
    #linSpeed = X/Y
    rate = rospy.Rate(10)
    SetSpeeds.setspeedsvw(0,Degrees*math.pi/(180*Seconds))
    
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
    TIME = rospy.get_time() - TIME
    SetSpeeds.setspeeds(0,0)
    print(r-rInit)
    print(l-lInit)
    print(c)
    print("Time: " + str(TIME))


def Task4(H, W, Y):
    speed = 2*(H+W)/Y
    if(speed>6):
        print("Higher than max speed")
        return
       
    
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    
    l=0
    r=0
    SetSpeeds.setspeeds(speed,speed)
    TIME = rospy.get_time()
    print((r-rInit)*32.0/circumference)
    while ((r-rInit)*circumference/32<H and (l-lInit)*circumference/32<H):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
    
    Orientation(-90,2)
    
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
 
        
    SetSpeeds.setspeeds(speed, speed)
    while ((r-rInit)*circumference/32<W and (l-lInit)*circumference/32<W):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
    
    Orientation(-90,2)
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
  
    SetSpeeds.setspeeds(speed, speed)
    while ((r-rInit)*circumference/32<H and (l-lInit)*circumference/32<H):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
    
    Orientation(-90,2)
    
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
        
    SetSpeeds.setspeeds(speed, speed)
    while ((r-rInit)*circumference/32<W and (l-lInit)*circumference/32<W):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]   
    TIME = rospy.get_time() - TIME
    SetSpeeds.setspeedsvw(0,0)
    print("TIME: " +str(TIME)) 

   
   
def Circle(R, Y):
    halfcircum = R*math.pi
    V = (halfcircum)/Y
    W= -V/R

    
    c1 = abs((halfcircum+2.1)*32/circumference)
    c2 = abs((halfcircum-2.1)*32/circumference)
    
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    
    l=0
    r=0
    print("V: "+str(V) +"W: " +str(W))
    SetSpeeds.setspeedsvw(V,W)
    TIME = rospy.get_time()    
    while (r-rInit<c2 and l-lInit<c1):
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
    
    
    
    

    

