#!/usr/bin/env pybricks-micropython
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.parameters import Port
from pybricks.robotics import DriveBase

from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule
from line_follower import LineFollower
from time import sleep
from pringler import Pringler

# from pybricks.robotics import GyroDriveBase

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

# rgb-color values
WHITE = (23, 52, 39)
BROWN = (1, 7, 0)
BLUE = (2, 17, 17)
RED = (6, 4, 0)

drive_base.settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)

color_sensor = ColorSensor(Port.S2)                     # used for band detection
ultrasonic_sensor = UltrasonicSensor(Port.S4)           # used for obstacle detection
gyro_sensor  = GyroSensor(Port.S1)                      # used for navigation via drive_base
touch_sensor = TouchSensor(Port.S3)                   # used for wall alignment?

precision_module = PrecisionModule(
    left_motor,
    right_motor,
    drive_base,
    straight_speed,
    straight_acceleration,
    turn_rate,
    turn_acceleration,
    gyro_sensor)


# precision_module.straight_gyro(2000)
# sleep(5)
# precision_module.turn_gyro(360)
# sleep(5)
# precision_module.turn_gyro(-360)
# sleep(5)
# precision_module.straight_gyro(-2000)

# bridge = Bridge(precision_module, touche_sensor, color_sensor)

# bridge.run()



# TODO
#   - precision_module testen
#   - menu einbinden
#   - neu kalibrieren (gewicht verschieben?)
#   - greifarm aktuieren
#   - brücke
#   - linien folgen
#   - farbfinden
#   - pringler
#

# TODO Cornelius
#   -
#   -
