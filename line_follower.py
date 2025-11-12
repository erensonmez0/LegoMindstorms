#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from time import sleep

class LineFollower:
    BLACK = 9
    WHITE = 85
    BLUE = 15
    THRESHOLD = (BLACK+WHITE)/2
    PROPORTIONAL_GAIN = 1.2
    DRIVE_SPEED = 100
    
    

    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor

   
    def run(self):
        # Start following the line endlessly.
        while self.color_sensor.reflection()!=self.BLUE:

            
            # Calculate the deviation from the threshold.
            deviation = self.THRESHOLD - self.color_sensor.reflection()

            # Calculate the turn rate.
            turn_rate = self.PROPORTIONAL_GAIN* deviation

            # Set the drive base speed and turn rate.
            self.drive_base.drive(self.DRIVE_SPEED, turn_rate=int(turn_rate))

            # You can wait for a short time or do other things in this loop.
            #avoid obstacle
            if self.ultrasonic_sensor.distance() <= 30:
                self.avoid_obstacle() 
    
    def avoid_obstacle(self):
        self.drive_base.drive(10,60)
        self.drive_base.drive(10,-60)


