#!/usr/bin/env python

import sys
import os
sys.path.append(os.path.abspath("/home/pi/catkin_ws/src/pi3_robot_2019/drivers"))
import MySensors
MySensors.initSensors()
MySensors.exitSensors()
