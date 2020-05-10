#!/usr/bin/env python

# This file implements the main controller for the robot.
# It should not be called directly, instead use the launch file
# The file creates a ros node: /pi3_robot_2019/{ROBOT_ID}
# The file creates the following:
# Service Servers:
# 	/pi3_robot_2019/{ROBOT_ID}}/run_function : pi3_robot_2019/RunFunction
#		execute the function specified in the message
#		see variable function_map for list of possible functions
#		currently used to start subservices
# Subscribers:
#   /pi3_robot_2019/{ROBOT_ID}/speed_vw : geometry_msgs/Twist
#		sets the speeds of the robot according to the desired (v,w)


import sys
import os
import rospy
import signal
from geometry_msgs.msg import Twist
driver_folder = "/home/pi/catkin_ws/src/pi3_robot_2019/drivers"
sys.path.append(os.path.abspath(driver_folder))
import MyServos
import MyEncoders
import MySensors
import subprocess
from pi3_robot_2019.srv import RunFunction
from pi3_robot_2019.srv import RunFunctionRequest
from pi3_robot_2019.srv import RunFunctionResponse
from pi3_robot_2019.srv import GetEncoder
from pi3_robot_2019.srv import GetEncoderRequest
from pi3_robot_2019.srv import GetEncoderResponse
from pi3_robot_2019.srv import GetSpeeds
from pi3_robot_2019.srv import GetSpeedsRequest
from pi3_robot_2019.srv import GetSpeedsResponse

import json


# ================= BASIC SERVICES ====================================

# call back function for speed_vw subscriber
def set_speeds_vw(twist):
  rospy.loginfo("speed vw: {:.3f}   {:.3f}".format(twist.linear.x, twist.angular.z) )
  MyServos.setSpeedsVW_IPS(twist.linear.x, twist.angular.z) 
  
# call back fuction implementing run_function service routine
def handle_run_function(request):
	fun_id = request.function_id
	params = request.params
	return RunFunctionResponse(str(function_map[fun_id](params)))

# call back function for cleaning up
def on_shutdown():
	global camera, distance_sensors
	if camera != None:
		camera.terminate()
	if distance_sensors != None:
		distance_sensors.terminate()
	MyServos.setSpeeds(0,0)


# ================ RUN GET ENCODER FUNCTIONS =====================
def handle_get_encoder(self):
	counts = MyEncoders.counts
	return GetEncoderResponse(counts)

def handle_get_speeds(self):
	ret = MyEncoders.getInstantaneousSpeed()
	return GetSpeedsResponse(ret)


# ================ RUN FUNCTION SERVICE FUNCTIONS =====================

	
# function to start the distance sensor
distance_sensors = None
def init_distance_sensors(params):
	global distance_sensors
	print ("\ninit sensors\n")
	if distance_sensors==None:
		
		# get rate from params (default = 20)
		print ('params', params)
		print ("\ninit sensors\n")
		rate = params[0] if len(params)>0 else '20'
		
		distance_sensors = subprocess.Popen([
			"rosrun",
			"pi3_robot_2019",
			"distance_sensor_publisher.py",
			"_rate:=" + rate,
			"__ns:=" + rospy.get_name()
		])
	else:
		print("ELSE")
	return 'ok'
			
# function to start the camera
camera = None
def init_camera(params):
	global camera
	if camera==None:
		if len(params)==3:
			camera = subprocess.Popen([
				"rosrun",
				"raspicam_node",	# google raspicam_node for details
				"raspicam_node",
				"_width:="+str(params[0]),
				"_height:="+str(params[1]),
				"_framerate:=30", #actual framerate is 1/3 chosen value
				"_quality:="+str(params[2]),
				"_ISO:=200",
				"_shutter_speed:=100000",
				"_saturation:=50",
				"_awb_mode:=horizon",
				"__ns:="+rospy.get_name(),
				"__name:=cam"
			])
		else:
			camera = subprocess.Popen([
				"rosrun",
				"raspicam_node",	# google raspicam_node for details
				"raspicam_node",
				"_width:=320",
				"_height:=240",
				"_framerate:=30", #actual framerate is 1/3 chosen value
				"_quality:=100",
				"_ISO:=200",
				"_shutter_speed:=100000",
				"_saturation:=50",
				"_awb_mode:=horizon",
				"__ns:="+rospy.get_name(),
				"__name:=cam"
			])
		return 'ok'
	if(len(params) >0 and params[0]=='kill'):
		camera.send_signal(subprocess.signal.SIGINT)
		camera=None	
		return 'killed'
		
	camera.send_signal(subprocess.signal.SIGINT)
	camera=None	
	return init_camera(params)
	

# list of functions
function_map = {
	'init_camera': init_camera ,
	'init_distance_sensors': init_distance_sensors
}

# ================ MAIN FUNCTION ======================================
  
if __name__ == '__main__':
	
	# get robot id
	try:
		robot_id = json.load(open(driver_folder + '/robot_id.json','rb'))
	except IOError :
		  print('Could not find {}/robot_id.json'.format(driverFolder,))
		  exit(-1)
	
	
	try:
		# init node and stop servos, then set shutdown cleanup function
		print('Creating node...')
		rospy.init_node(robot_id)
		MyServos.setSpeeds(0,0)
		rospy.on_shutdown(on_shutdown)
		print('node created')
		
		# init subscribers:
		print('creating speed_vw subscriber...')
		rospy.Subscriber("~speed_vw",
						 Twist,
						 set_speeds_vw)
		print('Subscriber created')

		print('creating service run_function...')
		# init services:
		rospy.Service("~run_function",
					  RunFunction,
					  handle_run_function)
		print('Service Created')
		rospy.Service("~get_encoder",
					  GetEncoder,
					  handle_get_encoder)

		rospy.Service("~get_speeds",
					  GetSpeeds,
					  handle_get_speeds)
		
		
		# spin until shutdown
		print('Waiting for commands...')
		#init_camera(None)
		init_distance_sensors(['10'])
		rospy.spin()
		print('Shutting down')


	except Exception as e:
		print(e, 'quitting...')
		on_shutdown()
    
    
  
