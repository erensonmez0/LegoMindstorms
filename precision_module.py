#!/usr/bin/env pybricks-micropython
from time import sleep

from pybricks.ev3devices import Motor, GyroSensor
from pybricks.robotics import DriveBase


class PrecisionModule:

    def __init__(
            self,
            left_motor: Motor,
            right_motor: Motor,
            # wheel_diameter: Number,
            # axle_track: Number,
            drive_base: DriveBase,
            straight_speed,
            straight_acceleration,
            turn_rate,
            turn_acceleration,
            gyro_sensor: GyroSensor,
    ):
        """PrecisionModule(left_motor, right_motor, wheel_diameter, axle_track, gyro_sensor)

        Arguments:
            left_motor (Motor):
                The motor that drives the left wheel.
            right_motor (Motor):
                The motor that drives the right wheel.
            drive_base {DriveBase}: Given drive base to operate on.
            straight_speed (Number, mm): Speed when going straight.
            straight_acceleration (Number, mm): Acceleration when going straight.
            turn_rate (Number, mm): Speed when turning.
            turn_acceleration (Number, mm): Acceleration when turning.
            gyro_sensor (GyroSensor): Gyro sensor to measure angles and distances.
        """
        self.left_motor = left_motor
        self.right_motor = right_motor
        # self.wheel_diameter = wheel_diameter
        # self.axle_track = axle_track
        self.drive_base = drive_base
        self.straight_speed = straight_speed
        self.straight_acceleration = straight_acceleration
        self.turn_rate = turn_rate
        self.turn_acceleration = turn_acceleration
        self.gyro_sensor = gyro_sensor




    def straight_gyro(
            self, distance: int
    ) -> None:
        """straight(distance)

        Drives straight for a given distance and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            distance (Number, mm): Distance to travel
        """

        robotSpeed = self.straight_speed

        self.drive_base.reset()
        self.gyro_sensor.reset_angle(0)

        PROPORTIONAL_GAIN = 1.1
        if distance < 0:  # move backwards
            while self.drive_base.distance() > distance:
                # print(self.gyro_sensor.angle())
                reverseSpeed = -1 * robotSpeed
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(reverseSpeed, angle_correction)
                sleep(0.1)
        elif distance > 0:  # move forwards
            while self.drive_base.distance() < distance:
                # print(self.gyro_sensor.angle())
                angle_correction = 1 * PROPORTIONAL_GAIN * self.gyro_sensor.angle()
                self.drive_base.drive(robotSpeed, angle_correction)
                sleep(0.1)
        self.drive_base.stop()



    def turn_gyro(
            self, angle: int
    ) -> None:
        """turn(angle)

        Turns in place by a given angle and then stops.
        Accuracy is increased by unsing the gyro sensor.

        Arguments:
            angle (Number, deg): Angle of the turn.
        """
        # speed = 150  # mm/s
        speed = self.turn_rate

        self.gyro_sensor.reset_angle(0)
        if angle < 0:
            while self.gyro_sensor.angle() > angle:
                # print(self.gyro_sensor.angle())
                self.right_motor.run(speed=(-1 * speed))
                self.left_motor.run(speed=speed)
                # wait(10)
                sleep(0.1)
        elif angle > 0:
            while self.gyro_sensor.angle() < angle:
                # print(self.gyro_sensor.angle())
                self.right_motor.run(speed=speed)
                self.left_motor.run(speed=(-1 * speed))
                # wait(10)
                sleep(0.1)
        # else:
            # print("Error: no angle chosen")

        self.right_motor.brake()
        self.left_motor.brake()






