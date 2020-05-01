#!/usr/bin/env python
# license removed for brevity
import rospy

from Tkinter import *
import Lab2Tasks
import SetSpeeds

rospy.init_node('lab2', anonymous=True)
rate = rospy.Rate(10) # 10hz
    
def on_shutdown():
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0)

    rate.sleep()
    
class Application(Frame):
    function = ""
    def Task2(self):
        self.function = "Task2"
        self.quit()
    def Task3(self):
        self.function = "Task3"
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT    \n"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        self.QUIT.grid(row=0, column=0,ipadx=150, ipady=150, sticky="ew")

        
        self.T2 = Button(self)
        self.T2["text"] = "Task2\n(PID)"
        self.T2.grid(row=0, column=1,ipadx=150, ipady=150, sticky="ew")
        self.T2["command"] =  self.Task2
        
        self.T3 = Button(self)
        self.T3["text"] = "Task3\n(Wall Following)"
        self.T3.grid(row=0, column=2,ipadx=150, ipady=150, sticky="ew")

        self.T3["command"] =  self.Task3
 

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
        if(app.function=="Task2"):
            print("Task2")
            Lab2Tasks.Task2()
        elif(app.function=="Task3"):
            print("Task2")
            Lab2Tasks.Task3()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
