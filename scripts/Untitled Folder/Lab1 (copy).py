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




#============================Creates publisher to send speeds=================
rospy.init_node('lab1', anonymous=True)
pub = rospy.Publisher('pi3_robot_2019/r1/speed_vw', Twist, queue_size=1, latch = True)
rate = rospy.Rate(10) # 10hz


#==========================Creates Service to request encoder information
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

speedvw = Twist()


#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612


def lab1():
    print("Press \n1 for Forward:\n2 for SShape: ")
    X = int(input()) #20
    if(X==1):
        Forward()
    else:
        SShape()


def SShape():
    print("Enter a value for R1(inches): ") 
    R1 = float(input()) #5
    print("Enter a value for R2(inches): ") 
    R2 = float(input()) #5
    print("Enter a value for Y(seconds): ") 
    Y = float(input()) #10
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
    speedvw.linear.x=V1
    speedvw.angular.z=W1
    
    TIME = rospy.get_time()
    pub.publish(speedvw)
    
    while (r-rInit<c2 and l-lInit<c1):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        
        #print(encod)
        
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
    
    
    speedvw.linear.x=V1
    speedvw.angular.z=W2
    pub.publish(speedvw)
    while (r-rInit<c1 and l-lInit<c2):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        
        #print(encod)
        
    TIME = rospy.get_time() - TIME
    speedvw.linear.x=0
    speedvw.angular.z=0
    pub.publish(speedvw)
    print("TIME: " +str(TIME))
        
    print(r-rInit)
    print("c1: "+str(c1))
    print(l-lInit)
    print("c2: "+str(c2))
    
def Forward():
    

    
    
    print("Enter a number for X(in inches): ")
    X = float(input()) #20
    print("Enter a number for Y(in seconds): ")
    Y = float(input()) #4
    
    linSpeed = X/Y
    
    speedvw.linear.x=linSpeed
    speedvw.angular.z=0
    c = abs(X*32/circumference)
    encod =  get_encoder().result
    
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    
    l=0
    r=0
    
    rospy.loginfo(speedvw)
    pub.publish(speedvw)
    TIME = rospy.get_time()
    while (r-rInit<c and l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        
        #print(encod)
        

    
    TIME = rospy.get_time() - TIME
    speedvw.linear.x=0
    speedvw.angular.z=0
    pub.publish(speedvw)
    print(TIME)
    print(((r-rInit)*circumference/32))
    print(((l-lInit)*circumference/32))
    
    #while not rospy.is_shutdown():
        
        
        
    
        
    
    
    #time.sleep(3)
    #speedvw.linear.x=2
    #speedvw.angular.z=0
    
    #rate.sleep()
    #rospy.loginfo(speedvw)
    #pub.publish(speedvw)
    #time.sleep(1)
    
    #speedvw.linear.x=0
    #speedvw.angular.z=0
    #pub.publish(speedvw)
    #rospy.loginfo(speedvw)
    
    
    
    
def on_shutdown():
    rospy.loginfo("Shutting down")
    rate.sleep()
    rate.sleep()
    speedvw.linear.x=0
    speedvw.angular.z=0
    pub.publish(speedvw)
    rospy.loginfo(speedvw)
    rate.sleep()
    


if __name__ == '__main__':
    try:
        rospy.on_shutdown(on_shutdown)
        lab1()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
