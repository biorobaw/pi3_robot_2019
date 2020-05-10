#!/usr/bin/env python
# license removed for brevity
import rospy
import math #for Robot Dimensions
from robot_client.srv import GetEncoder #For recieving Encoder info
from robot_client.srv import GetEncoderRequest 
from robot_client.srv import GetEncoderResponse
import SetSpeeds #For setting speeds


#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)



#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

    
def Task2(X, Y): 
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    print("Not Solved Yet")
    return

def Task3(Degrees, Seconds): 
    encod =  get_encoder().result                         
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    print("Not Solved Yet")
    return


def Task4(H, W, Y):
    encod =  get_encoder().result                         
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    print("Not Solved Yet")
    return

   
   
def Task5(R, Y):
    encod =  get_encoder().result                         
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    print("Not Solved Yet")
    return
    
    
    

    

