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
    PROPORTIONAL_GAIN =1.2
    DRIVE_SPEED = 100

    

    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor|None=None):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor

   
    def run(self):
        # Start following the line endlessly.
        while self.color_sensor.reflection()!=self.BLUE:

            light = self.color_sensor.reflection()
            
            # ROBOT on line
            if light > self.THRESHOLD:
                
                # Calculate the deviation from the threshold.
                deviation = self.THRESHOLD - light

                # Calculate the turn rate.
                turn_rate = self.PROPORTIONAL_GAIN * deviation

                # Set the drive base speed and turn rate.
                self.drive_base.drive(self.DRIVE_SPEED, turn_rate)

                # You can wait for a short time or do other things in this loop.
                sleep(0.2)

            # ROBOT not on line -> search until we find it again (poll sensor each loop)
            else:
                attempts = 0
                max_attempts = 20  # prevent infinite searching
                while attempts < max_attempts:
                    # update current light reading
                    light = self.color_sensor.reflection()
                    if light >= self.THRESHOLD:
                        break  # found the line, exit search immediately

                    # small forward step, then check again
                    self.drive_base.straight(50)
                    sleep(0.2)
                    if self.color_sensor.reflection() >= self.THRESHOLD:
                        break

                    # do a short scan: turn slightly left, then right, checking each time
                    self.drive_base.turn(15)
                    sleep(0.1)
                    if self.color_sensor.reflection() >= self.THRESHOLD:
                        break

                    self.drive_base.turn(-30)
                    sleep(0.1)
                    if self.color_sensor.reflection() >= self.THRESHOLD:
                        break

                    # return roughly to center
                    self.drive_base.turn(15)

                    attempts += 1
                    EV3Brick().screen.print(attempts)

                # stop motion when search finishes (either found or max attempts reached)
                self.drive_base.drive(0, 0)
        
    def avoid_obstacle(self):
        self.drive_base.drive(10,60)
        self.drive_base.drive(10,-60)


