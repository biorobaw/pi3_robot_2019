#!/usr/bin/env python

# This is a supporting file for the raspberry pi robot to control the
# Parallax Continuous Rotation Servos & PCA9685 Servo Hat using library from:
# https://github.com/adafruit/Adafruit_Python_PCA9685
from __future__ import division
import time
import MyEncoders
import RPi.GPIO as GPIO
# Import the PCA9685 module.
import Adafruit_PCA9685
import json
import os
import sys

driverFolder = '/home/pi/catkin_ws/src/pi3_robot_2019/drivers'
sys.path.append(os.path.abspath(driverFolder))

GPIO.setmode(GPIO.BCM)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()
pwm.set_pwm_freq(50)
MAX_INPUT = 23
servo_stop = 307      #No servo movement
servo_min  = 307 - MAX_INPUT #Full reverse
servo_max  = 307 + MAX_INPUT #Full foward

LEFT_SERVO  = 0
RIGHT_SERVO = 1

#Calibrate these vlaue (in meters):
HALF_WHEEL_DISTANCE = 0.05207 #4.1" full distance: 0.05"=0.05207m
WHEEL_DIAMETER = 0.066294 # 2.61"
WHEEL_CIRCUMFERENCE = 0.20827  #2.61*pi " = 8.1996" = 0.20827m


# For set speeds, input a number between -40 and 40 for each wheel 
# -MAX_INPUT is full reverse, MAX_INPUT is full foward
def setSpeeds(l_input, r_input):
    #this performs bounds checking on all inputs received
    # if the input is outside bounds, set it the the extreme boundary
    
    #l_input=-l_input # fix for inverted connections, remove if neccesary
    #r_input=-r_input # fix for inverted connections, remove if neccessary
    
    if l_input < -MAX_INPUT:
        l_input = -MAX_INPUT
    if r_input > MAX_INPUT: 
        r_input = MAX_INPUT
    if r_input < -MAX_INPUT:
        r_input = -MAX_INPUT
    if r_input > MAX_INPUT: 
        r_input = MAX_INPUT
    # Use pwm to set the correct speed to each servo -
    pwm.set_pwm(LEFT_SERVO, 0, servo_stop + l_input)
    pwm.set_pwm(RIGHT_SERVO, 0, servo_stop - r_input)

def approximage(value, table):
    length = len(table)
    left_bound = -1
    while left_bound < length -1 and table[left_bound+1] < value:
        left_bound +=1
    if left_bound == -1:
        left_bound = 0
    elif left_bound < length-1:
        mid_value = (table[left_bound]+table[left_bound+1])/2
        if value > mid_value:
            left_bound+=1
    return left_bound

def setSpeedsRPS(l_input, r_input):
    left_index = approximage(l_input,leftSpeedmap)
    right_index = approximage(r_input,rightSpeedmap)
    
    #print("setSpeeds(%d, %d)" %(left_index, right_index))
    setSpeeds(-MAX_INPUT + left_index, -MAX_INPUT + right_index)

def setSpeedsIPS(l_input, r_input):
    setSpeedsRPS(l_input/8.2, r_input/8.2)

def setSpeedsVW_IPS(v, w):
    setSpeedsIPS(v-(w*2.1), v+(w*2.1))

    
# sets the speeds in meters per second:
def setSpeedsMPS(l_input, r_input):
    setSpeedsRPS(l_input/WHEEL_CIRCUMFERENCE, r_input/WHEEL_CIRCUMFERENCE)

def setSpeedsVW_MPS(v,w):
    setSpeedsMPS( v-w*HALF_WHEEL_DISTANCE , v+ w*HALF_WHEEL_DISTANCE )

def calibrate():
    global leftSpeedmap , rightSpeedmap
    #init arrays:
    leftSpeedmap = [0 for i in range(0 , 2*MAX_INPUT+1)]
    rightSpeedmap = [0 for i in range(0 , 2*MAX_INPUT+1)]
    #set speed of servo on a range of -MAX_INPUT to MAX_INPUT
    print('Calibrating Servos, press Ctrl-C to quit...')
    x = -MAX_INPUT
    while x <= MAX_INPUT:
        # Move servo on channel O between extremes.
        MyEncoders.counts = [0,0]
        print("setSpeeds(%d, %d)" %(x, x))
        setSpeeds(x,x)
        time.sleep(1)
        print("counts = %d, %d" %(MyEncoders.counts[0], MyEncoders.counts[1]))
        if x < 0:
            leftSpeedmap[x+MAX_INPUT] = -1 * (MyEncoders.counts[0] / 32)
            rightSpeedmap[x+MAX_INPUT] = -1 * (MyEncoders.counts[1] / 32)
        else:
            leftSpeedmap[x+MAX_INPUT] = MyEncoders.counts[0] / 32
            rightSpeedmap[x+MAX_INPUT] = MyEncoders.counts[1] / 32
        x += 1

    setSpeeds(0,0)
    print(leftSpeedmap) 
    print(rightSpeedmap) 

leftPickleFile = os.path.expanduser(driverFolder + "/leftSpeedmap.json")
rightPickleFile = os.path.expanduser(driverFolder+"/rightSpeedmap.json")

leftSpeedmap = []
rightSpeedmap = []

def saveCalibration():
    print("SAVING: ")
    print(leftSpeedmap)
    print(rightSpeedmap)
    json.dump(leftSpeedmap,open(leftPickleFile,"wb+"))
    json.dump(rightSpeedmap,open(rightPickleFile,"wb+"))
    
def restoreDefaults():
    global leftSpeedmap, rightSpeedmap
    leftSpeedmap = [-0.75,-0.75,-0.75,-0.75,-0.75,-0.75, -0.78125, -0.75, -0.75, -0.6875, -0.6875, -0.65625, -0.59375, -0.5625, -0.53125, -0.46875, -0.40625, -0.375, -0.3125, -0.28125, -0.25, -0.1875, -0.125, -0.0625, -0.03125, 0.0, 0.0, 0.09375, 0.125, 0.1875, 0.25, 0.28125, 0.3125, 0.375, 0.4375, 0.5, 0.5, 0.59375, 0.59375, 0.65625, 0.6875, 0.71875, 0.71875, 0.78125, 0.78125, 0.78125, 0.78125, 0.78125, 0.78125, 0.78125, 0.78125]
    rightSpeedmap = [-0.75,-0.75,-0.75,-0.75,-0.75-0.75, -0.75, -0.75, -0.71875, -0.71875, -0.65625, -0.65625, -0.59375, -0.5625, -0.5, -0.46875, -0.40625, -0.375, -0.3125, -0.25, -0.21875, -0.15625, -0.125, -0.09375, -0.0, 0.0, 0.0625, 0.125, 0.15625, 0.21875, 0.25, 0.3125, 0.375, 0.4375, 0.46875, 0.53125, 0.5625, 0.59375, 0.65625, 0.6875, 0.71875, 0.71875, 0.75, 0.78125, 0.78125, 0.8125, 0.8125, 0.8125, 0.8125, 0.8125, 0.8125]
    saveCalibration()
  
def loadCalibration():
    global leftSpeedmap, rightSpeedmap
    try:
      leftSpeedmap  = json.load(open(leftPickleFile,'rb'))
      rightSpeedmap = json.load(open(rightPickleFile,'rb'))
    except IOError :
      restoreDefaults()
     
loadCalibration()

print(leftSpeedmap)
print(rightSpeedmap)
      
if __name__ == '__main__':
    raw_input("press enter to calibrate...")
    calibrate()
    saveCalibration()
