#!/usr/bin/env python
# license removed for brevity
import rospy
import math
from geometry_msgs.msg import Twist
from std_msgs.msg import String
from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse
from robot_client.srv import GetSpeeds
from robot_client.srv import GetSpeedsRequest
from robot_client.srv import GetSpeedsResponse
from robot_client.srv import RunFunction
from robot_client.srv import RunFunctionRequest
from robot_client.srv import RunFunctionResponse
import SetSpeeds

from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension

from Tkinter import *
#====================================Creates Services====================
rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

rospy.wait_for_service('pi3_robot_2019/r1/get_speeds')
get_speeds = rospy.ServiceProxy('pi3_robot_2019/r1/get_speeds', GetSpeeds)

#============================Creates publisher to send speeds==============
rospy.init_node('speed_widget', anonymous=True)
pub = rospy.Publisher('pi3_robot_2019/r1/speed_vw', Twist, queue_size=1, latch = True)
rate = rospy.Rate(10) # 10hz
#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)



speedvw = Twist()

class Application(Frame):
    encod =  get_encoder().result
    base_l = encod[0]
    base_r = encod[1]
    lPrev = 0
    rPrev = 0
    global sense
    sense = (0.0, 0.0, 0.0) 
    def distance_sensors(msg):
        global sense
        sense = msg.data
        
    rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit
        
        self.QUIT.pack({"side": "left"})
        self.QUIT.pack(ipadx=100)
        self.QUIT.pack(ipady=100)
        
        #=====================ENCODER WIDGET==================
        self.encoder = Button(self)
        self.set_encoder()

        self.encoder.pack({"side": "left"})
        self.encoder.pack(ipadx=100)
        self.encoder.pack(ipady=100)
        
        self.sensors = Button(self)
        self.set_sensor()
        self.sensors["command"] = self.reset

        self.sensors.pack({"side": "top"})
        self.sensors.pack(ipadx=100)
        self.sensors.pack(ipady=100)
        
        
        #========================SPEED WIDGET=========================
        #Right wheel speed entry
        self.r_cont = Entry()
        self.r_cont.pack()
        self.r_cont.pack({"side": "right"})
        self.r_cont.pack(ipadx=30)
        self.r_cont.pack(ipady=25)
        #Left wheel speed entry
        self.l_cont = Entry()
        self.l_cont.pack()
        self.l_cont.pack({"side": "right"})
        self.l_cont.pack(ipadx=30)
        self.l_cont.pack(ipady=25)
        # here is the application variable
        self.r_var = StringVar()
        # set it to some value
        self.r_var.set("Right Wheel")
        # tell the entry widget to watch this variable
        self.r_cont["textvariable"] = self.r_var
        
        self.l_var = StringVar()
        self.l_var.set("Left Wheel")
        self.l_cont["textvariable"] = self.l_var
        
        self.stop = Button(self)
        self.stop["fg"]   = "red"
        self.stop["text"] = "Press to stop"
        self.stop["command"] = self.stop_serv
        self.stop.pack({"side": "right"})
        self.stop.pack(ipadx=100)
        
        
        self.speed_widget = Button(self)
        self.speed_widget["text"] = "Enter speeds and press to run"
        self.speed_widget["command"] = self.set_speed
        self.speed_widget.pack({"side": "right"})
        self.speed_widget.pack(ipadx=100)
        
        self.turnL_but = Button(self)
        self.turnL_but["text"] = "Press to\nturn left\n90Degrees"
        self.turnL_but["command"] = self.turnL
        self.turnL_but.pack({"side": "top"})
        self.turnL_but.pack(ipadx=50)
        
        self.turnR_but = Button(self)
        self.turnR_but["text"] = "Press to\nturn Right\n90Degrees"
        self.turnR_but["command"] = self.turnR
        self.turnR_but.pack({"side": "top"})
        self.turnR_but.pack(ipadx=50)
        #========================END SPEED NODE=========================
        
    def turnR(self):
        Turn(90)
    def turnL(self):
        Turn(-90) 
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
    def reset(self):
        encod =  get_encoder().result
        self.base_l = encod[0]
        self.base_r = encod[1]
    def set_encoder(self):
        TIME = rospy.get_time()
        speeds = get_speeds().result
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        l = l-self.base_l
        r = r-self.base_r
        lVel = speeds[0]*circumference/32
        rVel = speeds[1]*circumference/32
        if lVel<.2:
            lVel = 0
        if rVel<.2:
            rVel = 0

        
        str_var = "Inches Traveled\n"
        str_var += "Left Encoder: "+ str(l*circumference/32) +" \nRight Encoder: " +str(r*circumference/32)+"\nVl(IPS):"
        str_var += "\n"+ str('{:g}'.format(float('{:.{p}g}'.format(lVel, p=3))))+"\nVr(IPS):\n"+str('{:g}'.format(float('{:.{p}g}'.format(rVel, p=3))))
        self.encoder["text"] = str_var
        self.lPrev = l
        self.rPrev = r
        self.after(500, self.set_encoder)
    def set_sensor(self):
        str_var = "Left Sensor: "+ str(sense[0]*39.3701) +" \nFront Sensor: " +str(sense[1]*39.3701) + "\nRight Sensor: "+str(sense[2]*39.3701)
        self.sensors["text"] = str_var
        self.after(500, self.set_sensor)  
    def set_speed(self):
        l=float(self.l_var.get())
        r=float(self.r_var.get())
        
        
        speedvw.linear.x= (l+r)/2
        speedvw.angular.z=(r-l)/width
        pub.publish(speedvw)
    def stop_serv(self):
        speedvw.linear.x=0
        speedvw.angular.z=0
        pub.publish(speedvw)
      
      
      
      
def Turn(Degrees): 
    rate = rospy.Rate(10) 
    c = 2*math.pi*(width/2) * (abs(Degrees)*1.00/360)*(32/8.0110612) 
    encod =  get_encoder().result                              #times how many inches per tick
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    maxSpeed=3
    while (r-rInit<c or l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        satSpeed = c - ((r-rInit)*(circumference/32))
        satSpeed = satSpeed*.25
        if satSpeed>maxSpeed:
            satSpeed=maxSpeed
        if(Degrees>0):
            SetSpeeds.setspeeds(satSpeed,-1*satSpeed)
        else:
            SetSpeeds.setspeeds(-1*satSpeed,satSpeed)
        rate.sleep()
    SetSpeeds.setspeeds(0,0)  
      
def on_shutdown():
    rospy.loginfo("Shutting down")
    speedvw.linear.x=0
    speedvw.angular.z=0
    pub.publish(speedvw)
    rospy.loginfo(speedvw)
    rate.sleep()


if __name__ == '__main__':
    try:
        rospy.on_shutdown(on_shutdown)
        root = Tk()
        app = Application(master=root)
        app.mainloop()
        root.destroy()
    except Exception as e:
        rospy.loginfo(e)
        on_shutdown()
        


