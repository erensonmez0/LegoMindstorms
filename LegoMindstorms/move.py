from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from time import sleep
class move:
    def __init__ (self, left_motor, right_motor):
        self.left_motor = left_motor
        self.right_motor = right_motor


    def move_forwards(self):
        self.left_motor.run_target(50000, 3600, wait=False)
        self.right_motor.run_target(50000, 3600,wait=False)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()

    def turn_left_fast(self):
        self.left_motor.run_target(50000, 90, wait=False)
        self.right_motor.run_target(50000, -90, wait=False)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()    

    def turn_right_fast(self):
        self.right_motor.run_target(50000, 90, wait=False)
        self.left_motor.run_target(50000, -90, wait=False)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()

    def turn_left_slow(self):
        self.left_motor.run_target(50000, 90, wait=False)
        self.right_motor.run_target(50000, -90, wait=False)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()

    def turn_right_slow(self):
        self.right_motor.run_target(50000, 90, wait=False)
        self.left_motor.run_target(50000, -90, wait=False)
        self.left_motor.wait_until_not_moving()
        self.right_motor.wait_until_not_moving()
