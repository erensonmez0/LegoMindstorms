#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port, Direction
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from time import sleep
from line_follower import LineFollower
from bridge import Bridge
from time import sleep

# ---------------------- Hardware setup ----------------------
ev3 = EV3Brick()
left_motor  = Motor(Port.B)   # adjust to your wiring
right_motor = Motor(Port.C)
motor = Motor(Port.D)
wheel_diameter = 33.25
axle_track = 160
drive_base = DriveBase(left_motor, right_motor, wheel_diameter=33.25, axle_track=160)
drive_base.settings(200, 200, 120, 120)

color_sensor = ColorSensor(Port.S2)        # used for band detection
#ultra = UltrasonicSensor(Port.S2)   # optional
gyro_sensor  = GyroSensor(Port.S1)    


motor.run(300)
sleep(1.5)
drive_base.straight(200)
drive_base.straight(-200)
motor.run(-300)
sleep(1.8)



"""Bridge(drive_base).run()   """  # optional


"""line_follower = LineFollower(drive_base=drive_base, color_sensor= color_sensor)
line_follower.run()"""

                    