#!/usr/bin/env python
# license removed for brevity
import rospy
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String


from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension



from Tkinter import *

maze = [[0, 1, 0, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]


#============================Create subscriber to recieve grid info==============
rospy.init_node('lab4_grid', anonymous=True)

rate = rospy.Rate(10) # 10hz


def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)




class Application(Frame):
    mazeGrid = [None]*16
    file = [None]*16
    curcell =4
    dir = 'N'

    def createWidgets(self):
        #self.QUIT = Button(self)
        #self.QUIT["text"] = "QUIT"
        #self.QUIT["fg"]   = "red"
        #self.QUIT["command"] =  self.quit
        #self.QUIT.pack({"side": "left"})
        #self.QUIT.pack(ipadx=100)
        #self.QUIT.pack(ipady=100)
        
        #root.grid_columnconfigure(0, minsize=100)
        
        self.updateGrid()
        
    def updateGrid(self):
        for i in range(16):
            pngName = str(maze[i][1]) + str(maze[i][2]) +str(maze[i][3]) +str(maze[i][4])
            
            if(self.curcell ==i):
                pngName += self.dir
            pngName+=".png"
            print(pngName)
            self.file[i] = PhotoImage(file="src/robot_client/scripts/grid_images/"+pngName)
            self.mazeGrid[i] = Label(self, text = i+1, compound=CENTER, image=self.file[i])
            self.mazeGrid[i].grid(row=i/4, column=i%4)
                
            #else:
            #    self.mazeGrid[i] = Label(self, text = i+1, compound=CENTER, image=self.g0000)
            #    self.mazeGrid[i].grid(row=i/4, column=i%4)            
        #self.mazeGrid[0] = Label(self, text = "BLAHBLAH", compound=CENTER, image=self.gridoption1)
        #self.mazeGrid[0].grid(row=0, column=0)
        
        


        

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

      
      
      
      
      
      



if __name__ == '__main__':
    try:


        root = Tk()
        app = Application(master=root)
        app.mainloop()
        
        root.destroy()
        #app.mainloop()
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
        pass
    except Exception as e:
        #on_shutdown()
        rospy.loginfo("InteruptException")
        pass


