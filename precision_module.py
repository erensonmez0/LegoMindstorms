#!/usr/bin/env pybricks-micropython
from time import sleep

from pybricks.ev3devices import Motor, GyroSensor
from pybricks.robotics import DriveBase


class PrecisionModule:

    def __init__(
            self,
            left_motor: Motor,
            right_motor: Motor,
            drive_base: DriveBase,
            straight_speed,
            straight_acceleration,
            turn_rate,
            turn_acceleration,
            gyro_sensor: GyroSensor,
    ):
        """PrecisionModule(left_motor, right_motor, wheel_diameter, axle_track, gyro_sensor)

        Arguments:
            :param left_motor (Motor):
                The motor that drives the left wheel.
            :param right_motor (Motor):
                The motor that drives the right wheel.
            :param drive_base {DriveBase}: Given drive base to operate on.
            :param straight_speed (Number, mm): Speed when going straight.
            :param straight_acceleration (Number, mm): Acceleration when going straight.
            :param turn_rate (Number, mm): Speed when turning.
            :param turn_acceleration (Number, mm): Acceleration when turning.
            :param gyro_sensor (GyroSensor): Gyro sensor to measure angles and distances.
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.drive_base = drive_base
        self.straight_speed = straight_speed
        self.straight_acceleration = straight_acceleration
        self.turn_rate = turn_rate
        self.turn_acceleration = turn_acceleration
        self.gyro_sensor = gyro_sensor



    def straight_gyro_with_condition(
            self, distance: int, condition_to_check
    ) -> None:
        """straight(distance)

        Drives straight for a given distance and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Example use:
            precision_module.straight_gyro_with_condition(-500, (lambda: MindsStormUtil.tempBool(touche_sensor)))
            precision_module.straight_gyro_with_condition(-500, (lambda: touch_sensor.pressed()))

        Arguments:
            :param distance: Distance to travel in mm
            :param condition_to_check: Will continuously check this condition (please give as "lambda:") and abort if true
        """

        robotSpeed = self.straight_speed

        self.drive_base.reset()
        self.gyro_sensor.reset_angle(0)

        PROPORTIONAL_GAIN = 1.1
        if distance < 0:  # move backwards
            while (self.drive_base.distance() > distance) and not condition_to_check():
                reverseSpeed = -1 * robotSpeed
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(reverseSpeed, angle_correction)
        elif distance > 0:  # move forwards
            while (self.drive_base.distance() < distance) and not condition_to_check():
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(robotSpeed, angle_correction)
        self.drive_base.stop()



    def straight_gyro(
            self, distance: int
    ) -> None:
        """straight(distance)

        Drives straight for a given distance and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            :param distance: Distance to travel in mm
        """
        self.straight_gyro_with_condition(distance, lambda: False)



    def turn_gyro(
            self, angle: int
    ) -> None:
        """turn(angle)

        Turns in place by a given angle and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            :param angle: Angle of the turn in degree.
        """
        speed = self.turn_rate

        # angle correction
        angle = angle * 0.985

        self.gyro_sensor.reset_angle(0)
        if angle < 0:
            while self.gyro_sensor.angle() > angle:
                self.right_motor.run(speed=(-1 * speed))
                self.left_motor.run(speed=speed)
        elif angle > 0:
            while self.gyro_sensor.angle() < angle:
                self.right_motor.run(speed=speed)
                self.left_motor.run(speed=(-1 * speed))

        self.right_motor.brake()
        self.left_motor.brake()
