# Single-file script for the Pybricks Virtual Robot Simulator

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# ---- Robot setup (adjust if your sim uses different ports) ----
ev3 = EV3Brick()
left_motor  = Motor(Port.A)
right_motor = Motor(Port.B)

# Wheel diameter 56 mm (EV3 wheel), axle_track ~152 mm (tune for your model)
WHEEL_DIAMETER_MM = 56
AXLE_TRACK_MM     = 152

robot = DriveBase(left_motor, right_motor,
                  wheel_diameter=WHEEL_DIAMETER_MM,
                  axle_track=AXLE_TRACK_MM)

# Base driving profile
BASE_STRAIGHT_SPEED = 200   # mm/s
BASE_STRAIGHT_ACCEL = 200   # mm/s^2
BASE_TURN_RATE      = 120   # deg/s
BASE_TURN_ACCEL     = 120   # deg/s^2
robot.settings(BASE_STRAIGHT_SPEED, BASE_STRAIGHT_ACCEL,
               BASE_TURN_RATE, BASE_TURN_ACCEL)

# Sensors (ok if unused)
color_sensor  = ColorSensor(Port.S1)
ultra_sensor  = UltrasonicSensor(Port.S2)
gyro_sensor   = GyroSensor(Port.S3)

# Optional third motor (e.g., gripper)
# motorC = Motor(Port.C)

# ---- Movement helper ----
class Move:
    def __init__(self, robot: DriveBase, ev3: EV3Brick):
        self.r = robot
        self.ev3 = ev3

    def forwards(self, mm=360):
        print("Moving forwards")
        self.r.straight(mm)

    def backwards(self, mm=360):
        print("Moving backwards")
        self.r.straight(-mm)

    def _set_slow(self):
        self.r.settings(100, 100, 60, 60)

    def _set_base(self):
        self.r.settings(BASE_STRAIGHT_SPEED, BASE_STRAIGHT_ACCEL,
                        BASE_TURN_RATE, BASE_TURN_ACCEL)

    def turn_left_fast(self, deg=90):
        print("Turning left fast")
        self._set_base()
        self.r.turn(-deg)

    def turn_right_fast(self, deg=90):
        print("Turning right fast")
        self._set_base()
        self.r.turn(deg)

    def turn_left_slow(self, deg=90):
        print("Turning left slow")
        self._set_slow()
        self.r.turn(-deg)
        self._set_base()

    def turn_right_slow(self, deg=90):
        print("Turning right slow")
        self._set_slow()
        self.r.turn(deg)
        self._set_base()

# ---- Demo sequence (your old main) ----
mover = Move(robot, ev3)

print("Hello World")            # display/console — safer than ev3.screen in sim

mover.forwards(360)
wait(500)
mover.turn_left_fast(90)
wait(500)
mover.forwards(360)
wait(500)
mover.turn_right_fast(90)
wait(500)
mover.forwards(360)
wait(500)
mover.backwards(360)
wait(500)
mover.turn_left_slow(90)
wait(500)
mover.turn_right_slow(90)
wait(500)
mover.forwards(360)
