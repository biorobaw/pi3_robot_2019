#!/usr/bin/env python
# license removed for brevity

from Tkinter import *





class Application(Frame):
    maze = [[0, 1, 0, 0, 1, -1], [0, 1, 0, 0, 0, -1], [0, 1, 0, 0, 0,-1],[0, 1, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 0, 1, -1], [0, 0, 0, 0, 0, -1], [0, 0, 0, 0, 0, -1],[0, 0, 1, 0, 0, -1],
            [0, 0, 0, 1, 1, -1], [0, 0, 0, 1, 0, -1], [0, 0, 0, 1, 0, -1],[0, 0, 1, 1, 0, -1]]
    mazeGrid = [None]*16
    file = [None]*16
    curcell =-1
    prevcell=-1
    dir = 'N'

    def createWidgets(self):     
        self.startGrid()
        
    def updateGrid(self):
        pngName = str(self.maze[self.curcell][1]) + str(self.maze[self.curcell][2]) +str(self.maze[self.curcell][3]) +str(self.maze[self.curcell][4])
        pngName += self.dir
        pngName+=".png"
        self.file[self.curcell] = PhotoImage(file="src/robot_client/scripts/grid_images/"+pngName)
        self.mazeGrid[self.curcell] = Label(self, text = self.curcell+1, compound=CENTER, image=self.file[self.curcell])
        self.mazeGrid[self.curcell].grid(row=self.curcell/4, column=self.curcell%4)
        
        if(self.prevcell!=-1 and self.prevcell!=self.curcell):
            pngName = str(self.maze[self.prevcell][1]) + str(self.maze[self.prevcell][2]) +str(self.maze[self.prevcell][3]) +str(self.maze[self.prevcell][4])
            pngName+=".png"
            self.file[self.prevcell] = PhotoImage(file="src/robot_client/scripts/grid_images/"+pngName)
            self.mazeGrid[self.prevcell] = Label(self, text = self.prevcell+1, compound=CENTER, image=self.file[self.prevcell])
            self.mazeGrid[self.prevcell].grid(row=self.prevcell/4, column=self.prevcell%4)
            
        
        self.prevcell=self.curcell
        
    def startGrid(self):
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



