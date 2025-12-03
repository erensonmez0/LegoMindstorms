from pybricks.ev3devices import TouchSensor, ColorSensor

from mindstorm_util import MindsStormUtil
from precision_module import PrecisionModule


class Bridge:
    RAMP_UP = 1000
    TURN_LEFT = 90
    TURN_RIGHT = -90
    BRIDGE_LENGTH = 1250
    RAMP_DOWN = 1000

    DISTANCE_TO_BRIDGE_START = 280

    BLUE = 6


     
    def __init__(self, precision_module:PrecisionModule, touche_sensor:TouchSensor, color_sensor:ColorSensor):
        self.precision_module = precision_module
        self.touch_sensor = touche_sensor
        self.color_sensor = color_sensor


    def align_start(self):
        self.precision_module.straight_gyro(-200)
        self.precision_module.turn_gyro(self.TURN_RIGHT)
        self.precision_module.straight_gyro(- (self.DISTANCE_TO_BRIDGE_START - 50))


        MindsStormUtil.drive_backwards_till_wall(self.precision_module, self.touch_sensor, 70)

        # drive to startpoint of ramp
        self.precision_module.straight_gyro(self.DISTANCE_TO_BRIDGE_START)
        self.precision_module.turn_gyro(self.TURN_LEFT)

        MindsStormUtil.drive_forwards_till_color(self.precision_module, self.color_sensor, self.BLUE, 50)


        
    def drive_bridge(self):
        self.precision_module.straight_gyro(self.RAMP_UP)
        self.precision_module.turn_gyro(self.TURN_LEFT)
        self.precision_module.straight_gyro(self.BRIDGE_LENGTH)
        self.precision_module.turn_gyro(self.TURN_LEFT)
        self.precision_module.straight_gyro(self.RAMP_DOWN)

    def run(self):
        self.align_start()
        self.drive_bridge()








