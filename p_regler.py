#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
import time


class PRegler:
    BLACK = 8
    WHITE = 42
    THRESHOLD = (BLACK + WHITE) / 2
    PROPORTIONAL_GAIN = 1.2
    DRIVE_SPEED = 100

    def __init__(self, drive_base: DriveBase, color_sensor: ColorSensor,
                 ultrasonic_sensor: UltrasonicSensor | None = None):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor

    def run(self):
        # Start following the line endlessly.
        while 1 == 1:

            light = self.color_sensor.reflection()                              # light = r

            # ROBOT on line
            if light > self.THRESHOLD:                                          # THRESHOLD = w

                # Calculate the deviation from the threshold.
                deviation = self.THRESHOLD - light                              # deviation = xd

                # Calculate the turn rate.
                turn_rate = self.PROPORTIONAL_GAIN * deviation                  # turn_rate = y

                # Set the drive base speed and turn rate.
                self.drive_base.drive(self.DRIVE_SPEED, int(turn_rate))

                # You can wait for a short time or do other things in this loop.
                time.sleep(0.2)

            # ROBOT not on line
            else:
                self.drive_base.drive(0, 0)
                EV3Brick().speaker.beep(frequency=500, duration=100)

