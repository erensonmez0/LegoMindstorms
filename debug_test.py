import time

from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase

from config import BLUE, DISTANCE_TO_BRIDGE_START, TURN_LEFT
from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule


class DebugTest:
    def __init__(self, drive_base:DriveBase, arm_motor:Motor, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor, precision_module:PrecisionModule,touch_sensor:TouchSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.arm_motor = arm_motor
        self.precision_module = precision_module
        self.touch_sensor = touch_sensor

    def run(self):
        

        self.precision_module.straight_gyro(1000)