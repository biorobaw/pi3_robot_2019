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

        self.hi_there = Button(self)
        #str = "Hello var"
        #self.hi_there["text"] = "Hello",
        #self.hi_there["text"] = str
        self.set_encoder()
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})
        self.hi_there.pack(ipadx=200)
        self.hi_there.pack(ipady=200)

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



if __name__ == '__main__':
    try:
        #prompt()
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

