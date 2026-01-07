#!/usr/bin/env pybricks-micropython
import time

from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.hubs import EV3Brick
from pybricks.media.ev3dev import Font
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait

from bridge import Bridge
from color_field import ColorField
from config import *
from line_follower import LineFollower
from precision_module import PrecisionModule
from pringler import Pringler
from debug_test import DebugTest


# ---------------------- Hardware setup ----------------------
ev3 = EV3Brick()

#Setup Motors
left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
motor = Motor(Port.D)

# Setup Drive base
drive_base = DriveBase(left_motor, right_motor, WHEEL_DIAMETER, AXLE_TRACK)
drive_base.settings(STRAIGHT_SPEED_FAST, STRAIGHT_ACCELERATION, TURN_RATE, TURN_ACCELERATION)

# Setup Sensors
color_sensor = ColorSensor(Port.S2)                     # used for band detection
ultrasonic_sensor = UltrasonicSensor(Port.S4)           # used for obstacle detection
gyro_sensor  = GyroSensor(Port.S1)                      # used for navigation via drive_base
touch_sensor = TouchSensor(Port.S3)                     # used for wall alignment

# Setup precision module
precision_module = PrecisionModule(
    left_motor,
    right_motor,
    drive_base,
    STRAIGHT_SPEED_FAST,
    STRAIGHT_ACCELERATION,
    TURN_RATE,
    TURN_ACCELERATION,
    gyro_sensor
)


# ---------------------- Menu Setup ----------------------
FONT_SIZE = 12
FONT = Font(size=FONT_SIZE)
ev3.screen.set_font(FONT)

LINE_H = FONT_SIZE + 2
LIST_Y0 = 14
TEXT_X = 10
BAR_W = 6


class Section:
    LINE_FOLLOW, PRINGLER, BRIDGE, COLOR_FIELD, DEBUG, RUN_COURSE, EXIT = range(7)
    ORDER = [ DEBUG,LINE_FOLLOW, PRINGLER, BRIDGE, COLOR_FIELD, RUN_COURSE, EXIT]
    NAMES = {
        DEBUG: "Debug",
        LINE_FOLLOW: "Linienfolgen",
        PRINGLER: "Pringler",
        BRIDGE: "Brücke",
        COLOR_FIELD: "Farbfeldsuche",
        RUN_COURSE: "Run Course",
        EXIT: "Beenden"
    }

def wait_release():
    while ev3.buttons.pressed():
        wait(20)

def draw_text_bold(x, y, text):
    ev3.screen.draw_text(x, y, text)
    ev3.screen.draw_text(x + 1, y, text)

def draw_menu(idx):
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Abschnitt waehlen:")

    for j, sec in enumerate(Section.ORDER):
        y = LIST_Y0 + j * LINE_H
        name = Section.NAMES[sec]

        if j == idx:
            ev3.screen.draw_box(0, y - 1, BAR_W, y + LINE_H - 3, fill=True)
            draw_text_bold(TEXT_X, y, "> " + name)
        else:
            ev3.screen.draw_text(TEXT_X, y, "  " + name)

    footer_y = 128 - 2 * LINE_H
    ev3.screen.draw_text(0, footer_y, "Hoch/Runter: Auswahl")
    ev3.screen.draw_text(0, footer_y + LINE_H, "Enter: Start")

def menu_select(initial=0):
    i = initial
    wait_release()
    while True:
        draw_menu(i)
        wait(120)
        b = ev3.buttons.pressed()
        if Button.UP in b:
            i = (i - 1) % len(Section.ORDER)
            wait_release()
            wait(50)

        elif Button.DOWN in b:
            i = (i + 1) % len(Section.ORDER)
            wait_release()
            wait(50)

        elif Button.CENTER in b:
            wait_release()
            return Section.ORDER[i]
        
        elif Button.LEFT in b:
            wait_release()
            return None

# ---------------------- Section Runners ----------------------
def run_line_follow():
    ev3.screen.clear()
    ev3.screen.print("Linienfolgen")
    ev3.screen.print("Starting...")
    
    try:
        line_follower = LineFollower(
            drive_base=drive_base,
            color_sensor=color_sensor,
            ultrasonic_sensor=ultrasonic_sensor
        )
        line_follower.run()
    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error:")
        ev3.screen.print(str(e))
        wait(3000)
    
    ev3.screen.clear()
    ev3.screen.print("Fertig!")
    ev3.screen.print("Enter: Menu")

    wait_release()
    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return

