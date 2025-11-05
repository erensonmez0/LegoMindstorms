from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from time import sleep

class LineFollower:
    def __init__(self, drive_base:DriveBase, line_sensor:ColorSensor, drive_speed:int, black:int, white:int, blue:int):
        self.drive_base = drive_base
        self.drive_speed = drive_speed
        self.black = black
        self.white = white
        self.blue = blue
        self.line_sensor = line_sensor
        self.threshold = (black+white)/2
        self.proportional_gain = 1.2

    # Set the gain of the proportional line controller. This means that for every
    # percentage point of light deviating from the threshold, we set the turn
    # rate of the drivebase to 1.2 degrees per second.

    # For example, if the light value deviates from the threshold by 10, the robot
    # steers at 10*1.2 = 12 degrees per second.




   
    def run(self):
        # Start following the line endlessly.
        while self.line_sensor.reflection()!=self.blue:
            # Calculate the deviation from the threshold.
            deviation = self.threshold - self.line_sensor.reflection()

            # Calculate the turn rate.
            turn_rate = self.proportional_gain * deviation

            # Set the drive base speed and turn rate.
            self.drive_base.drive(self.drive_speed, turn_rate)

            # You can wait for a short time or do other things in this loop.
            sleep(0.2)
    
    def avoid_obstacle(self):
        self.drive_base.drive(10,60)
        self.drive_base.drive(10,-60)


