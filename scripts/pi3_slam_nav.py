#!/usr/bin/env python
# license removed for brevity

#This is a simple bug algorithm to demonstrate the user of using ORB_SLAM2 for localization. 
#You will need to have raspicam running on the robot, and launch the pi3_orb_slam2.launch file on this device
#Rviz is used for the visualization
import rospy
from Tkinter import * #For GUI
import math
from geometry_msgs.msg import PoseStamped #getting pose from ORB_SLAM2
from tf.transformations import euler_from_quaternion #for calculation theta
from threading import Thread
from std_msgs.msg import Float32MultiArray
from std_msgs.msg import MultiArrayLayout
from std_msgs.msg import MultiArrayDimension
from robot_client.srv import GetEncoder
from robot_client.srv import GetEncoderRequest
from robot_client.srv import GetEncoderResponse


import SetSpeeds

rospy.init_node('pi3_slam_nav', anonymous=True)
rate = rospy.Rate(10) # 10hz

rospy.wait_for_service('pi3_robot_2019/r1/get_encoder')
get_encoder = rospy.ServiceProxy('pi3_robot_2019/r1/get_encoder', GetEncoder)

#=================Robot Dimensions==================================
diameter = 2.55
width = 4.2
sensorwidth = 3
circumference = 2*math.pi*(diameter/2) #circumference for 2.55 is 8.0110612

thread = False
maxspeed = 4
turningspeed= 1
timeLimit = 2
k=.5
x = 0
y = 0
th = 0
prevTime =0
dTime=0
sense = (0.0, 0.0, 0.0) 
def distance_sensors(msg):
    global sense
    sense = msg.data
rospy.Subscriber("/pi3_robot_2019/r1/distance_sensors/d_data",
                         Float32MultiArray, distance_sensors)

#This function updates the pose everytime a new PointStamped2 message is recieved from the ORB_SLAM2 node
def pose_fun(msg):
	global x
	global y
	global th
	global prevTime
	global dTime
	#print(msg.pose.position)
	x = msg.pose.position.x
	y = msg.pose.position.y
	quaternion = (msg.pose.orientation.x, msg.pose.orientation.y, msg.pose.orientation.z, msg.pose.orientation.w)
        euler = euler_from_quaternion(quaternion)
	#roll = euler[0]
	#pitch = euler[1]
	yaw = euler[2]
    
    	th = yaw;
	timeNow= rospy.get_time()
	#dTime = timeNow-prevTime
	prevTime = timeNow
	
	#print(th)

	
	
rospy.Subscriber("/orb_slam2_mono/pose",
                         PoseStamped, pose_fun)





    
def on_shutdown(): #Called when shutting down
    global thread
    thread = False
    rospy.loginfo("Shutting down")
    SetSpeeds.setspeeds(0,0) #Stop Robot
    rate.sleep()


def moveCoord(xC, yC):#function for navigating to coordinate
        print(xC)
	print(yC)
	global thread
	stop = False
	while thread:
		yaw = math.atan2(yC-y, xC-x);
		print(yaw)
		
		dx = xC-x
		dy = yC-y
		distance = (dx*dx) + (dy*dy)
		print("Distance: " +str(distance))
		dth = yaw-th #Find the difference between the current theta, and the desired theta to be facing the coordinate.
		l = sense[0]*39.3701
        	f = sense[1]*39.3701
        	r = sense[2]*39.3701 

		if(stop ==False and (rospy.get_time() -prevTime)>timeLimit):
			stop=True
			SetSpeeds.setspeeds(0,0)
			rate.sleep()
			continue
		else:
			if((rospy.get_time() -prevTime)>1):
				rate.sleep()
				continue
			else:
				stop=False
			

			
		if(abs((dth))>.1): #If the robot has delta theta greater than .1, turn in place.
			print("Delta theta: "+str(dth))
			if(dth>.5):
				k=1
			else:
				k=.75
			if(dth>0): #robot needs to turn left
				SetSpeeds.setspeeds(-turningspeed*k,turningspeed*k)
				print("Turning left")
			else: #robot needs to turn right
				SetSpeeds.setspeeds(turningspeed*k,-turningspeed*k)
				print("Turning right")
			
		elif(f<8): #If the robot runs into an obstacle, start wall following
			Turn(-90)
			wallFollow()
		
		elif(abs(distance) >.01): #move towards the goal
			print("going straight")
			SetSpeeds.setspeeds(maxspeed,maxspeed)
		else: #if the robot has reached the goal, finish
			print("Reached the coordinate: (" +str(xC)+", "+str(yC)+")")
			SetSpeeds.setspeeds(0,0)
			thread = False
			return
		
		rate.sleep()
	
				
    
