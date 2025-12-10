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
        self.arm_motor.run_target(500,400)

    def initiate_hug_mode(self):
        self.arm_motor.run_target(500,300)

    def disengage(self):
        self.arm_motor.run_target(500,-250)

    def to_wall(self):
        while True:
            self.drive_base.drive(140,0)
            if self.ultrasonic_sensor.distance()<=60:
                self.drive_base.turn(-90)
                self.initiate_hug_mode()
                return
            
    def to_can(self):
        while True:
            self.drive_base.drive(140,10)
            EV3Brick().screen.print(self.ultrasonic_sensor.distance())
            if self.ultrasonic_sensor.distance()<=30:
                self.grab()
                self.drive_base.turn(-90)
                return

    def to_square(self):
        hits = 0
        self.drive_base.turn(-90)
        while hits < 2:
            self.drive_base.drive(40,0)
            if self.color_sensor.reflection()>=30:
                hits += 0
        self.disengage()
        self.drive_base.straight(-40)
        self.drive_base.drive(0,200)
        
    def run(self):
        self.to_wall()
        self.to_can()
        self.to_square()


    