#!/usr/bin/env python

# This file implements a ros publisher for the distance sensor
# rosparameters:
#	_robot_id  :  used for node and topic names
#	_rate      :  ideal data generation frequency
# topics:
#	/pi3_robot_2019_{ROBOT_ID}/d_data : Float32MultiArray


import sys
import os
import rospy
import signal
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
driver_folder="/home/pi/catkin_ws/src/pi3_robot_2019/drivers"
sys.path.append(os.path.abspath(driver_folder))
import MySensors
import json

# name of the robot node
def robot_ros_name():
	return 'pi3_robot_2019_' + robot_id

# get and pack data
def pack_data():
	msg = Float32MultiArray()
	msg.data = MySensors.get_meters()
	msg.layout.data_offset = 0
	dim = MultiArrayDimension()
	dim.label = 'num_sensors'
	dim.size = 3
	dim.stride = 1
	msg.layout.dim = [dim]
	return msg 

def on_shutdown():
	if rospy.has_param('~rate'):
		rospy.delete_param('~rate')
	MySensors.exitSensors()

if __name__ == '__main__':
	# print(os.environ['ROS_IP'])
	# print(os.environ['ROS_MASTER_URI'])
	# get robot id
	try:
		robot_id = json.load(open(driver_folder + '/robot_id.json','rb'))
	except IOError :
		print('Could not find {}/robot_id.json'.format(driverFolder,))
		exit(-1)
	
	try:
		#init node, sensors and then setup clean up function
		rospy.init_node('distance_sensors')
		MySensors.initSensors()
		rospy.on_shutdown(on_shutdown)
		
		# create publisher, then publish at given rate
		sensor_publisher = rospy.Publisher('~d_data',
						    Float32MultiArray,queue_size=1)
		para_rate = int(rospy.get_param('~rate','50'))
		print('publishing rate: ',para_rate)
		rate = rospy.Rate(para_rate)
		while not rospy.is_shutdown():
			sensor_publisher.publish(pack_data())
			rate.sleep()
			
	except Exception as e:
		print(e, 'quitting...')
		on_shutdown()
			
