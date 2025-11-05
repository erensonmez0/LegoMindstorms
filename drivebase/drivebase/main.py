#!/usr/bin/env pybricks-micropython
# ...existing code...
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port, Direction
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase

left_motor = Motor(Port.C)
right_motor = Motor(Port.B)
ev3 = EV3Brick()
wheel_diameter = 36  
axle_track = 110     
drive_base = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

drive_base.straight(500)
drive_base.turn(180)
drive_base.straight(500)
drive_base.turn(-180)