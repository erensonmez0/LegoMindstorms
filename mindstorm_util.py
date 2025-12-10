from pybricks.ev3devices import TouchSensor, ColorSensor


class MindsStormUtil:

    @staticmethod
    def check_touch_sensor(touch_sensor:TouchSensor) -> bool:
        return touch_sensor.pressed()


    @staticmethod
    def check_color(color_sensor:ColorSensor, color_value:tuple[int, int, int]) -> bool:
        threshold = 4
        return ((-threshold < (color_sensor.rgb()[0] - color_value[0]) < threshold)
                and (-threshold < (color_sensor.rgb()[1] - color_value[1]) < threshold)
                and (-threshold < (color_sensor.rgb()[2] - color_value[2]) < threshold))

