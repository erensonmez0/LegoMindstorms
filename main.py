from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor
from pybricks.parameters import Port, Direction
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from time import sleep
from line_follower import LineFollower

left_motor = Motor(Port.C, Direction.COUNTERCLOCKWISE)
right_motor = Motor(Port.B)
gyro_sensor = GyroSensor(Port.S1)
line_sensor = ColorSensor(Port.S2)
ev3 = EV3Brick()
wheel_diameter = 36   #Wheel Diameter
axle_track = 120     #distance between wheels
steering = 60 #turn speed in °/s
overshoot = 5 

drive_base = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)
line_follower = LineFollower(drive_base=drive_base, line_sensor=line_sensor, drive_speed=10, black=9, white=85, blue=60)
line_follower.avoid_obstacle()
drive_base.straight(500)
drive_base.turn(180)
drive_base.straight(500)
drive_base.turn(-180)



