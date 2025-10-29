#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor
from pybricks.parameters import Port
from pybricks.iodevices import Ev3devSensor
from time import sleep
from move import move

# Create your objects here

# Initialize the EV3 Brick.
ev3 = EV3Brick()

# Initialize a motor at port B.
test_motor = Motor(Port.B)
mover = move(left_motor=Motor(Port.B), right_motor=Motor(Port.C))
mover.move_forwards()
mover.turn_left_fast()
mover.move_forwards()
mover.turn_right_fast()
mover.move_forwards()
mover.turn_left_slow()
mover.turn_right_slow()
mover.move_forwards()

# Write your program here

# Play a sound.
#ev3.speaker.beep()

# Run the motor up to 500 degrees per second. To a target angle of 90 degrees.
#test_motor.run_target(50000, 9000)

# Play another beep sound.
# /**
# ev3.speaker.beep(frequency=1000, duration=500)

# ev3.speaker.beep(frequency=392, duration=500)
# sleep(0.0025)

# ev3.speaker.beep(frequency=392, duration=500)

# ev3.speaker.beep(frequency=440, duration=500)
# ev3.speaker.beep(frequency=392, duration=500)
# ev3.speaker.beep(frequency=523, duration=500)
# ev3.speaker.beep(frequency=494, duration=500)

# **/

# sensor = Ev3devSensor(Port.S1)
# # while True:
# #     result = sensor.read('TOUCH')
# #     if result == "(4059,)":
# #         print("hello")
# #     else:
# #         print("bob")

# ev3.screen.print("bob")
# sleep(5)


