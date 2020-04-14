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
from robot_client.srv import GetSensor
from robot_client.srv import GetSensorRequest
from robot_client.srv import GetSensorResponse
from robot_client.srv import RunFunction
from robot_client.srv import RunFunctionRequest
from robot_client.srv import RunFunctionResponse

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension

from Tkinter import *




speedvw = Twist()

      
def on_shutdown():
    rospy.loginfo("Shutting down")
    rate.sleep()
    rate.sleep()

    rate.sleep()

def distance_sensors(msg):
        print("ahhhhh")
        print(msg.data)


if __name__ == '__main__':
    try:
        #prompt()
        
        #print('Subscriber created')
        
        rospy.init_node('d_dataSub', anonymous=True)
        rate = rospy.Rate(10) # 10hz
        rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray,
                         distance_sensors)
        print('Subscriber created')
        rospy.spin()
        #root.destroy()
        #app.mainloop()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
        pass
    except Exception as e:
        on_shutdown()
        rospy.loginfo("InteruptException")
        pass


