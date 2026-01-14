from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase

from config import *
from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule
from bridge import Bridge

import time


class Pringler:
    def __init__(self, drive_base:DriveBase, arm_motor:Motor, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor, precision_module:PrecisionModule,touch_sensor:TouchSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.arm_motor = arm_motor
        self.precision_module = precision_module
        self.touch_sensor = touch_sensor

    def grab(self):
        self.arm_motor.run_target(500,430)

    def initiate_hug_mode(self):
        self.arm_motor.run_target(500,320)

    def disengage(self):
        self.arm_motor.run_target(500,-5)

    def initialise(self):
        self.drive_base.straight(200)
        distance_from_wall = 150
        #go against wall and set distance
        self.drive_base.turn(-90)

        self.precision_module.straight_gyro_with_condition(-100, lambda:(self.touch_sensor.pressed()))
        if self.ultrasonic_sensor.distance()>distance_from_wall:
            self.precision_module.straight_gyro_with_condition(200, lambda:(self.ultrasonic_sensor.distance()==distance_from_wall))
        elif self.ultrasonic_sensor.distance()<distance_from_wall:
            self.precision_module.straight_gyro_with_condition(-200, lambda:(self.ultrasonic_sensor.distance()==distance_from_wall))
        self.precision_module.turn_gyro(-90)
            
    
    
    def prep_for_bridge(self):
        self.precision_module.straight_gyro(-100)
        self.precision_module.turn_gyro(-135)
        self.precision_module.straight_gyro_with_condition(-2000, lambda:(self.touch_sensor.pressed()))
        # save current speed and change to slow
        temp_speed = self.precision_module.straight_speed
        self.precision_module.change_straight_speed(STRAIGHT_SPEED_SLOW)

        # drive backwards till touching the wall
        self.precision_module.straight_gyro_with_condition(-300, lambda:(self.touch_sensor.pressed()))
        self.precision_module.straight_gyro(50)
        self.precision_module.straight_gyro_with_condition(-60, lambda: (self.touch_sensor.pressed()))

        # drive to startpoint of ramp
        self.precision_module.straight_gyro(DISTANCE_TO_BRIDGE_START)
        self.precision_module.turn_gyro(TURN_LEFT)

        self.precision_module.straight_gyro_with_condition(300, lambda:MindsStormUtil.check_color(self.color_sensor, BLUE))

        # change current speed back to original value
        self.precision_module.change_straight_speed(temp_speed)


    def run(self):
        distance_from_end = 650
        distance_from_pring = 50
    
        distance_from_square = -550
        self.initialise()
        self.precision_module.straight_gyro(800)
        self.precision_module.straight_gyro_with_condition(10000, lambda:self.ultrasonic_sensor.distance()<=distance_from_end)
        self.precision_module.turn_gyro(45)
        self.initiate_hug_mode()
        self.precision_module.straight_gyro_with_condition(10000, lambda:self.ultrasonic_sensor.distance()<=distance_from_pring)
        self.grab()
        time.sleep(1)
        self.precision_module.straight_gyro(distance_from_square)
        self.disengage()
        self.precision_module.straight_gyro(-100)
        self.drive_base.drive(0,10000)   
        
        
        self.prep_for_bridge()
