# pi3_robot_2019

This project implements ROS controllers for the lab's pi3_robot made in 2019
Currently there are 2 important branches:
    ros_controller (this branch), implements the controller for the robot
    java_client, which implements a java client to communicate with the robot.
    
# Java Client capabilities

The java client provides a java API to use the functionalities offered by the ros controller. 
Currently the following functionalities are provided:

    * Set speeds through a ros publisher of Twist messages defining linear and angular speeds
    * Ability to load sub-modules via a custom ros service (RunFunction) including:
           * a camera sub-module
           * a distance sensor sub-module
    * Ability to read camera frames via a ros subscriber of compressed images and transform them into opencv mat objects.
    * Ability to read distance sensor information via a ros subscriber.

# JAVA API Installation

Use maven to include the java client in your code. 
    To do so, add the following lines to your pom file ( replace for an adequate version number ):
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
        <artifactId>pi3_robot_2019</artifactId>
        <version>java-client-1.0.0</version> 
    </dependency>
</dependencies>
```
Alternatively, download and compile the code.

# Usage

To see how to use the API, read the example main function in `Pi3Robot2019.java`


# Pi3Robot2019JavaClient

The project implements a ROS controller for the lab's robot.
It consists of 3 pieces of software:
  1. A rosnode in java implementing the client
  2. A rosnode in python implementing the server
  3. Robot drivers (not included in the repository)

# Current functionality
 
 Currently, only set speeds commands are supported and no feedback is implemented. 
 Note that basic ROS usage knowledge is expected.
 
# Notes for future developers

  If you need to add more custom ros services, you will first have to modifiy branch `ros_controller` adding the `.srv` files.
  Then, in a machine with rosjava installer, run the script `export_java.sh`, you will be prompted to enter a version number.
  See https://semver.org/ for choosing an adequate version number. Commit and push the changes.
  Finally, in this branch, update the pom file and use your new service.
  


  
  
