# pi3_robot_2019

This project implements ROS controllers for the lab's pi3_robot used since 2019
Currently there are 2 important branches:
    ros_controller (this branch), implements the controller for the robot
    java_client, which implements a java client to communicate with the robot.
    
# Controller capabilities

The controller uses ros to communicate and control the robot through messages and services.
Currently, only set speeds commands are supported and no feedback is implemented.
Other commands are under development

# Installation

* If you received an SD card from the lab, the software should already be included in the SD card.
* If updating the software from an existing SD card, run the following commands in the terminal:
```
cd ~/catkin_ws/src/pi3_robot_2019
git pull
cd ~/catkin_ws/
catkin_make
```
You might need to update the robot drivers which are stored under a private repository, 
either create your own or ask for access to the current lab mantainer.

* To install the software on a different system, pull the repository in the source folder of your catkin workspace.
ROS needs to be already installed in your system, then proceed to build the ros package. Basic ros understandment is assumed.

# Usage
To use the controller you have to do the following:
  1. Set environment variables `ROS_IP` and `ROS_SERVER_URI` (http://wiki.ros.org/ROS/Tutorials/MultipleMachines)
  2. Run the following command:  `rosrun pi3_robot_2019 motionController.py`
  3. Run a client to control the robot, currently 


