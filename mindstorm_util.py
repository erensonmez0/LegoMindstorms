from time import sleep

from pybricks.ev3devices import TouchSensor, ColorSensor

from precision_module import PrecisionModule


class MindsStormUtil:

    @staticmethod
    def drive_backwards_till_wall(precision_module:PrecisionModule, touch_sensor:TouchSensor, max_mm:float) -> bool:
        """
        drive backwards until touching the wall or max_counter of cm
        :param precision_module: Module to use for precisely drive backwards
        :param touch_sensor: Sensor to determine contact with wall
        :param max_mm: Maximal amount of mm before aborting and returning false
        :return: Returns true if wall was reached, false if max_cm was reached
        """
        ALIGN_BACKWARDS = -1                  # half a cm
        max_counter = max_mm / -ALIGN_BACKWARDS
        while True:
            if touch_sensor.pressed():
                return True
            if max_counter <= 0:
                return False
            precision_module.straight_gyro(ALIGN_BACKWARDS)
            sleep(0.5)
            max_counter = max_counter - 1


    @staticmethod
    def drive_forwards_till_color(precision_module: PrecisionModule, color_sensor: ColorSensor, color_value:tuple[int, int, int], max_mm: float) -> bool:
        """
        drive backwards until touching the wall or max_counter of cm
        :param precision_module: Module to use for precisely drive backwards
        :param color_sensor: Sensor to determine abort condition
        :param color_value: Color value to stop at
        :param max_mm: Maximal amount of mm before aborting and returning false
        :return: Returns true if color was found, false if max_cm was reached
        """
        ALIGN_FORWARDS = 1
        max_counter = max_mm / ALIGN_FORWARDS
        while True:
            # print(color_sensor.rgb())
            # print(color_value)
            if ((-4 < (color_sensor.rgb()[0] - color_value[0]) < 4)
                    and (-4 < (color_sensor.rgb()[1] - color_value[1]) < 4)
                    and (-4 < (color_sensor.rgb()[2] - color_value[2]) < 4)):
                return True
            if max_counter <= 0:
                return False
            precision_module.straight_gyro(ALIGN_FORWARDS)
            sleep(0.5)
            max_counter = max_counter - 1


