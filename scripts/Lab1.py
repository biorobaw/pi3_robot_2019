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
import Lab1Tasks


#speedvw = Twist()
rospy.init_node('lab1', anonymous=True)
rate = rospy.Rate(10) # 10hz


    
def on_shutdown():
    rospy.loginfo("Shutting down")
    rate.sleep()
    rate.sleep()
    #speedvw.linear.x=0
    #speedvw.angular.z=0
    #pub.publish(speedvw)
    #rospy.loginfo(speedvw)
    rate.sleep()
    
    
#==========================GUI STUFF================
class Application(Frame):
    function = ""
    def forw_b(self):
        self.function = "forward"
        self.quit()
    def sshape_b(self):
        self.function = "sshape"
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=200)
        self.QUIT.pack(ipady=200)

        self.forward = Button(self)
        self.forward["text"] = "Forward",
        self.forward["command"] = self.forw_b

        self.forward.pack({"side": "left"})
        self.forward.pack(ipadx=200)
        self.forward.pack(ipady=200)

        self.forward.pack({"side": "left"})
        
        self.sshape = Button(self)
        self.sshape["text"] = "SShape",
        self.sshape["command"] = self.sshape_b

        self.sshape.pack({"side": "left"})
        self.sshape.pack(ipadx=200)
        self.sshape.pack(ipady=200)

        self.sshape.pack({"side": "left"})
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
class Forward_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "RUN\n\n\n\n\n\nEnter values for Inches \nand Seconds respectively"
        self.QUIT["fg"]   = "red"
        
        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=200)
        self.QUIT.pack(ipady=200)     
        
        self.x_cont = Entry()
        self.x_cont.pack()
        self.x_cont.pack(ipadx=200)
        self.x_cont.pack(ipady=50)

        # here is the application variable
        self.x_var = IntVar()
        # set it to some value
        self.x_var.set(0)
        # tell the entry widget to watch this variable
        self.x_cont["textvariable"] = self.x_var

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.x_cont.bind('<Key-Return>',
                              self.print_contents)
        self.QUIT["command"] =  self.run
        
        self.y_cont = Entry()
        self.y_cont.pack()
        self.y_cont.pack(ipadx=200)
        self.y_cont.pack(ipady=50)

        # here is the application variable
        self.y_var = IntVar()
        # set it to some value
        self.y_var.set(0)
        # tell the entry widget to watch this variable
        self.y_cont["textvariable"] = self.y_var

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.y_cont.bind('<Key-Return>',
                              self.print_contents)
        self.QUIT["command"] =  self.run

    def print_contents(self, event):
        print "hi. contents of entry is now ---->", \
              self.x_var.get()
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    
class SShape_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "RUN\n\n\n\n\n\nEnter values for R1, R2 \nand Y(Seconds) respectively"
        self.QUIT["fg"]   = "red"
        
        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=200)
        self.QUIT.pack(ipady=200)     
        
        self.R1_cont = Entry()
        self.R1_cont.pack()
        self.R1_cont.pack(ipadx=200)
        self.R1_cont.pack(ipady=50)

        # here is the application variable
        self.R1_var = StringVar()
        # set it to some value
        self.R1_var.set(0)
        # tell the entry widget to watch this variable
        self.R1_cont["textvariable"] = self.R1_var

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.R1_cont.bind('<Key-Return>',
                              self.print_contents)
        self.QUIT["command"] =  self.run
        
        self.R2_cont = Entry()
        self.R2_cont.pack()
        self.R2_cont.pack(ipadx=200)
        self.R2_cont.pack(ipady=50)

        # here is the application variable
        self.R2_var = StringVar()
        # set it to some value
        self.R2_var.set(0)
        # tell the entry widget to watch this variable
        self.R2_cont["textvariable"] = self.R2_var

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.R2_cont.bind('<Key-Return>',
                              self.print_contents)
        
        self.Y_cont = Entry()
        self.Y_cont.pack()
        self.Y_cont.pack(ipadx=200)
        self.Y_cont.pack(ipady=50)

        # here is the application variable
        self.Y_var = StringVar()
        # set it to some value
        self.Y_var.set(0)
        # tell the entry widget to watch this variable
        self.Y_cont["textvariable"] = self.Y_var

        # and here we get a callback when the user hits return.
        # we will have the program print out the value of the
        # application variable when the user hits return
        self.Y_cont.bind('<Key-Return>',
                              self.print_contents)
        self.QUIT["command"] =  self.run

    def print_contents(self, event):
        print "hi. contents of entry is now ---->", \
              self.x_var.get()
        
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
        if(app.function == "forward"):
            root = Tk()
            app = Forward_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Forward(app.x_var.get(), app.y_var.get())
        if(app.function == "sshape"):
            root = Tk()
            app = SShape_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.SShape(float(app.R1_var.get()),float(app.R2_var.get()),float(app.Y_var.get()))
            
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
