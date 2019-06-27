#!/usr/bin/env python

# This file implements the main controller for the robot.
# The file creates a ros node: /pi3_robot_2019_{ROBOT_ID}_robot
# The file creates the following:
# Service Servers:
# 	/pi3_robot_2019_{ROBOT_ID}}/run_function : pi3_robot_2019/RunFunction
#		execute the function specified in the message
#		see variable function_map for list of possible functions
#		currently used to start subservices
# Subscribers:
#   /pi3_robot_2019_{ROBOT_ID}/speed_vw : geometry_msgs/Twist
#		sets the speeds of the robot according to the desired (v,w)


import sys
import os
import rospy
import signal
from geometry_msgs.msg import Twist
driver_folder = "/home/pi/catkin_ws/src/pi3_robot_2019/drivers"
sys.path.append(os.path.abspath(driver_folder))
import MyServos
import subprocess
from pi3_robot_2019.srv import RunFunction
from pi3_robot_2019.srv import RunFunctionRequest
from pi3_robot_2019.srv import RunFunctionResponse
import json


# ================= BASIC SERVICES ====================================

# name of the robot node
def robot_ros_name():
	return 'pi3_robot_2019_'+robot_id

# call back function for speed_vw subscriber
def set_speeds_vw(twist):
  # rospy.loginfo("speed vw: {:.3f}   {:.3f}".format(twist.linear.x, twist.angular.z) )
  MyServos.setSpeedsVW_MPS(twist.linear.x, twist.angular.z) 
  
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

# ================ RUN FUNCTION SERVICE FUNCTIONS =====================

	
# function to start the distance sensor
distance_sensors = None
def init_distance_sensors(params):
	global distance_sensors
	if distance_sensors==None:
		
		# get rate from params (default = 20)
		print ('params', params)
		rate = params[0] if len(params)>0 else '20'
		
		distance_sensors = subprocess.Popen([
			"rosrun",
			"pi3_robot_2019",
			"distance_sensor_publisher.py",
			"_rate:=" + rate
		])
	return 'ok'
			
# function to start the camera
camera = None
def init_camera(params):
	global camera
	if camera==None:
		camera = subprocess.Popen([
			"rosrun",
			"raspicam_node",	# google raspicam_node for details
			"raspicam_node"
			,"__name:="+robot_ros_name()+'_cam'
		])
	return 'ok'

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
		print('Createing node...')
		rospy.init_node(robot_ros_name()+'_robot')
		MyServos.setSpeeds(0,0)
		rospy.on_shutdown(on_shutdown)
		print('node created')
		
		# init subscribers:
		print('creating speed_vw subscriber...')
		rospy.Subscriber(robot_ros_name()+"/speed_vw",
						 Twist,
						 set_speeds_vw)
		print('Subscriber created')

		print('creating service run_function...')
		# init services:
		rospy.Service(robot_ros_name()+"/run_function",
					  RunFunction,
					  handle_run_function)
		print('Service Created')
		
		
		# spin until shutdown
		print('Waiting for commands...')
		rospy.spin()
		print('Shutting down')


	except Exception as e:
		print(e, 'quitting...')
		on_shutdown()
    
    
  
