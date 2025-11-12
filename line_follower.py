#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
import time

class LineFollower:
    BLACK = 8
    WHITE = 42
    BLUE = 6
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
                self.drive_base.drive(self.DRIVE_SPEED, int(turn_rate))
                                      

                # You can wait for a short time or do other things in this loop.
                time.sleep(0.2)

            # ROBOT not on line -> search until we find it again (poll sensor each loop)
            else:
                # Try scanning to the right first, then to the left if not found.
                self.drive_base.straight(100)
                found = self.scan_turn_until_line(turn_rate=60, debounce=1, timeout_s=.0)
                if not found:
                    found = self.scan_turn_until_line(turn_rate=-60, debounce=1, timeout_s=3.0)
                # ensure we stop motion (scan_turn_until_line stops on success or timeout)
                self.drive_base.drive(0, 0)

    def scan_turn_until_line(self, turn_rate: int = 60, debounce: int = 1, timeout_s: float = 5.0) -> bool:
        """Rotate in place and poll the color sensor until the line is found.

        Returns True if the line was found, False on timeout.
        debounce: number of consecutive positive reads required to accept the line (helps filter noise)
        """
        start = time.time()
        good_reads = 0

        # start rotation in place
        self.drive_base.drive(0, turn_rate)

        try:
            while True:
                # safety timeout
                if time.time() - start > timeout_s:
                    return False

                light = self.color_sensor.reflection()
                if light >= self.THRESHOLD:
                    good_reads += 1
                else:
                    good_reads = 0

                if good_reads >= debounce:
                    return True

                # small delay to let sensor update
                time.sleep(0.04)
        finally:
            # stop motion immediately
            self.drive_base.drive(0, 0)
        
    def avoid_obstacle(self):
        self.drive_base.drive(10,60)
        self.drive_base.drive(10,-60)


