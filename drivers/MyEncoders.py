#!/usr/bin/env python

# This is a supporting file for the raspberry pi robot to control the
# wheel encoders
import RPi.GPIO as GPIO
import time
import rospy
from threading import Thread, Lock
import os

mutex = Lock()
LEFT_ENCODER  = 18
RIGHT_ENCODER = 17
counts = [0,0]
delta_T = [0,0]
time_stamp = [0,0]



# seems to me that
# this function is triggered when an event is detected from either encoder
def iencoder(channel):
  global counts,delta_T,time_stamp
  # increment the count of the respective encoder by 1
  time = rospy.get_time()
  id = channel-17
  mutex.acquire()
  counts[id] += 1
  delta_T[id] = time - time_stamp[id]
  time_stamp[id] = time
  mutex.release()


#def getCounts():
#    mutex.aqcuire()
#    res = [copy values]
#    mutex.release()
#    return res
    
def getInstantaneousSpeed():
    time_now = rospy.get_time()
    mutex.acquire()
    c = [counts[0], counts[1]]
    delta = [delta_T[0],delta_T[1]]
    stamps = [time_stamp[0],time_stamp[1]]
    mutex.release()
    return [1/max(time_now - stamps[0], delta[0]), 1/max(time_now - stamps[1], delta[1])]
    
    return res

# Setup the GPIO pins for both encoders
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# Add interrupt events when a rising signal is triggered
GPIO.add_event_detect(18, GPIO.RISING, callback=iencoder, bouncetime=5)
GPIO.add_event_detect(17, GPIO.RISING, callback=iencoder, bouncetime=5)


if __name__ == '__main__':
	# test encoders
	import sys
	import os
	sys.path.append(os.path.abspath("/home/pi/catkin_ws/src/pi3_robot_2019/drivers"))
	import MyServos
	
	#TODO: add test code
	
