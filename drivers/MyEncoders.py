#!/usr/bin/env python

# This is a supporting file for the raspberry pi robot to control the
# wheel encoders
import RPi.GPIO as GPIO
import time
import os

LEFT_ENCODER  = 18
RIGHT_ENCODER = 17
counts = [0,0]


# seems to me that
# this function is triggered when an event is detected from either encoder
def iencoder(channel):
  # increment the count of the respective encoder by 1
  if channel == 18:
    counts[0] += 1
  if channel == 17:
    counts[1] += 1

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
	
