#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from precision_module import PrecisionModule
from config import BLUE_LINE_FOLLOW
from mindstorm_util import MindsStormUtil

import time

class LineFollower:
    BLACK = 8
    WHITE = 42
    THRESHOLD = (BLACK+WHITE)/2
    PHRESHOLD = (BLACK+WHITE)/3
    PROPORTIONAL_GAIN = 2.2
    DRIVE_SPEED = 90
    TURN_SPEED = 10000
    INDEX = 0
    

    

    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor):
        self.drive_base = drive_base
        self.drive_base.settings(turn_rate=1000, turn_acceleration=10000)
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.watch = StopWatch()
        

   
    def run(self):
        
        
        # Start following the line endlessly.
        while not MindsStormUtil.check_color(color_sensor=self.color_sensor, color_value=BLUE_LINE_FOLLOW, threshold=3):
            self.PROPORTIONAL_GAIN = 2
            self.DRIVE_SPEED += 1

            light = self.color_sensor.reflection()
            EV3Brick().screen.print(self.color_sensor.reflection()-self.THRESHOLD)
            
            # ROBOT on line
            if light >= self.PHRESHOLD:               

                
                # Calculate the deviation from the threshold.
                deviation = light - self.THRESHOLD

                # Calculate the turn rate.
                turn_rate = self.PROPORTIONAL_GAIN * deviation

                # Set the drive base speed and turn rate.
                self.drive_base.drive(self.DRIVE_SPEED, turn_rate)
                self.DRIVE_SPEED += 1
                                      

                # You can wait for a short time or do other things in this loop.
                if self.ultrasonic_sensor.distance() <= 90:
                    self.avoid_obstacle()

            # ROBOT not on line -> search until we find it again (poll sensor each loop)
            else:
                EV3Brick().speaker.beep(800,6)
                self.search_line()

    def scan_turn_until_line(self, angle = 90) -> bool:
        """Rotate in place and poll the color sensor until the line is found.

        Returns True if the line was found, False on timeout.
        debounce: number of consecutive positive reads required to accept the line (helps filter noise)
        """
        for i in range(9):
            self.drive_base.turn(angle=angle/9)
            if MindsStormUtil.check_color(color_sensor=self.color_sensor, color_value=BLUE_LINE_FOLLOW, threshold=3):
                return True
            elif self.color_sensor.reflection() >= self.THRESHOLD:
                return True
        self.drive_base.turn(-angle)
            
        return False
        
    def avoid_obstacle(self):
        #TODO implement this  :D
        self.drive_base.turn(80)
        self.drive_base.straight(150)
        self.drive_base.turn(-80)
        self.drive_base.straight(400)
        self.drive_base.turn(-80)
        self.drive_base.straight(150)
        self.drive_base.turn(80)



    def search_line(self):
        self.DRIVE_SPEED=40
        for i in range(3):
            if self.scan_turn_until_line(-90):
                self.drive_base.drive(self.DRIVE_SPEED, -70)
                return
            elif self.scan_turn_until_line(90):
                self.drive_base.drive(self.DRIVE_SPEED, 70)
                return
                        
            self.drive_base.straight(100)
            if self.color_sensor.reflection()>self.PHRESHOLD:
                return



 
