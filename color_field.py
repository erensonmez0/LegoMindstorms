#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
import time

class ColorField:
    BLACK = 8
    WHITE = 45 # 44 - 48
    RED = 16 # TEMPORARY 14- 18

    WALL_DISTANCE_THRESHOLD = 150  # Turn when closer than this
    TURN_CLEARANCE = 80  # Distance to maintain from wall when turning

    DRIVE_SPEED = 100
    TURN_ANGLE = 90  # degrees
    INSET_DISTANCE = 50  # How much to narrow the path each turn (mm)


    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.red_found = False
        self.white_found = False
        self.inset_accumulator = 0

    def run(self):
        ev3 = EV3Brick()

        while not (self.red_found and self.white_found):
            light = self.color_sensor.reflection()

            # Detect colors
            if abs(light - self.RED) < 4 and not self.red_found:
                self.red_found = True
                ev3.speaker.beep(1000, 200)
                print("RED FOUND!")

            if abs(light - self.WHITE) < 4 and not self.white_found:
                self.white_found = True
                ev3.speaker.beep(1500, 200)
                print("WHITE FOUND!")

            if self.red_found and self.white_found:
                self.drive_base.stop()
                ev3.speaker.beep(2000, 500)
                print("Both colors found! Mission complete.")
                break

            distance = self.ultrasonic_sensor.distance()
            if distance < self.WALL_DISTANCE_THRESHOLD:
                # Wall detected - execute turn with narrowing
                self.avoid_obstacle()
            else:
                # Continue forwarding
                self.drive_base.drive(self.DRIVE_SPEED, 0)

            time.sleep(0.05)  # Small delay for sensor readings
            

    """
    It should turn left, but when turning it also should narrow down the area it's running in
    """
    def avoid_obstacle(self):
        ev3 = EV3Brick()

        # Stop current motion
        self.drive_base.stop()

        # Back up slightly to ensure clearance
        self.drive_base.straight(-self.TURN_CLEARANCE)

        # Increase inset for next pass (narrow the search area)
        self.inset_accumulator += self.INSET_DISTANCE
        
        # Turn left 90 degrees
        self.drive_base.turn(self.TURN_ANGLE)
        
        # Move forward a bit, but less than before (narrowing)
        forward_distance = 100 - self.inset_accumulator
        if forward_distance > 20:  # Minimum forward distance
            self.drive_base.straight(forward_distance)
        
        # Turn left again to face parallel to previous direction
        self.drive_base.turn(self.TURN_ANGLE)
        
        # Now continue forward (inset from previous path)
        #print(f"Turned left, inset: {self.inset_accumulator}mm")
        
        time.sleep(0.1)

