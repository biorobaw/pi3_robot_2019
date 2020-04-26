#!/usr/bin/env python
# license removed for brevity
import rospy
import time
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String


from std_msgs.msg import Int8MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension



from Tkinter import *




#============================Create subscriber to recieve grid info==============
#rospy.init_node('lab4_grid', anonymous=True)

#rate = rospy.Rate(10) # 10hz


def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)




class Application(Frame):
    maze = [[0, 1, 0, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]
    mazeGrid = [None]*16
    file = [None]*16
    curcell =4
    dir = 'N'

    def createWidgets(self):     
        self.updateGrid()
        
    def updateGrid(self):
        for i in range(16):
            pngName = str(self.maze[i][1]) + str(self.maze[i][2]) +str(self.maze[i][3]) +str(self.maze[i][4])
            
            if(self.curcell ==i):
                pngName += self.dir
            if(self.maze[i][0]==0): #If cell is unvisited display the question mark tile instead. Feel 
                pngName="0"         #free to comment this out instead.
                
            pngName+=".png"
            #print(pngName)
            self.file[i] = PhotoImage(file="src/robot_client/scripts/grid_images/"+pngName)
            self.mazeGrid[i] = Label(self, text = i+1, compound=CENTER, image=self.file[i])
            self.mazeGrid[i].grid(row=i/4, column=i%4)
                

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



