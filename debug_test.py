import time

from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.robotics import DriveBase

from config import BLUE, DISTANCE_TO_BRIDGE_START, TURN_LEFT, BLUE_LINE_FOLLOW
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
        # ev3 = EV3Brick()

        # self.precision_module.straight_gyro(500)

        # self.arm_motor.run_target(500, 300)
        # self.arm_motor.stop()
        # time.sleep(3)
        # self.arm_motor.run_target(500, 390)
        # self.arm_motor.stop()
        # time.sleep(3)
        # self.precision_module.straight_gyro(-100)
        # self.arm_motor.run_target(500, -5)
        # self.arm_motor.stop()

        # ev3.speaker.set_volume(100, '_all_')
        # ev3.speaker.play_file('/home/robot/LegoMindstorms/goodresult82807.wav')
        # ev3.speaker.play_file('/home/robot/LegoMindstorms/boing.wav')

        # self.drive_base.straight(100)
        # self.precision_module.turn_gyro_with_condition(360, lambda: (self.touch_sensor.pressed()))
        self.precision_module.straight_gyro_with_condition(360, lambda: (self.touch_sensor.pressed()))
        #     time.sleep(1)