from pybricks.robotics import DriveBase


class Bridge:
    RAMP_UP = 1000
    TURN = 90
    BRIDGE_LENGTH = 1250
    RAMP_DOWN = 1000
     
    def __init__(self, drive_base:DriveBase):
        self.drive_base = drive_base

    def run(self):
        self.drive_base.straight(self.RAMP_UP)
        self.drive_base.turn(self.TURN)
        self.drive_base.straight(self.BRIDGE_LENGTH)
        self.drive_base.turn(self.TURN)
        self.drive_base.straight(self.RAMP_DOWN)
        
        


