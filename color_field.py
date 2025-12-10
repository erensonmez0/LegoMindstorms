#!/usr/bin/env python3
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from precision_module import PrecisionModule
import time

class ColorField:
    BLACK = 8
    WHITE = 45  # 44 - 48
    RED = 16  # 14- 18
    BLUE = 2

    INITIAL_WALL_THRESHOLD = 100  # Starting distance to wall
    THRESHOLD_DECREASE = 20  # Decrease by this much every 4 turns

    DRIVE_SPEED = 200
    
    ALIGN = -10  # Small backward steps for wall alignment
    DISTANCE_TO_START = 80  # Distance from wall to starting position
    INITIAL_STRAIGHT = 200  # Distance to drive straight at the beginning

    def __init__(self, drive_base: DriveBase, color_sensor: ColorSensor, 
                 ultrasonic_sensor: UltrasonicSensor, touch_sensor: TouchSensor,
                 precision_module: PrecisionModule):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.touch_sensor = touch_sensor
        self.precision_module = precision_module
        self.red_found = False
        self.white_found = False
        self.turn_count = 0
        self.current_threshold = self.INITIAL_WALL_THRESHOLD
        self.positioned = False

    def initial_positioning(self):
        """Align against right wall using touch sensor"""
        ev3 = EV3Brick()
        
        print("Starting alignment...")
        ev3.speaker.beep(500, 200)
        
        # Drive straight at the beginning
        print("Driving straight...")
        self.precision_module.straight_gyro(self.INITIAL_STRAIGHT)
        time.sleep(1.0)
        
        # Turn LEFT to face the wall
        print("Turning left to wall...")
        self.precision_module.turn_gyro(-90)
        time.sleep(1.0)
        
        # Drive backwards until touching the wall or max attempts
        print("Backing up to wall...")
        max_counter = 20
        while (not self.touch_sensor.pressed()) and (max_counter > 0):
            self.precision_module.straight_gyro(self.ALIGN)
            time.sleep(0.5)
            max_counter = max_counter - 1
        
        print("Wall contact: {self.touch_sensor.pressed()}, attempts left: {max_counter}")
        time.sleep(0.5)
        
        # Drive forward to create distance from wall
        print("Creating distance from wall...")
        self.precision_module.straight_gyro(self.DISTANCE_TO_START)
        time.sleep(1.0)
        
        # Turn RIGHT to face forward
        print("Turning right to start position...")
        self.precision_module.turn_gyro(90)
        time.sleep(1.0)
        
        print("Positioning complete! Starting search...")
        ev3.speaker.beep(1500, 200)
        
        self.positioned = True
        
    def run(self):
        ev3 = EV3Brick()

        # Do initial positioning ONCE
        if not self.positioned:
            self.initial_positioning()

        print("Starting main search loop...")
        
        while not (self.red_found and self.white_found):
            light = self.color_sensor.reflection()

            # Detect colors
            if abs(light - self.RED) < 4 and not self.red_found:
                self.red_found = True
                ev3.speaker.beep(1000, 200)
                print("*** RED FOUND! ***")

            if abs(light - self.WHITE) < 4 and not self.white_found:
                self.white_found = True
                ev3.speaker.beep(1500, 200)
                print("*** WHITE FOUND! ***")

            if self.red_found and self.white_found:
                self.drive_base.stop()
                ev3.speaker.beep(2000, 500)
                print("=== BOTH COLORS FOUND! MISSION COMPLETE! ===")
                break

            distance = self.ultrasonic_sensor.distance()
            
            # Check if wall detected with current threshold
            if distance < self.current_threshold:
                print("Wall detected at {distance}mm (threshold: {self.current_threshold}mm)")
                self.avoid_obstacle()
            else:
                # Continue forward
                self.drive_base.drive(self.DRIVE_SPEED, 0)

            time.sleep(0.05)
            

    def avoid_obstacle(self):
        ev3 = EV3Brick()

        # Stop current motion
        self.drive_base.stop()
        time.sleep(0.5)

        # Turn LEFT 90 degrees
        print("Turning left...")
        self.precision_module.turn_gyro(-90)
        
        time.sleep(1.0)
        
        # Increment turn counter
        self.turn_count += 1
        
        print("=== Turn #{self.turn_count}, threshold: {self.current_threshold}mm ===")
        
        # Every 4 turns, DECREASE the wall threshold (narrow the area)
        if self.turn_count % 4 == 0:
            self.current_threshold -= self.THRESHOLD_DECREASE
            if self.current_threshold < 40:
                self.current_threshold = 40
            print("*** NARROWING! New threshold: {self.current_threshold}mm ***")
            ev3.speaker.beep(800, 100)
        
        time.sleep(0.5)