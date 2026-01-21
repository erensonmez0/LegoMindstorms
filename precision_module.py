#!/usr/bin/env pybricks-micropython
from time import sleep

from pybricks.ev3devices import Motor, GyroSensor
from pybricks.robotics import DriveBase

from config import *


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

    def change_straight_speed(self, new_speed, new_acceleration=None):
        """
        Set new Speed (and optional acceleration) for whole class and underlying drive base.
        :param new_speed: New value for speed
        :param new_acceleration: Optional value for acceleration
        """
        if new_acceleration:
            self.drive_base.settings(new_speed, new_acceleration, TURN_RATE, TURN_ACCELERATION)
            self.settings(new_speed, new_acceleration, TURN_RATE, TURN_ACCELERATION)
        else:
            self.drive_base.settings(new_speed, STRAIGHT_ACCELERATION, TURN_RATE, TURN_ACCELERATION)
            self.settings(new_speed, STRAIGHT_ACCELERATION, TURN_RATE, TURN_ACCELERATION)

    def get_straight_speed(self):
        return self.straight_speed, self.straight_acceleration

    def change_turn_speed(self, new_turn_rate, new_turn_acceleration=None):
        """
            Set new turn speed (and optional turn acceleration) for whole class and underlying drive base.
            :param new_turn_rate: New value for turn rate
            :param new_turn_acceleration: Optional value for turn acceleration
            """
        if new_turn_acceleration:
            self.settings(STRAIGHT_SPEED_FAST, STRAIGHT_ACCELERATION, new_turn_rate, new_turn_acceleration)
            self.settings(STRAIGHT_SPEED_FAST, STRAIGHT_ACCELERATION, new_turn_rate, new_turn_acceleration)
        else:
            self.settings(STRAIGHT_SPEED_FAST, STRAIGHT_ACCELERATION, new_turn_rate, TURN_ACCELERATION)
            self.settings(STRAIGHT_SPEED_FAST, STRAIGHT_ACCELERATION, new_turn_rate, TURN_ACCELERATION)


    def settings(
            self,
            straight_speed,
            straight_acceleration,
            turn_rate,
            turn_acceleration):
        """
        Change the constants settings to new values.

        Arguments:
        :param straight_speed: New value for straight speed.
        :param straight_acceleration: New value for straight acceleration.
        :param turn_rate: New value for turn rate.
        :param turn_acceleration: New value for turn acceleration.
        """
        self.straight_speed = straight_speed
        self.straight_acceleration = straight_acceleration
        self.turn_rate = turn_rate
        self.turn_acceleration = turn_acceleration


    def change_input_output(
            self,
            left_motor: Motor,
            right_motor: Motor,
            gyro_sensor: GyroSensor):
        """
        Change the Motors and Sensors to new instances.

        :param left_motor: New left motor.
        :param right_motor: New right motor.
        :param gyro_sensor: New gyro sensor.
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        self.gyro_sensor = gyro_sensor


    def straight_gyro_with_condition(
            self, distance: int, condition_to_check
    ) -> bool:
        """straight(distance)

        Drives straight for a given distance and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Example use:
            precision_module.straight_gyro_with_condition(-500, (lambda: MindsStormUtil.tempBool(touche_sensor)))
            precision_module.straight_gyro_with_condition(-500, (lambda: touch_sensor.pressed()))

        Arguments:
            :param distance: Distance to travel in mm
            :param condition_to_check: Will continuously check this condition (please give as "lambda:") and abort if true
            :return bool: returns true when the method aborted due to the condition_to_check
        """
        min_speed = 50
        return_bool = condition_to_check

        self.drive_base.stop()
        self.drive_base.reset()
        self.gyro_sensor.reset_angle(0)

        PROPORTIONAL_GAIN = 1.1
        if distance < 0:  # move backwards
            while (self.drive_base.distance() > distance) and not return_bool():    #die klammern hinter return_bool sind essenziell!
                robotSpeed = min(
                    max(
                        (0.005 * self.straight_speed * abs(distance - self.drive_base.distance())),
                        min_speed),
                    self.straight_speed)
                reverseSpeed = -1 * robotSpeed
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(reverseSpeed, angle_correction)
                return_bool = condition_to_check
        elif distance > 0:  # move forwards
            while (self.drive_base.distance() < distance) and not return_bool():    #die klammern hinter return_bool sind essenziell!
                robotSpeed = min(
                    max(
                        (0.005 * self.straight_speed * abs(distance - self.drive_base.distance())),
                        min_speed),
                    self.straight_speed)
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(robotSpeed, angle_correction)
                return_bool = condition_to_check
        self.drive_base.stop()
        if return_bool():   #die klammern hinter return_bool sind essenziell!
            return True
        else:
            return False


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


    def turn_gyro_with_condition(
            self, angle: float,  condition_to_check
    ) -> bool:
        """turn(angle)

        Turns in place by a given angle and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            :param condition_to_check: Will continuously check this condition (please give as "lambda:") and abort if true
            :param angle: Angle of the turn in degree.
            :return bool: returns true when the method aborted due to the condition_to_check
        """
        min_speed = 50
        return_bool = condition_to_check

        # angle correction
        angle = angle * 1

        self.drive_base.stop()
        self.gyro_sensor.reset_angle(0)
        if angle < 0:
            while self.gyro_sensor.angle() > angle and not return_bool():   #die klammern hinter return_bool sind essenziell!
                speed = max((0.05 * self.turn_rate * abs(angle - self.gyro_sensor.angle())), min_speed)
                self.right_motor.run(speed=(-1 * speed))
                self.left_motor.run(speed=speed)
                return_bool = condition_to_check

        elif angle > 0:
            while self.gyro_sensor.angle() < angle and not return_bool():   #die klammern hinter return_bool sind essenziell!
                speed = max((0.05 * self.turn_rate * abs(angle - self.gyro_sensor.angle())), min_speed)
                self.right_motor.run(speed=speed)
                self.left_motor.run(speed=(-1 * speed))
                return_bool = condition_to_check

        self.right_motor.brake()
        self.left_motor.brake()
        if return_bool():   #die klammern hinter return_bool sind essenziell!
            return True
        else:
            return False


    def turn_gyro(
            self, angle: float
    ) -> None:
        """turn(angle)

        Turns in place by a given angle and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            :param angle: Angle of the turn in degree.
        """
        self.turn_gyro_with_condition(angle, lambda: False)