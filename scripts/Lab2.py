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
from Tkinter import *
import Lab2Tasks
import SetSpeeds
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension

rospy.init_node('lab2', anonymous=True)
rate = rospy.Rate(10) # 10hz
    
def on_shutdown():
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0)
    rate.sleep()
    rate.sleep()
    rate.sleep()
    
class Application(Frame):
    function = ""
    def Task2(self):
        self.function = "t2"
        self.quit()
        
    def createWidgets(self):
        self.T2 = Button(self)
        self.T2["text"] = "T2"
        self.T2["fg"]   = "red"
        

        self.T2.pack({"side": "left"})
        self.T2.pack(ipadx=200)
        self.T2.pack(ipady=200)
        self.T2["command"] =  self.Task2
 

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


if __name__ == '__main__':
    try:
        rospy.on_shutdown(on_shutdown)
        root = Tk()
        app = Application(master=root)
        app.mainloop()
        root.destroy()
        if(app.function=="t2"):
            print("t2")
            Lab2Tasks.wallfollow1(rospy)
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
