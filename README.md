# pi3_robot_2019
This project contains a ROS client for the lab's robot "Pi3Robot2019"
There are lab files which are used in the Control of Mobile Robots course, with python files containing the functions for setting the robots speeds, reading from the encoders and sensors, as well as recieving images from the robots camera.
The lab programs only require the full installation of ROS 


In the launch folder there are the launch files for launching ORB_SLAM2 configured for the robot's camera which can be used along side the pi3_slam_nav.py file for running a bug algorithm using the pose recieved from ORB_SLAM2
In order to use the programs related to ORB_SLAM2, you must install ORB_SLAM2: https://github.com/appliedAI-Initiative/orb_slam_2_roshttps://github.com/appliedAI-Initiative/orb_slam_2_ros

See the docs folder for detailed installation and run instructions
