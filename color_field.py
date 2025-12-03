#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
import time

class ColorField:
    BLACK = 8
    WHITE = 45 # 44 - 48
    RED = 16 # 14- 18
    BLUE = 2

    INITIAL_WALL_THRESHOLD = 100  # Starting distance to wall
    THRESHOLD_INCREASE = 15  # Reduce by this much every 3 turns

    DRIVE_SPEED = 200
    TURN_ANGLE = 90  # degrees
    TURN_RIGHT = -90
    TURN_LEFT = 90
    
    ALIGN = -10  # Small backward steps for wall alignment
    DISTANCE_TO_START = 150  # Distance from wall to starting position


    def __init__(self, drive_base:DriveBase, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor, touch_sensor: TouchSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.touch_sensor = touch_sensor
        self.red_found = False
        self.white_found = False
        self.turn_count = 0
        self.current_threshold = self.INITIAL_WALL_THRESHOLD
        self.positioned = False

    def initial_positioning(self):
        """Align against right wall using touch sensor, similar to bridge alignment"""
        ev3 = EV3Brick()
        
        print("Starting alignment...")
        ev3.speaker.beep(500, 200)
        
        # Wait for BLUE to start
        while self.color_sensor.reflection() != self.BLUE:
            self.drive_base.drive(self.DRIVE_SPEED, 0)
            time.sleep(0.05)
        
        self.drive_base.stop()
        print("BLUE detected! Aligning...")
        ev3.speaker.beep(1000, 300)
        
        # Continue a bit forward after blue
        self.drive_base.straight(200)
        
        # Turn right to face the wall
        self.drive_base.turn(self.TURN_LEFT)
        time.sleep(0.2)
        
        # Drive backwards until touching the wall or max attempts
        max_counter = 20
        while (not self.touch_sensor.pressed()) and (max_counter > 0):
            self.drive_base.straight(self.ALIGN)
            time.sleep(0.1)
            max_counter = max_counter - 1
        
        print("Wall contact or max attempts reached")
        
        # Drive forward to create distance from wall
        self.drive_base.straight(self.DISTANCE_TO_START)
        time.sleep(0.2)
        
        # Turn left to face forward
        self.drive_base.turn(self.TURN_RIGHT)
        time.sleep(0.2)
        
        print("Positioning complete! Starting run...")
        ev3.speaker.beep(1500, 200)
        
        self.positioned = True
        
    def run(self):
        ev3 = EV3Brick()

        # Do initial positioning ONCE
        if not self.positioned:
            self.initial_positioning()

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
            
            # Check if wall detected with current threshold
            if distance < self.current_threshold:
                self.avoid_obstacle()
            else:
                # Continue forward
                self.drive_base.drive(self.DRIVE_SPEED, 0)

            time.sleep(0.05)
            

    def avoid_obstacle(self):
        ev3 = EV3Brick()

        # Stop current motion
        self.drive_base.stop()
        time.sleep(0.1)

        # Turn left 90 degrees (NO backing up)
        self.drive_base.turn(self.TURN_ANGLE)
        
        # Increment turn counter
        self.turn_count += 1
        
        # Every 4 turns, reduce the wall threshold (narrow the area)
        if self.turn_count % 4 == 0:
            self.current_threshold += self.THRESHOLD_INCREASE
            if self.current_threshold > 180:  # Minimum threshold
                self.current_threshold = 180
            ev3.speaker.beep(800, 100)
        
        time.sleep(0.1)