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


rospy.init_node('lab1', anonymous=True)
rate = rospy.Rate(10) # 10hz


    
def on_shutdown():
    rospy.loginfo("Shutting down")
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
    def orien(self):
        self.function = "orien"
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
        
        self.orientation = Button(self)
        self.orientation["text"] = "Orientation",
        self.orientation["command"] = self.orien

        self.orientation.pack({"side": "left"})
        self.orientation.pack(ipadx=200)
        self.orientation.pack(ipady=200)

        self.sshape.pack({"side": "left"})
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
class Forward_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.RUN = Button(self)
        self.RUN["text"] = "RUN\n\n\n\n\n\nEnter values for Inches \nand Seconds respectively"
        self.RUN["fg"]   = "red"
        
        self.RUN.pack({"side": "left"})
        self.RUN.pack(ipadx=200)
        self.RUN.pack(ipady=200)
        self.RUN["command"] =  self.run

        
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
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
class Orientation_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.RUN = Button(self)
        self.RUN["text"] = "RUN\n\n\n\n\n\nEnter values for Degrees \nand Seconds respectively"
        self.RUN["fg"]   = "red"
        
        self.RUN.pack({"side": "left"})
        self.RUN.pack(ipadx=200)
        self.RUN.pack(ipady=200)
        self.RUN["command"] =  self.run

        
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
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    
class SShape_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.RUN = Button(self)
        self.RUN["text"] = "RUN\n\n\n\n\n\nEnter values for R1, R2 \nand Y(Seconds) respectively"
        self.RUN["fg"]   = "red"
        
        self.RUN.pack({"side": "left"})
        self.RUN.pack(ipadx=200)
        self.RUN.pack(ipady=200)
        self.RYB["command"] =  self.run

        
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
        if(app.function == "orien"):
            root = Tk()
            app = Orientation_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Orientation(app.x_var.get(), app.y_var.get(), rate)
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
