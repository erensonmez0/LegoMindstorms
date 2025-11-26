from pybricks.ev3devices import TouchSensor
from pybricks.robotics import DriveBase
from time import sleep




class Bridge:
    RAMP_UP = 1000
    TURN_LEFT = 90
    TURN_RIGHT = -90
    BRIDGE_LENGTH = 1250
    RAMP_DOWN = 1000

    ALIGN = -15
    DISTANCE_TO_BRIDGE_START = 280


     
    def __init__(self, drive_base:DriveBase, touche_sensor:TouchSensor):
        self.drive_base = drive_base
        self.touch_sensor = touche_sensor


    # TODO auslagern in extra util class
    def align_start(self):
        self.drive_base.straight(-150)
        self.drive_base.turn(self.TURN_RIGHT)
        self.drive_base.straight(- (self.DISTANCE_TO_BRIDGE_START - 50))

        # drive backwards until touching the wall or max_counter of cm
        max_counter = 20
        while (not self.touch_sensor.pressed()) or (max_counter <= 0):
            self.drive_base.straight(self.ALIGN)
            sleep(1)
            max_counter = max_counter - 1

        # drive to startpoint of ramp
        self.drive_base.straight(self.DISTANCE_TO_BRIDGE_START)
        self.drive_base.turn(self.TURN_LEFT)


        
    def drive_bridge(self):
        self.drive_base.straight(self.RAMP_UP)
        self.drive_base.turn(self.TURN_LEFT)
        self.drive_base.straight(self.BRIDGE_LENGTH)
        self.drive_base.turn(self.TURN_LEFT)
        self.drive_base.straight(self.RAMP_DOWN)

    def run(self):
        # TODO bridge ablauf
        self.align_start()
        # self.drive_bridge()








