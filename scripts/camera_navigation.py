#!/usr/bin/env python


import sys
import os
import rospy
import roslib
import signal
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import numpy as np
import time
from collections import namedtuple

from std_srvs.srv import Empty
from std_srvs.srv import EmptyRequest
from std_srvs.srv import EmptyResponse

# speed vw publisher?
# camera detection subscriber?
# distance sensor subscriber?

DEBUGGING = False

Detection = namedtuple('MarkerDetection',['id','x','y','w','h','time'])
camera_detections = {}
distance_measures = [1000,1000,1000]

#start_time = time.time()
def my_time():
    return time.time()#-start_time

def set_speeds(v,w):
    # print('v,w',v,w)
    t = Twist()
    t.linear.x  = v
    t.angular.z = w
    speed_publisher.publish(t)


def new_camera_detection(msg):
    data = msg.data
    # detection format 'id, x, y, width, height' # 5 parameters
    for i in range(len(data)//5):
        id = int(data[i*5])
        x  = data[i*5+1]
        y  = data[i*5+2]
        w  = data[i*5+3]
        h  = data[i*5+4]
        camera_detections[id]=Detection(id,x,y,w,h,my_time())
        #~ if DEBUGGING:
            #~ print(camera_detections[id])
            
            
def new_distance_measure(msg):
    global distance_measures
    distance_measures = msg.data #+ (my_time(),)
    #print('new d', distance_measures)

def on_shutdown():
    set_speeds(0,0)


# kp functions:
def threshold_function(value, min_value, max_value):
    if value < min_value:
         return min_value
    if value > max_value:
         return max_value
    return value
    
def kp_control(error,kp,min_value,max_value):
    return threshold_function(kp*error, min_value, max_value)


# STATES:
DONE        = 0
EVADING     = 1
SEARCHING   = 2
CENTERING   = 3
ADVANCING   = 4



def state_done():
    set_speeds(0,0)

def state_increase_distance():
    set_speeds(0.05,0)

end_wait = 0
def state_wait():
    set_speeds(0,0)
    
max_angular = 0.6
min_angular = -0.50
def state_searching():
    set_speeds(0,0.85) # originally 0.6

min_absolute_angular = 0.6
def state_centering():
    detection = camera_detections[destination]
    w = kp_control(-detection.x, 2, min_angular, max_angular) 
    if abs(w) < min_absolute_angular:
        if w > 0:
            w=min_absolute_angular
        else:
            w=-min_absolute_angular
    # print('x, w:',detection.x,w )
    set_speeds(0,w)
        
#~ def state_find_obstacle():
    #~ set_speeds(0,0.75)
        
#~ def state_evading():
    #~ print('state evading')
    #~ pass
    
CLOSE_THRESHOLD_AREA = 0.7
CLOSE_DISTANCE = 0.08
def state_advancing():
    detection = camera_detections[destination]
    w = kp_control(-detection.x, 2, min_angular, max_angular)
    if abs(detection.x) < 0.2: 
        area = detection.w * detection.h
        #v = -kp_control(abs(area-CLOSE_THRESHOLD_AREA), 0.12/0.2, 0.02, 0.12)
        v = -kp_control(abs(distance_measures[1] - CLOSE_DISTANCE), 0.12/0.08, 0.02, 0.12)
        #v = -0.5 #sign is inverted
    else:
        v=0
    set_speeds(v,w)
    # do pid on angle while moving forward 
    pass
    
    
    
    
def switch_done():
    global state, new_command #, target_distance
    print('done')
    if new_command:
        d = distance_measures[1]
        #~ print('new command: target, d = ',destination,d)
        if  d < 0.14 :
            print('switch to increase distance', d)
            #~ target_distance = d -0.03
            state = state_increase_distance
        else:
            print('switch state searching')
            state = state_searching
        new_command = False
       
def switch_searching():
    global state
    if destination in camera_detections:
        detection = camera_detections[destination]
        if my_time() - detection.time <0.1 and abs(detection.x)<0.75:
            state = state_centering
            print('Switch to centering')

def switch_centering():
    global state
    detection = camera_detections[destination]
    if my_time() - detection.time <0.1:
        if abs(detection.x) < 0.2:
            state = state_advancing
            print('Switch to advancing')

def switch_increase_distance():
    global state
    print 'd', distance_measures[1]
    if distance_measures[1] > 0.11:
        switch_wait = my_time() + 2
        state = state_wait
        print('Switch to searching') 

def switch_wait():
    global state
    if my_time() > end_wait:
        state = state_searching
        print('Switch to searching')

#~ def switch_find_obstacle():
    #~ global state
    #~ print(distance_measures[2], target_distance)
    #~ if distance_measures[2] < target_distance:
        #~ state = state_done
        #~ print('Switch to evading')

#~ def switch_evading():
    #~ global state
    #~ if destination in camera_detections:
        #~ detection = camera_detections[destination]
        #~ if my_time() - detection.time <0.1:
            #~ state = state_centering
            #~ print('Switch to centering')

def switch_advancing():
    global state
    detection = camera_detections[destination]
    #~ if detection.time - my_time() <0.1:
        #~ if detection.w*detection.h > CLOSE_THRESHOLD_AREA:
            #~ state = state_done
            #~ print('switch to done')
    if distance_measures[1] < CLOSE_DISTANCE:
        state = state_done
        print('switch to done')


# variables
destination = -1
new_command = False
state = state_done 
#~ target_distance = 1000
state_switch_functions = {state_done:       switch_done, 
                          state_searching:  switch_searching,
                          state_centering:  switch_centering,
                          #state_find_obstacle: switch_find_obstacle,
                          #state_evading:    switch_evading,
                          state_advancing:  switch_advancing,
                          state_increase_distance : switch_increase_distance,
                          state_wait:       switch_wait
                          }
        

def execute_state_machine():
    # update state
    # print 'e'
    while True:
        old_state = state
        state_switch_functions[old_state]()
        if state == old_state:
            break
    # perform state logic
    state()
    return state != state_done
    
def process_command(msg):
    global destination,new_command
    if msg.data-1 != destination:
        destination = msg.data - 1
        new_command = True
        print('renewing',msg.data,destination)

def reset_commands(empty):
    global new_command,destination
    new_command = False
    destination = -1
    last_destination.publish(destination)
    return EmptyResponse()


if __name__ == "__main__":
    rospy.init_node('camera_navigator')
    
    try:
        # init node  and then setup clean up function
        rospy.init_node('camera_navigator')
        rospy.on_shutdown(on_shutdown)
        
        # subscribe to detection topic
        detection_subscriber = rospy.Subscriber("/color_cylinder_detector/detections",
                         Float32MultiArray,
                         new_camera_detection,
                         queue_size=1)
                         
        # subscribe to detection topic 
        distance_subscriber = rospy.Subscriber("distance_sensors/d_data",
                         Float32MultiArray,
                         new_distance_measure,
                         queue_size=1)
        
        # create publisher, then publish at given rate
        speed_publisher = rospy.Publisher('speed_vw',
                            Twist,queue_size=1)
                            
        # create subscriber to wait for commands
        command_listener = rospy.Subscriber("~commands",
                                            Int32,
                                            process_command,
                                            queue_size=1
                                            )
                                        
        reset_commands_server = rospy.Service("~reset_command",
                                                Empty,
                                                reset_commands)
        
        last_destination = rospy.Publisher("~last_destination",
                                                Int32,
                                                latch=True,
                                                queue_size=1)
        last_destination.publish(destination)
        
        # create publisher to publish las completed task
                            
        # control cycle is 10Hz                    
        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            if DEBUGGING:
                val = raw_input("Next feeder")
                destination = int(val)-1
                new_command = True
            if new_command:
                while not rospy.is_shutdown() and execute_state_machine()  :
                    rate.sleep()
                last_destination.publish(destination+1)
            rate.sleep()
                    

    except Exception as e:
        print(e, 'quitting...')
        on_shutdown()



