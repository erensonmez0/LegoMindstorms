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
    PROPORTIONAL_GAIN = 1
    DRIVE_SPEED = 50
    TURNS = [90, -180, -90, 180]
    INDEX = 0

    

    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor|None=None):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.data = DataLog('time', 'reflection')
        self.watch = StopWatch()

   
    def run(self):
        light = self.color_sensor.reflection()
        EV3Brick().screen.clear()
        EV3Brick().screen.print("light:", light)
        EV3Brick().screen.print("th:", self.THRESHOLD)
        
        self.data.log(self.watch.time(), light)
        # Start following the line endlessly.
        while True:

            light = self.color_sensor.reflection()
            EV3Brick().screen.print(self.color_sensor.reflection()-self.THRESHOLD)
            
            # ROBOT on line
            if light >= self.BLACK:
                

                self.data.log(self.watch.time(), self.color_sensor.reflection())
                
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
                # Try scanning to the right first, then to the left if not found.
                self.search_line()

    def scan_turn_until_line(self, angle = 90) -> bool:
        """Rotate in place and poll the color sensor until the line is found.

        Returns True if the line was found, False on timeout.
        debounce: number of consecutive positive reads required to accept the line (helps filter noise)
        """
        
        turn_angle = angle/15
        for i in range(15):
            self.drive_base.turn(turn_angle)
            self.data.log(self.watch.time(), self.color_sensor.reflection())
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
            if self.scan_turn_until_line(self.TURNS[self.INDEX]):
                return
            elif self.scan_turn_until_line(self.TURNS[self.INDEX]):
                return
                        
            self.drive_base.straight(200)
            self.data.log(self.watch.time(), self.color_sensor.reflection())
            if self.color_sensor.reflection()>=self.THRESHOLD:
                return