def run_pringler():
    ev3.screen.clear()
    ev3.screen.print("Pringler")
    ev3.screen.print("Starting...")
    
    try:
        pringler = Pringler(
            drive_base=drive_base,
            arm_motor=motor,
            color_sensor=color_sensor,
            ultrasonic_sensor=ultrasonic_sensor,
            precision_module=precision_module,
            touch_sensor=touch_sensor
        )
        pringler.run()
    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error:")
        ev3.screen.print(str(e))
        wait(3000)
    
    ev3.screen.clear()
    ev3.screen.print("Fertig!")
    ev3.screen.print("Enter: Menu")
    wait_release()

    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return
        
def run_bridge():
    ev3.screen.clear()
    ev3.screen.print("Brücke")
    ev3.screen.print("Starting...")
    
    try:
        bridge = Bridge(
            precision_module=precision_module,
            touche_sensor=touch_sensor,
            color_sensor=color_sensor
        )
        bridge.run()
    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error:")
        ev3.screen.print(str(e))
        wait(3000)
    
    ev3.screen.clear()
    ev3.screen.print("Fertig!")
    ev3.screen.print("Enter: Menu")
    wait_release()

    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return
        
def run_color_field():
    ev3.screen.clear()
    ev3.screen.print("Farbfeldsuche")
    ev3.screen.print("Starting...")
    
    try:
        color_field = ColorField(
            drive_base=drive_base,
            color_sensor=color_sensor,
            ultrasonic_sensor=ultrasonic_sensor,
            touch_sensor=touch_sensor,
            precision_module=precision_module
        )
        color_field.run()
    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error:")
        ev3.screen.print(str(e))
        wait(3000)
    
    ev3.screen.clear()
    ev3.screen.print("Fertig!")
    ev3.screen.print("Enter: Menu")

    wait_release()

    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return
        
def run_debug_callibration():
    ev3.screen.clear()
    ev3.screen.print("Debug")
    ev3.screen.print("Starting...")
    
    try:
        debug_test = DebugTest(
            drive_base=drive_base,
            arm_motor=motor,
            color_sensor=color_sensor,
            ultrasonic_sensor=ultrasonic_sensor,
            precision_module=precision_module,
            touch_sensor=touch_sensor
        )
        debug_test.run()
    except Exception as e:
        ev3.screen.clear()
        ev3.screen.print("Error:")
        ev3.screen.print(str(e))
        wait(3000)
    
    ev3.screen.clear()
    ev3.screen.print("Fertig!")
    ev3.screen.print("Enter: Menu")

    wait_release()
    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return

# ---------------------- Main Loop ----------------------
def main():
    current = menu_select(0)

    if current is None:  # LEFT button pressed in menu
        ev3.screen.clear()
        ev3.screen.print("Programm beendet.")
        return
    
    while True:
        if current == Section.EXIT:
            ev3.screen.clear()
            ev3.screen.print("Programm beendet.")
            break
        elif current == Section.DEBUG:
            run_debug_callibration()
        elif current == Section.LINE_FOLLOW:
            run_line_follow()
        elif current == Section.PRINGLER:
            run_pringler()
        elif current == Section.BRIDGE:
            run_bridge()
        elif current == Section.COLOR_FIELD:
            run_color_field()
        elif current == Section.RUN_COURSE:
            ev3.screen.print("Following Line")
            run_line_follow()
            ev3.screen.print("Pringling")
            run_pringler()
            ev3.screen.print("Bridge")
            run_bridge()
            ev3.screen.print("Color Field")
            run_color_field()



        current = menu_select(Section.ORDER.index(current))

        if current is None:  # LEFT button pressed in menu
            ev3.screen.clear()
            ev3.screen.print("Programm beendet.")
            break


main()



# TODO
#   - farbfinden -> anfang
#   - pringler  -> greifen
#   - Übergang brücke farbfeld
#
