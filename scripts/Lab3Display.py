#!/usr/bin/env python
# license removed for brevity
import rospy

import math
from std_msgs.msg import String

from Tkinter import *


def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)

class Application(Frame):
    R1=0
    R2=0
    R3=0
    loc =[0,0]

    def createWidgets(self):     
        self.updateDisplay()
        
    def updateDisplay(self):
        strSet = "R1: "+str(self.R1)+"\nR2: "+str(self.R2)+"\nR3: "+str(self.R3)+"\nYour location: " +str(self.loc)
        self.display = Label(self, text =strSet , compound=CENTER)

        self.display.grid(row=0)
        self.display.grid(ipadx=150, ipady=150)
                

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        
class Entry_GUI(Frame):
    Num = 3
    minH = [None]*Num
    minS = [None]*Num
    minV = [None]*Num
    
    maxH = [None]*Num
    maxS = [None]*Num
    maxV = [None]*Num
    label =[None]*(Num*3)
    entries = [None]*(Num*3*2)
    
    def run(self):
        self.quit()
    def createWidgets(self):     
        
        self.Run=Button(self)
        self.Run["text"] = "Run"      
        self.Run.grid(row=0, column=3,ipadx=100, ipady=25,sticky="ew")
        self.Run["command"] = self.run
        
        
        for i in range(self.Num):
            self.label[i*3] = Label(self)
            self.label[i*3]["text"] = "Enter H values for mask #" +str(i+1) +"(0-180)"      
            self.label[i*3].grid(row=(i*3), column=0,ipadx=100, ipady=25,sticky="ew")
        
        
            self.minH[i] = IntVar()
            self.minH[i].set(0)
            self.entries[i*6] = Entry(self)
            self.entries[i*6].grid(row=(i*3), column=1,ipadx=100, ipady=25,sticky="ew")
            self.entries[i*6]["textvariable"] = self.minH[i]
        
            self.maxH[i] = IntVar()
            self.maxH[i].set(180)
            self.entries[(i*6)+1] = Entry(self)
            self.entries[(i*6)+1].grid(row=(i*3), column=2,ipadx=100, ipady=25,sticky="ew")
            self.entries[(i*6)+1]["textvariable"] = self.maxH[i]
        
        
            self.label[(i*3)+1] = Label(self)
            self.label[(i*3)+1]["text"] = "Enter S values for mask #" +str(i+1) +"(0-180)"      
            self.label[(i*3)+1].grid(row=(i*3)+1, column=0,ipadx=100, ipady=25,sticky="ew")

        
            self.minS[i] = IntVar()
            self.minS[i].set(0)
            self.entries[(i*6)+2] = Entry(self)
            self.entries[(i*6)+2].grid(row=(i*3)+1, column=1,ipadx=100, ipady=25,sticky="ew")
            self.entries[(i*6)+2]["textvariable"] = self.minS[i]
            
            self.maxS[i] = IntVar()
            self.maxS[i].set(255)
            self.entries[(i*6)+3] = Entry(self)
            self.entries[(i*6)+3].grid(row=(i*3)+1, column=2,ipadx=100, ipady=25,sticky="ew")
            self.entries[(i*6)+3]["textvariable"] = self.maxS[i]
        
            self.label[(i*3)+2] = Label(self)
            self.label[(i*3)+2]["text"] = "Enter V values for mask #" +str(i+1) +"(0-180)"      
            self.label[(i*3)+2].grid(row=(i*3)+2, column=0,ipadx=100, ipady=25,sticky="ew")

        
            self.minV[i] = IntVar()
            self.minV[i].set(0)
            self.entries[(i*6)+4] = Entry(self)
            self.entries[(i*6)+4].grid(row=(i*3)+2, column=1,ipadx=100, ipady=25,sticky="ew")
            self.entries[(i*6)+4]["textvariable"] = self.minV[i]
        
            self.maxV[i] = IntVar()
            self.maxV[i].set(255)
            self.entries[(i*6)+5] = Entry(self)
            self.entries[(i*6)+5].grid(row=(i*3)+2, column=2,ipadx=100, ipady=25,sticky="ew")
            self.entries[(i*6)+5]["textvariable"] = self.maxV[i]
        
        
        

        
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()



