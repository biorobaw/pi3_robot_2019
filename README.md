# pi3_robot_2019

This project implements ROS controllers for the lab's pi3_robot made in 2019
Currently there are 2 important branches:
    ros_controller (this branch), implements the controller for the robot
    java_client, which implements a java client to communicate with the robot.
    
# Controller capabilities

The controller uses ros to provide mechanisms to control the robot through messages and services.
Currently the following functionalities are provided:

    * Set speeds through a ros subscriber to Twist messages defining linear and angular speeds
    * Ability to load sub-modules via a custom ros service (RunFunction) including:
           * a camera sub-module
           * a distance sensor sub-module
    * Ability to send camera frames via a ros publisher of compressed images (format jpeg)
    * Ability to send distance sensor information via a ros publisher

# Installation

* If you received an SD card from the lab, the software should already be included in the SD card.
* If updating the software from an existing SD card, run the following commands in the terminal:
```
roscd pi3_robot_2019
git pull
cd ~/catkin_ws/
catkin_make
```

* To install the software on a different system, pull the repository in the source folder of your catkin workspace.
ROS needs to be already installed in your system, then proceed to build the ros package. Basic ros understandment is assumed.

# Usage
To use the controller you have to do the following:
  1. Set environment variables `ROS_IP` and `ROS_SERVER_URI` (http://wiki.ros.org/ROS/Tutorials/MultipleMachines)
        1. `ROS_IP` should be the ip of he robot
        2. `ROS_SERVER_URI` should be the URI of the node running ROS core (example: http://rpi2019:11311 )
  2. Run the following command:  `rosrun pi3_robot_2019 mainController.py`
  3. Run a client to control the robot, currently 


