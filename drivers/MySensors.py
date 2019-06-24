# This is a supporting file for the raspberry pi robot to control the
# VL53L0X distance sensors using the library and example code from:
# https://github.com/johnbryanmoore/VL53L0X_rasp_python

import sys
import os
import time
import RPi.GPIO as GPIO
#add path to VL53L0X library location
sys.path.append(os.path.abspath("/home/pi/catkin_ws/src/pi3_robot_2019/drivers/VL53L0X_rasp_python/python"))
import VL53L0X


# shutdown pin of each sensor (left cener right)
shdn_pin = [27, 22 , 23]

# sensor (assigned the respective i2c ids)
sensor = [VL53L0X.VL53L0X(address=i) for i in [0x2D, 0x2B, 0x2F] ]


# name tags
SLEFT  = 0
SFRONT = 1
SRIGHT = 2


GPIO.setwarnings(False)

def initSensors():
    
    #init GPIO
    GPIO.setmode(GPIO.BCM)
    
    # Setup GPIO for shutdown pins on each VL53L0X
    for i in range(0,3):
		GPIO.setup(shdn_pin[i], GPIO.OUT)
		GPIO.setup(shdn_pin[i], GPIO.LOW)
    
    # Keep all low for 500 ms or so to make sure they reset
    time.sleep(0.50)

    # For each sensor: set shutdown pin high then start ranging
    for i in range(0,3):
		GPIO.output(shdn_pin[i], GPIO.HIGH)
		time.sleep(0.50)
		sensor[i].start_ranging(VL53L0X.VL53L0X_BETTER_ACCURACY_MODE)
		

#function to get distance
def get_inches(id = None):
	if id == None:
		return [sensor[id].get_distance() / 25.4 for id in range(3)]
	return sensor[id].get_distance() / 25.4

def get_mm(id = None):
	if id == None:
		return [sensor[id].get_distance() for id in range(3)]
	return sensor[id].get_distance()

def get_cm(id = None):
	if id == None:
		return [sensor[id].get_distance() / 10.0 for id in range(3)]
	return sensor[id].get_distance() / 10.0

def get_meters(id = None):
	if id == None:
		return [sensor[id].get_distance() / 1000.0 for id in range(3)]
	return sensor[id].get_distance() / 1000.0

#run this function before exiting the lab
def exitSensors():
	for i in range(3):
		sensor[i].stop_ranging()
		GPIO.output(shdn_pin[i], GPIO.LOW)


if __name__=='__main__':
	import signal
	try:
		# initialize sensor
		initSensors()
		
		# take initial distance measurement
		# measure how long it takes to compue 
		tic = time.clock()
		get_cm()
		toc = time.clock()
		average = (toc - tic) # time in s

		# measure how long the function takes on average:
		for i in range(100):
			tic = time.clock()
			cms = get_cm()
			toc = time.clock()
			delta = (toc - tic)
			average = 0.9 * average + 0.1 * delta
			time.sleep(0.1) # try different values
		
		average *= 1000000 # convert to ns
		print("Average read time: ",average)
				

		# do the experiment, but adding prints in between
		while True:
			tic = time.clock()
			cms = get_cm()
			toc = time.clock()
			delta = (toc - tic)*1000000
			average = 0.9 * average + 0.1 * delta
			cms_int = [int(cm) for cm in cms] 
			print(cms_int, int(average), int(delta))
			time.sleep(0.1) #try different values  and see what happens (0 , 0.01, 0.1)
	except KeyboardInterrupt:
		print('exception caught, exiting...')
		exitSensors()
	