#==========================GUI STUFF================
class Application(Frame):

    def createWidgets(self):


        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT    \n"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.grid(row=0, column=0,ipadx=150, ipady=150, sticky="ew")

	self.Pose = Button(self)

	self.set_Pose()
        self.Pose.grid(row=0, column=1,ipadx=150, ipady=150, sticky="ew")
        self.Pose["command"] =  self.move

	#X coord entry
        self.x_cont = Entry(self)
        self.x_cont.grid(row=1, column=0,ipadx=100, ipady=50, sticky="ew")
        #Y coord entry
        self.y_cont = Entry(self)

        self.y_cont.grid(row=1, column=1,ipadx=100, ipady=50, sticky="ew")
        # here is the application variable
        self.x_var = StringVar()
        # set it to some value
        self.x_var.set("X coordinate")
        # tell the entry widget to watch this variable
        self.x_cont["textvariable"] = self.x_var
        
        self.y_var = StringVar()
        self.y_var.set("Y coordinate")
        self.y_cont["textvariable"] = self.y_var

   
    def quit(self):
	self.master.destroy()
	on_shutdown()        
    def set_Pose(self):
	textTemp = "Your Pose\nX: " +str(x)+"\nY: " + str(y) +"\nTh: "+str(th) 
	if(thread ==False):
		textTemp+="\nPress to move to coordinates entered" #+ str(dTime)
	else:
		textTemp+= "\nMoving to: ("+self.x_var.get()+", " + self.y_var.get()+")"
	if((rospy.get_time() -prevTime)>timeLimit):
		textTemp+= "\nRobot is lost, please move the robot until\nit localizes"
	self.Pose["text"] = textTemp
	self.after(500, self.set_Pose)

    def move(self):
	global thread	
	if (thread == True):
		print("Already running")
		return	

	thread = True
	moveCoordThread = Thread(target = moveCoord, args = (float(self.x_var.get()), float(self.y_var.get()), ))
	moveCoordThread.start()
	return

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

def Turn(Degrees): 
    print("here")
    #linSpeed = X/Y
    rate = rospy.Rate(10)
    if(Degrees >0):
        SetSpeeds.setspeeds(3,-3)
    else:
        SetSpeeds.setspeeds(-3,3)
    
    c = 2*math.pi*(width/2) * (abs(Degrees)*1.00/360)*(32/circumference) #circumference of circle times how many rotations
    encod =  get_encoder().result                              #times how many inches per tick
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    
    TIME = rospy.get_time()
    while (r-rInit<c and l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]
        rate.sleep()
    SetSpeeds.setspeeds(0,0)

def wallFollow(): 
	while not rospy.is_shutdown():
		l = sense[0]*39.3701
        	f = sense[1]*39.3701
        	r = sense[2]*39.3701
		print("left: " +str(l) +" front: " +str(f) + "right: " +str(r))
        	fronterror = (f-8)*k
        	
		if(l >10 and r>10):
			forward(6,2) #Used for clearing wall
			SetSpeeds.setspeeds(0,0)
			return
		
		if(fronterror>maxspeed):
       		      fronterror = maxspeed
        
        	if(l<r):
            		wallerror = (l-8)*k
            		if(wallerror>0):
                  		SetSpeeds.setspeeds(fronterror-wallerror,fronterror)
            		else:
                		SetSpeeds.setspeeds(fronterror,fronterror+wallerror)
        	else:
            		wallerror = (r-8)*k
           		if(wallerror>0):
                   		SetSpeeds.setspeeds(fronterror,fronterror-wallerror)
            		else:
               			SetSpeeds.setspeeds(fronterror+wallerror,fronterror)
        	if(f<=8 or fronterror<.5):
            		SetSpeeds.setspeeds(0,0)
            		if(l<r):
                		Turn(90)
				return
            		else:
                		Turn(-90)
				return
            
        
        	rate.sleep()
def forward(X, Y): #Just used for clearing walls.
    linSpeed = X/Y
    SetSpeeds.setspeeds(linSpeed,linSpeed)
    c = abs(X*32/circumference) #Converting inches to ticks
    encod =  get_encoder().result
    lInit = encod[0] # GET INITIAL ENCODER VALUES
    rInit = encod[1]
    l=0
    r=0
    while (r-rInit<c and l-lInit<c):
        encod =  get_encoder().result
        l = encod[0]
        r = encod[1]

    SetSpeeds.setspeeds(0,0)

		
if __name__ == '__main__':
    try:
        rospy.on_shutdown(on_shutdown)
        root = Tk()
        app = Application(master=root)
	
	while not rospy.is_shutdown():
		app.update_idletasks()
            	app.update()
		rate.sleep()
	app.destroy()
        
            
        
    except rospy.ROSInterruptException:
        rospy.loginfo("InteruptException")
        on_shutdown()
    except Exception as e:
        on_shutdown()
        #pass
