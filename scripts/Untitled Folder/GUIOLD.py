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

#import Tkinter as tk
from Tkinter import *

#from tkinter import Entry
#from tkinter import Entry

rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)


#============================Creates publisher to send speeds=================
rospy.init_node('speed_widget', anonymous=True)
pub = rospy.Publisher('pi3_robot_2019/r1/speed_vw', Twist, queue_size=1, latch = True)
rate = rospy.Rate(10) # 10hz

speedvw = Twist()

#!/usr/bin/env python
# license removed for brevity
from Tkinter import *

class Application(Frame):
    encod =  get_encoder().result
    base_l = encod[0]
    base_r = encod[1]
    
    def say_hi(self):
        print ("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        
        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=200)
        self.QUIT.pack(ipady=200)
        
        self.RESET = Button(self)
        self.RESET["text"] = "RESET"
        self.RESET["fg"]   = "red"
        self.RESET["command"] =  self.reset

        self.RESET.pack({"side": "left"})
        self.RESET.pack(ipadx=200)
        self.RESET.pack(ipady=200)
        
        
        #=====================ENCODER WIDGET==================
        self.hi_there = Button(self)
        #str = "Hello var"
        #self.hi_there["text"] = "Hello",
        #self.hi_there["text"] = str
        self.set_encoder()
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})
        self.hi_there.pack(ipadx=200)
        self.hi_there.pack(ipady=200)
        
        
        
        #========================SPEED NODE=========================
        #Right wheel speed entry
        self.r_cont = Entry()
        self.r_cont.pack()
        #self.x_cont.pack({"side": "right"})
        self.r_cont.pack(ipadx=200)
        self.r_cont.pack(ipady=50)
        
        
        #Left wheel speed entry
        self.l_cont = Entry()
        self.l_cont.pack()
        #self.x_cont.pack({"side": "right"})
        self.l_cont.pack(ipadx=200)
        self.l_cont.pack(ipady=50)
        
        # here is the application variable
        self.r_var = IntVar()
        # set it to some value
        self.r_var.set(0)
        # tell the entry widget to watch this variable
        self.r_cont["textvariable"] = self.r_var
        
        self.l_var = IntVar()
        self.l_var.set(0)
        self.l_cont["textvariable"] = self.l_var
        
        
        self.speed_widget = Button(self)
        self.speed_widget["text"] = "Enter speeds and press to run",
        self.speed_widget["command"] = self.say_hi
        
        #========================END SPEED NODE=========================
        
               

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()


    def reset(self):
        #global base_l
        #global base_r
        encod =  get_encoder().result
        self.base_l = encod[0]
        self.base_r = encod[1]
        #print(self.base_l)
        #print(self.base_r)
    def set_encoder(self):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        #l=l+
        #r=r+2
        
        #print(self.base_l)
        #print(self.base_r)
        str_var = "Left Encoder: "+ str(l-self.base_l) +" \nRight Encoder: " +str(r-self.base_r)
        #str_var = "Left Encoder: "+ str(l) +" \nRight Encoder: " +str(r)
        self.hi_there["text"] = str_var
        #self.hi_there["text"] = "Left Encoder:",
        #pass
        self.after(100, self.set_encoder)


        #print(encod)
    def set_speed(self):
      
      
      #X = app.x_var.get()
      #Y = app.y_var.get()
      r=l_var.get()
      l=r_var.get()
      speedvw.linear.x=r_var.get()
      speedvw.angular.z=0
      pub.publish(speedvw)
      
      
      
      
      
      
def on_shutdown():
    rospy.loginfo("Shutting down")
    rate.sleep()
    rate.sleep()
    speedvw.linear.x=0
    speedvw.angular.z=0
    pub.publish(speedvw)
    rospy.loginfo(speedvw)
    rate.sleep()


if __name__ == '__main__':
    try:
        #prompt()
        rospy.on_shutdown(on_shutdown)
        root = Tk()
        app = Application(master=root)
        app.mainloop()
        #root.destroy()
        #app.mainloop()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        #on_shutdown()
        pass
    except Exception as e:
        #on_shutdown()
        rospy.loginfo("InteruptException")
        pass

