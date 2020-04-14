#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String

def talker():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz
    i=1
    while not rospy.is_shutdown():
        #hello_str = "hello world %s" % rospy.get_time() + str(i)
	hello_str = "hello world %s" + str(i)
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()
	i= i+1

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass
