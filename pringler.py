from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait
from precision_module import PrecisionModule
from bridge import Bridge
from mindstorm_util import MindsStormUtil
from config import BLUE
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
        self.arm_motor.run_target(500,470)

    def initiate_hug_mode(self):
        self.arm_motor.run_target(500,380)

    def disengage(self):
        self.arm_motor.run_target(500,-200)

    def initialise(self):
        self.drive_base.straight(200)
        distance_from_wall = 100
        #go against wall and set distance
        self.drive_base.turn(-90)

        self.precision_module.straight_gyro_with_condition(-200, lambda:(self.touch_sensor.pressed()))
        if self.ultrasonic_sensor.distance()>distance_from_wall:
            self.precision_module.straight_gyro_with_condition(200, lambda:(self.ultrasonic_sensor.distance()==distance_from_wall))
        elif self.ultrasonic_sensor.distance()<distance_from_wall:
            self.precision_module.straight_gyro_with_condition(-200, lambda:(self.ultrasonic_sensor.distance()==distance_from_wall))
        self.precision_module.turn_gyro(-90)
            
    
    
    def prep_for_bridge(self):
        DISTANCE_TO_BRIDGE_START = Bridge.DISTANCE_TO_BRIDGE_START
        TURN_LEFT = Bridge.TURN_LEFT
        self.precision_module.straight_gyro(-100)
        self.precision_module.turn_gyro(-135)
        self.precision_module.straight_gyro_with_condition(-2000, lambda:(self.touch_sensor.pressed()))
        self.precision_module.straight_gyro(DISTANCE_TO_BRIDGE_START)
        self.precision_module.turn_gyro(TURN_LEFT)

        self.precision_module.straight_gyro_with_condition(3000, lambda:MindsStormUtil.check_color(self.color_sensor, BLUE))




        
    def run(self):
        distance_from_end = 650
        distance_from_pring = 40
        distance_from_square = -550
        self.initialise()
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


        


    