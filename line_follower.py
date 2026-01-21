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
    PROPORTIONAL_GAIN = 1.6
    DRIVE_SPEED = 110
    TURN_SPEED = 200
    INDEX = 0
    

    

    def __init__(self, drive_base:DriveBase, precision_module:PrecisionModule, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor):
        self.drive_base = drive_base
        self.precision_module = precision_module
        self.drive_base.settings(turn_rate=200, turn_acceleration=100)
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.watch = StopWatch()
        

   
    def run(self):
        
        
        # Start following the line endlessly.
        while not MindsStormUtil.check_color(color_sensor=self.color_sensor, color_value=BLUE_LINE_FOLLOW, threshold=3):

            light = self.color_sensor.reflection()
            EV3Brick().screen.print(self.color_sensor.reflection()-self.THRESHOLD)
            print("11")
            # ROBOT on line
            if light >= self.PHRESHOLD:               

                
                # Calculate the deviation from the threshold.
                deviation = light - self.THRESHOLD

                # Calculate the turn rate.
                turn_rate = self.PROPORTIONAL_GAIN * deviation

                # Set the drive base speed and turn rate.
                self.drive_base.drive(self.DRIVE_SPEED, turn_rate)
                                      

                # You can wait for a short time or do other things in this loop.
                if self.ultrasonic_sensor.distance() <= 90:
                    print("apples")
                    self.avoid_obstacle()

            # ROBOT not on line -> search until we find it again (poll sensor each loop)
            else:
                EV3Brick().speaker.beep(800,6)
                print(12)
                self.search_line()

    def scan_turn_until_line(self, angle = 90) -> bool:
        """Rotate in place and poll the color sensor until the line is found.

        Returns True if the line was found, False on timeout.
        """
        
        print(2)
        found = self.precision_module.turn_gyro_with_condition(angle, lambda: ((self.color_sensor.reflection() >= self.PHRESHOLD or
                                                               MindsStormUtil.check_color(color_sensor=self.color_sensor, color_value=BLUE_LINE_FOLLOW, threshold=3))))
        
        
                 
        return found
    
    """"""
        
    def avoid_obstacle(self):
        #implement this  :D
        # self.drive_base.turn(80)
        # self.drive_base.straight(150)
        # self.drive_base.turn(-80)
        # self.drive_base.straight(400)
        # self.drive_base.turn(-80)
        # self.drive_base.straight(150)
        # self.drive_base.turn(80)
        #TODO change to use precisionmodule
        self.precision_module.turn_gyro(90)
        self.precision_module.straight_gyro(150)
        self.precision_module.turn_gyro(-90)
        self.precision_module.straight_gyro(400)
        self.precision_module.turn_gyro(-90)
        self.precision_module.straight_gyro(150)
        self.precision_module.turn_gyro(90)



    def search_line(self):
        for i in range(3):
            if self.scan_turn_until_line(-90):
                self.drive_base.drive(self.DRIVE_SPEED, -90)
                wait(300)
                self.precision_module.brake()
                return
            elif self.scan_turn_until_line(180):
                self.drive_base.drive(self.DRIVE_SPEED, 90)
                wait(300)
                self.precision_module.brake()

                return
            else:
                self.precision_module.turn_gyro(-90)
                self.precision_module.brake()

                        
            self.drive_base.straight(100)
            if self.color_sensor.reflection()>=self.THRESHOLD:
                return



 
