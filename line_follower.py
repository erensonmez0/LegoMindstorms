#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

import time

class LineFollower:
    BLACK = 8
    WHITE = 42
    BLUE = 6
    THRESHOLD = (BLACK+WHITE)/2
    PHRESHOLD = (BLACK+WHITE)/3
    PROPORTIONAL_GAIN = 1.6
    DRIVE_SPEED = 60
    INDEX = 0

    

    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor|None=None):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.watch = StopWatch()

   
    def run(self):
        light = self.color_sensor.reflection()
        EV3Brick().screen.clear()
        EV3Brick().screen.print("light:", light)
        EV3Brick().screen.print("th:", self.THRESHOLD)
        
        # Start following the line endlessly.
        while True:

            light = self.color_sensor.reflection()
            EV3Brick().screen.print(self.color_sensor.reflection()-self.THRESHOLD)
            
            # ROBOT on line
            if light > self.PHRESHOLD:
                

                
                # Calculate the deviation from the threshold.
                deviation = light - self.THRESHOLD

                # Calculate the turn rate.
                turn_rate = self.PROPORTIONAL_GAIN * deviation

                # Set the drive base speed and turn rate.
                self.drive_base.drive(self.DRIVE_SPEED, int(turn_rate))
                                      

                # You can wait for a short time or do other things in this loop.
                time.sleep(0.1)

            # ROBOT not on line -> search until we find it again (poll sensor each loop)
            else:
                EV3Brick().speaker.beep(800,6)
                self.search_line()

    def scan_turn_until_line(self, angle = 90) -> bool:
        """Rotate in place and poll the color sensor until the line is found.

        Returns True if the line was found, False on timeout.
        debounce: number of consecutive positive reads required to accept the line (helps filter noise)
        """
        for i in range(15):
            self.INDEX = (self.INDEX + 1)%2
            self.drive_base.turn(angle=angle/15)
            if self.color_sensor.reflection() >= self.THRESHOLD:
                return True
        self.drive_base.turn(-angle)
            
        return False
        
    def avoid_obstacle(self):
        #TODO implement this  :D
        self.drive_base.drive(10,60)
        self.drive_base.drive(10,-60)

    def search_line(self):
        for i in range(5):
            if self.scan_turn_until_line(90):
                
                return
            elif self.scan_turn_until_line(-90):
                return
                        
            self.drive_base.straight(200)
            if self.color_sensor.reflection()>self.THRESHOLD:
                return




