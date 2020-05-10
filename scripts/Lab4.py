#!/usr/bin/env python
#import roslib
#import sys
import rospy
import Lab4Tasks
from Tkinter import *
import SetSpeeds



#==========================GUI STUFF================
class Application(Frame):
    function = ""
    def task2(self):
        #root.destroy()
        self.function = "Task2"
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
        self.forward["text"] = "Task2",
        self.forward["command"] = self.task2

        self.forward.pack({"side": "left"})
        self.forward.pack(ipadx=200)
        self.forward.pack(ipady=200)

        self.forward.pack({"side": "left"})
           

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

class Entry_GUI(Frame):
    
    def N(self):
        self.dir=0
        self.quit()
    def E(self):
        self.dir=1
        self.quit()
    def S(self):
        self.dir=2
        self.quit()
    def W(self):
        self.dir=3
        self.quit()
    def createWidgets(self):     
        self.label = Label(self)
        self.label["text"] = "Enter the # of the current cell then select the orientation of the robot"      
        self.label.grid(row=0, column=0,ipadx=100, ipady=25,sticky="ew")
        
        
        self.curcell = IntVar()
        self.curcell.set(0)
        self.cellent = Entry(self)
        self.cellent.grid(row=1, column=0,ipadx=100, ipady=25,sticky="ew")
        self.cellent["textvariable"] = self.curcell
        
        
        self.g0000N = PhotoImage(file="src/robot_client/scripts/grid_images/0000N.png")
        self.g0000E = PhotoImage(file="src/robot_client/scripts/grid_images/0000E.png")
        self.g0000S = PhotoImage(file="src/robot_client/scripts/grid_images/0000S.png")
        self.g0000W = PhotoImage(file="src/robot_client/scripts/grid_images/0000W.png")


        
        self.direntN = Button(self, text = "N", compound=CENTER, image=self.g0000N)
        self.direntN.grid(row=0, column=2,ipadx=0, ipady=0,sticky="ew")
        self.direntN["command"] =  self.N
        
        self.direntE = Button(self, text = "E", compound=CENTER, image=self.g0000E)
        self.direntE.grid(row=1, column=3,ipadx=0, ipady=0,sticky="ew")
        self.direntE["command"] =  self.E
        
        self.direntS = Button(self, text = "S", compound=CENTER, image=self.g0000S)
        self.direntS.grid(row=1, column=2,ipadx=0, ipady=0,sticky="ew")
        self.direntS["command"] =  self.S
        
        self.direntW = Button(self, text = "W", compound=CENTER, image=self.g0000W)
        self.direntW.grid(row=1, column=1,ipadx=0, ipady=0,sticky="ew")
        self.direntW["command"] =  self.W
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
        
def on_shutdown():
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0)
    
    
    
if __name__ == '__main__':
    try:
        rospy.on_shutdown(on_shutdown)
        rospy.init_node('Lab4', anonymous=True)
        rate = rospy.Rate(10) # 10hz

        root = Tk()
        app = Application(master=root)
        app.mainloop()
        root.destroy()
        if(app.function ==""):
            print("pass")
            pass
        elif(app.function =="Task2"):
            root2 = Tk()
            app2 = Entry_GUI(master=root2)
            app2.mainloop()
            root2.destroy()
            #Lab4Tasks.Task2Main(app2.curcell.get(),app2.dir)
            Lab4Tasks.Task2SingleThread(app2.curcell.get(),app2.dir)
    except Exception as e:
        print(e)