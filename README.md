# Pi3Robot2019

The project implements a ROS controller for the lab's robot.
It consists of 3 pieces of software:
  1. A rosnode in java implementing the client
  2. A rosnode in python implementing the server
  3. Robot drivers (not included in the repository)

# Current functionality
 
 Currently, only set speeds commands are supported and no feedback is implemented.

# TODO

 Implement publisher in the robot to post sensor data (camera, distance sensors, battery, etc).
 Implement listener in client to read the data.
 Implement services in the robot to get feedback (command received, command completed, etc)

# Prerequisites

 The project assumes ROS is already installed in the robot, as well
 as the dependencies to use the hardware of the lab's Pi3Robot2019, 
 and basic ROS knowledge.

# Installation (needs verification):

 1. Copy the folder catkin_ws from the repository to the robot's home diretory (~/)
 2. cd into the the copied folder (~/catkin_ws) and run the command: catkin_make (see how to use catkin workspaces in ROS tutorials)
 3. Request the robot drivers to the lab mantainer, and copy them in the robot's folder (~/drivers)
 4. Use maven to include the java client to your code. 
    To do so, add the following lines to your pom file (replace for an adequate version number):
     ```
     <repositories>
      <repository>
          <id>jitpack.io</id>
          <url>https://jitpack.io</url>
      </repository>
    </repositories>
    
    <dependencies>
  	  <dependency>
        <groupId>com.github.biorobaw</groupId>
        <artifactId>Pi3Robot2019</artifactId>
        <version>VERSION_NUMBER</version>
      </dependency>
    </dependencies>
    ```
    
  # Usage (needs revision)
  
  1. Start roscore
  2. In PC:
      1. In your code, create an instance of Pi3Robot providing the ip and port of ros master, as well as the id of the robot. Sample usage code is provided in the main function of class `Pi3Robot.java`.
      2. Run your code, make sure to wait for the robot to be up before sending commands to the robot. Currently there is a bug which requires the pc ros node to start before the robot.    
  3. In the robot:
      1. set environment variables `ROS_IP` and `ROS_SERVER_URI` (http://wiki.ros.org/ROS/Tutorials/MultipleMachines)
      2. run the following command:  `rosrun pi3_robot_2019 motionController.py`
  
  
  
