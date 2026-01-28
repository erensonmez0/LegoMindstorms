#!/usr/bin/env python3
import time
from time import sleep

from pybricks.ev3devices import ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase

from config import *
from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule


class ColorField:
    BLACK = 8
    WHITE = 45  # 44 - 48
    RED = 16  # 14- 18
    BLUE = 2

    INITIAL_WALL_THRESHOLD = 100  # Starting distance to wall
    THRESHOLD_DECREASE = 20  # Decrease by this much every 4 turns

    DRIVE_SPEED = 200
    
    ALIGN = -10  # Small backward steps for wall alignment
    DISTANCE_TO_START = 50  # Distance from wall to starting position
    INITIAL_STRAIGHT = -50  # Distance to drive straight at the beginning

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

    def initial_positioning(self):
        ev3 = EV3Brick()

        # Drive straight at the beginning
        self.precision_module.straight_gyro(-200)
        time.sleep(1.0)
        
        # Turn LEFT to face the wall
        self.precision_module.turn_gyro(20)
        self.precision_module.straight_gyro(70)
        self.precision_module.turn_gyro(70)
        time.sleep(1.0)

        self.align_backwards(-80)

        # Drive forward to create distance from wall
        self.precision_module.straight_gyro(70)
        time.sleep(1.0)
        
        # Turn RIGHT to face forward
        self.precision_module.turn_gyro(TURN_RIGHT)
        time.sleep(1.0)


    def align_backwards(self, distance):
        # save current speed and change to slow
        temp_speed = self.precision_module.straight_speed
        self.precision_module.change_straight_speed(STRAIGHT_SPEED_SLOW)

        self.precision_module.straight_gyro_with_condition(distance, lambda: (self.touch_sensor.pressed()))

        # change current speed back to original value
        self.precision_module.change_straight_speed(temp_speed)


    def zickzack(self):
        ev3 = EV3Brick()
        offset = 40
        found_red = False
        found_white = False
        turn_counter = 0
        distance_to_wall = 120
        distance = 750
        color_threshold = 4
        distance_after_sucessfull_find = 70

        self.precision_module.change_straight_speed(STRAIGHT_SPEED_MEDIUM)

        while not (found_red and found_white):
            self.precision_module.straight_gyro_with_condition(
                distance,
                lambda: ((MindsStormUtil.check_color(self.color_sensor, RED, color_threshold))
                        or (MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold))
                        or (self.ultrasonic_sensor.distance() < distance_to_wall))
            )
            if MindsStormUtil.check_color(self.color_sensor, RED, color_threshold) and not found_white and not found_red:
                found_red = True
                ev3.speaker.beep(1000, 200)
                self.precision_module.straight_gyro_with_condition(
                    distance_after_sucessfull_find,
                    lambda: not MindsStormUtil.check_color(self.color_sensor, RED, color_threshold))
                continue
            elif MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold) and not found_red  and not found_white:
                found_white = True
                ev3.speaker.beep(1500, 200)
                self.precision_module.straight_gyro_with_condition(
                    distance_after_sucessfull_find,
                    lambda: not MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold))
                continue
            elif MindsStormUtil.check_color(self.color_sensor, RED, color_threshold) and not found_white and found_red:
                self.precision_module.straight_gyro_with_condition(
                    distance_after_sucessfull_find,
                    lambda: not MindsStormUtil.check_color(self.color_sensor, RED, color_threshold))
                continue
            elif MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold) and not found_red and found_white:
                self.precision_module.straight_gyro_with_condition(
                    distance_after_sucessfull_find,
                    lambda: not MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold))
                continue
            elif MindsStormUtil.check_color(self.color_sensor, RED, color_threshold) and found_white:
                break
            elif MindsStormUtil.check_color(self.color_sensor, WHITE, color_threshold) and found_red:
                break

            sleep(0.5)

            if turn_counter % 2 == 0:
                self.precision_module.turn_gyro(TURN_LEFT)
                self.precision_module.straight_gyro(offset)
                self.precision_module.turn_gyro(TURN_LEFT)
                self.align_backwards(-(distance_to_wall + 15))
                self.precision_module.straight_gyro(distance_to_wall)

            elif turn_counter % 2 == 1:
                self.precision_module.turn_gyro(TURN_RIGHT)
                self.precision_module.straight_gyro(offset)
                self.precision_module.turn_gyro(TURN_RIGHT)

            turn_counter = turn_counter + 1

        ev3.speaker.beep(2000, 500)
        sleep(0.1)
        ev3.speaker.beep(2000, 500)
        sleep(0.1)
        ev3.speaker.beep(2000, 500)



    def run(self):
        self.initial_positioning()
        self.zickzack()



