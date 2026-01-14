from pybricks.ev3devices import TouchSensor, ColorSensor
import math


class MindsStormUtil:

    @staticmethod
    def check_touch_sensor(touch_sensor:TouchSensor) -> bool:
        return touch_sensor.pressed()


    @staticmethod
    def check_color(color_sensor:ColorSensor, color_value:tuple[int, int, int], threshold=10) -> bool:
        """
        Check if the given color_value is close to the color given by the color sensor.
        :param threshold: optional input to use a different threshold for the color matching.
        :param color_sensor: Color sensor to use
        :param color_value: Color value to compare to
        :return: True if values are close to color, False otherwise
        """
        return ((-threshold < (color_sensor.rgb()[0] - color_value[0]) < threshold)
                and (-threshold < (color_sensor.rgb()[1] - color_value[1]) < threshold)
                and (-threshold < (color_sensor.rgb()[2] - color_value[2]) < threshold))
    
    
    @staticmethod
    def check_color_euclid(color_sensor:ColorSensor, color_value:tuple[int, int, int], threshold=10) -> bool:
        """
        Check if the given color_value is close to the color given by the color sensor.
        :param threshold: optional input to use a different threshold for the color matching.
        :param color_sensor: Color sensor to use
        :param color_value: Color value to compare to
        :return: True if values are close to color, False otherwise
        """
        return (math.sqrt((color_sensor.rgb()[0] - color_value[0])**2
                          + (color_sensor.rgb()[1] - color_value[1])**2
                          + (color_sensor.rgb()[2] - color_value[2])**2)
                < threshold)
               
