from time import sleep

from pybricks.ev3devices import TouchSensor, ColorSensor

from main import BLUE
from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule


class Bridge:
    RAMP_UP = 1000
    TURN_LEFT = -90
    TURN_RIGHT = 90
    BRIDGE_LENGTH = 1250
    RAMP_DOWN = 1000

    DISTANCE_TO_BRIDGE_START = 280

     
    def __init__(self, precision_module:PrecisionModule, touche_sensor:TouchSensor, color_sensor:ColorSensor):
        self.precision_module = precision_module
        self.touch_sensor = touche_sensor
        self.color_sensor = color_sensor


    def align_start(self):
        self.precision_module.straight_gyro(-100)
        self.precision_module.turn_gyro(self.TURN_RIGHT)

        # drive backwards till touching the wall
        self.precision_module.straight_gyro_with_condition(-300, lambda:(self.touch_sensor.pressed()))

        # drive to startpoint of ramp
        self.precision_module.straight_gyro(self.DISTANCE_TO_BRIDGE_START)
        self.precision_module.turn_gyro(self.TURN_LEFT)

        self.precision_module.straight_gyro_with_condition(300, lambda:MindsStormUtil.check_color(self.color_sensor, BLUE))


        
    def drive_bridge(self):
        self.precision_module.straight_gyro(self.RAMP_UP)
        self.precision_module.turn_gyro(self.TURN_LEFT)
        self.precision_module.straight_gyro(self.BRIDGE_LENGTH)
        self.precision_module.turn_gyro(self.TURN_LEFT)
        self.precision_module.straight_gyro(self.RAMP_DOWN)

    def run(self):
        self.align_start()
        sleep(5)
        self.drive_bridge()








