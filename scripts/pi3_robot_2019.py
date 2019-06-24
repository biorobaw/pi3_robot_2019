#!/usr/bin/env python

import sys
import os
import rospy
import signal
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
sys.path.append(os.path.abspath("/home/pi/catkin_ws/src/pi3_robot_2019/drivers"))
import MyServos
import MySensors
import subprocess


# variables
robot_id = 'b1' # id of the robot
sensor_frequency = 50 # sensor measurement frequency

# name of the robot node
def robot_ros_name():
	return 'pi3_robot_2019_'+robot_id

# call back function to set speeds
def set_speeds_vw(twist):
  # rospy.loginfo("speed vw: {:.3f}   {:.3f}".format(twist.linear.x, twist.angular.z) )
  MyServos.setSpeedsVW_MPS(twist.linear.x, twist.angular.z) 
  
def pack_sensor_data():
	msg = Float32MultiArray()
	msg.data = MySensors.get_meters()
	msg.layout.data_offset = 0
	dim = MultiArrayDimension()
	dim.label = 'num_sensors'
	dim.size = 3
	dim.stride = 1
	msg.layout.dim = [dim]
	return msg 

# call back function for cleaning up
def on_shutdown():
	global camera
	if camera != None:
		camera.terminate()
	MyServos.setSpeeds(0,0)
	MySensors.exitSensors()
	
	  
# function to start the camera	  
camera = None
def initCamera():
	global camera
	if camera==None:
		camera = subprocess.Popen(["rosrun","raspicam_node","raspicam_node","__name:="+robot_ros_name()+'_cam'])
	
  
if __name__ == '__main__':
	try:
		# init basic robot modules
		MyServos.setSpeeds(0,0)
		MySensors.initSensors()

		# init ros node and set on shutdown method
		rospy.init_node(robot_ros_name()+'_robot')
		rospy.on_shutdown(on_shutdown)

		# create subscriber for speed commands
		rospy.Subscriber(robot_ros_name()+"/speed_vw",Twist,set_speeds_vw)

		initCamera()
		
		# create publisher for sensor data
		sensor_publisher = rospy.Publisher(robot_ros_name()+'/sensor_data',Float32MultiArray,queue_size=1)


		# publish data until the program closes
		rate = rospy.Rate(sensor_frequency)
		while not rospy.is_shutdown():
			sensor_publisher.publish(pack_sensor_data())
			rate.sleep()
	except:
		on_shutdown()
    
    
  
