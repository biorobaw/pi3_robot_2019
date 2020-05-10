#!/usr/bin/env python
# license removed for brevity
import rospy
from Tkinter import * #For GUI
import SetSpeeds #Used for setting speeds to 0 on shutdown
import Lab1Tasks #Contains student defined lab task programs


rospy.init_node('lab1', anonymous=True)
rate = rospy.Rate(10) # 10hz


    
def on_shutdown(): #Called when shutting down
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0) #Stop Robot
    rate.sleep()

    
    
#==========================GUI STUFF================
class Application(Frame):
    function = ""
    def forw_b(self):
        self.function = "Task2"
        self.quit()
    def orien(self):
        self.function = "Task3"
        self.quit()
    def rectangle(self):
        self.function = "Task4"
        self.quit()
    def circle(self):
        self.function = "Task5"
        self.quit()
    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT    \n"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=0, column=0,ipadx=150, ipady=150, sticky="ew")

        self.forward = Button(self)
        self.forward["text"] = "Task 2\n(Distance)"
        self.forward["command"] = self.forw_b

        self.forward.grid(row=0, column=1,ipadx=150, ipady=150,sticky="ew")
        
        self.orientation = Button(self)
        self.orientation["text"] = "Task 3\n(Orientation)"
        self.orientation["command"] = self.orien

        self.orientation.grid(row=0, column=2,ipadx=150, ipady=150,sticky="ew")

        
        self.rect = Button(self)
        self.rect["text"] = "Task 4\n(Rectangle)"
        self.rect["command"] = self.rectangle

        self.rect.grid(row=1, column=0,ipadx=150, ipady=150,sticky="ew")
        
        self.circ = Button(self)
        self.circ["text"] = "Task 5\n(Circle)"
        self.circ["command"] = self.circle

        self.circ.grid(row=1, column=1,ipadx=150, ipady=150,sticky="ew")
        
        

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
        self.degrees = IntVar()
        # set it to some value
        self.degrees.set(0)
        # tell the entry widget to watch this variable
        self.x_cont["textvariable"] = self.degrees

        
        self.y_cont = Entry()
        self.y_cont.pack()
        self.y_cont.pack(ipadx=200)
        self.y_cont.pack(ipady=50)

        # here is the application variable
        self.secs = IntVar()
        # set it to some value
        self.secs.set(0)
        # tell the entry widget to watch this variable
        self.y_cont["textvariable"] = self.secs
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
class Task4_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.RUN = Button(self)
        self.RUN["text"] = "RUN\n\n\n\n\n\nEnter values for H, W \nand Y(Seconds) respectively"
        self.RUN["fg"]   = "red"
        
        self.RUN.pack({"side": "left"})
        self.RUN.pack(ipadx=200)
        self.RUN.pack(ipady=200)
        self.RUN["command"] =  self.run

        
        self.R1_cont = Entry()
        self.R1_cont.pack()
        self.R1_cont.pack(ipadx=200)
        self.R1_cont.pack(ipady=50)

        # here is the application variable
        self.X_var = StringVar()
        # set it to some value
        self.X_var.set(0)
        # tell the entry widget to watch this variable
        self.R1_cont["textvariable"] = self.X_var
        
        self.R2_cont = Entry()
        self.R2_cont.pack()
        self.R2_cont.pack(ipadx=200)
        self.R2_cont.pack(ipady=50)

        # here is the application variable
        self.Y_var = StringVar()
        # set it to some value
        self.Y_var.set(0)
        # tell the entry widget to watch this variable
        self.R2_cont["textvariable"] = self.Y_var
        
        self.sec_cont = Entry()
        self.sec_cont.pack()
        self.sec_cont.pack(ipadx=200)
        self.sec_cont.pack(ipady=50)

        # here is the application variable
        self.secs = StringVar()
        # set it to some value
        self.secs.set(0)
        # tell the entry widget to watch this variable
        self.sec_cont["textvariable"] = self.secs
        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    
class Task5_GUI(Frame):
    def run(self):
        self.quit()
    def createWidgets(self):
        self.RUN = Button(self)
        self.RUN["text"] = "RUN\n\n\n\n\n\nEnter values for R, \nand Y(Seconds) respectively"
        self.RUN["fg"]   = "red"
        
        self.RUN.pack({"side": "left"})
        self.RUN.pack(ipadx=200)
        self.RUN.pack(ipady=200)
        self.RUN["command"] =  self.run

        
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
        if(app.function == "Task2"):
            root = Tk()
            app = Forward_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Task2(app.x_var.get(), app.y_var.get())
        elif(app.function == "Task3"):
            root = Tk()
            app = Orientation_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Task3(app.degrees.get(), app.secs.get())
        elif(app.function == "Task4"):
            root = Tk()
            app = Task4_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Task4(float(app.X_var.get()),float(app.Y_var.get()),float(app.secs.get()))
        elif(app.function == "Task5"):
            root = Tk()
            app = Task5_GUI(master=root)
            app.mainloop()
            root.destroy()
            Lab1Tasks.Task5(float(app.R1_var.get()),float(app.Y_var.get()))
            
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
