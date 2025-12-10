#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick

from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Direction
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
# from pybricks.robotics import GyroDriveBase
from time import sleep

from precision_module import PrecisionModule
from line_follower import LineFollower
from bridge import Bridge
from time import sleep
from pringler import Pringler

from precision_module import PrecisionModule

# ---------------------- Hardware setup ----------------------
ev3 = EV3Brick()

left_motor  = Motor(Port.B)   # adjust to your wiring
right_motor = Motor(Port.C)
motor = Motor(Port.D)
wheel_diameter = 33
axle_track = 160
drive_base = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

straight_speed = 100
straight_acceleration = 100
turn_rate = 120
turn_acceleration = 120

drive_base.settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)

color_sensor = ColorSensor(Port.S2)                     # used for band detection
ultrasonic_sensor = UltrasonicSensor(Port.S4)           # used for obstacle detection
"""gyro_sensor  = GyroSensor(Port.S1)                      # used for navigation via drive_base
touche_sensor = TouchSensor(Port.S3)  """                 # used for wall alignment?


pringler = Pringler(drive_base, motor, color_sensor, ultrasonic_sensor)
pringler.run()

# TODO
#   - refactoring
#   - utils class
#   - menu einbinden
#   - kalibrieren (gewicht verschieben?)
#   - brücke
#   - linien folgen
#   - farbfinden
#
#


                    