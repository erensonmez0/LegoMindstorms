from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from pybricks.robotics import DriveBase
from pybricks.tools import DataLog, StopWatch, wait

class Pringler:
    def __init__(self, drive_base:DriveBase, arm_motor:Motor, color_sensor:ColorSensor, ultrasonic_sensor: UltrasonicSensor):
        self.drive_base = drive_base
        self.color_sensor = color_sensor
        self.ultrasonic_sensor = ultrasonic_sensor
        self.arm_motor = arm_motor

    def grab(self):
        self.arm_motor.run_time(time=1, speed=20)

    def disengage(self):
        self.arm_motor.run_time(time=1, speed=-20)
