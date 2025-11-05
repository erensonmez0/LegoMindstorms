from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from time import sleep
class move:
    def __init__ (self, left_motor, right_motor,ev3):
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.ev3 = ev3


    def move_forwards(self):
        self.left_motor.run_target(500, 3600, wait=False)
        self.right_motor.run_target(500, 3600,wait=False)
        self.ev3.screen.print("Moving forwards")
        
    def turn_left_fast(self):
        self.left_motor.run_target(500, 3600, wait=False)
        self.right_motor.run_target(500, -3600, wait=False)
        self.ev3.screen.print("Turning left fast")

    def turn_right_fast(self):
        self.right_motor.run_target(500, 3600, wait=False)
        self.left_motor.run_target(500, -3600, wait=False)
        self.ev3.screen.print("Turning right fast")


    def turn_left_slow(self):
        self.right_motor.run_target(500, -3600, wait=False)
        self.ev3.screen.print("Turning left slow")

    def turn_right_slow(self):
        self.left_motor.run_target(500, -3600, wait=False)
        self.ev3.screen.print("Turning right slow")

    def move_backwards(self):
        self.left_motor.run_target(500, -3600, wait=False)
        self.right_motor.run_target(500, -3600,wait=False)
        self.ev3.screen.print("Moving backwards")
        
