#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, GyroSensor, ColorSensor, UltrasonicSensor, TouchSensor
from pybricks.parameters import Port, Button
from pybricks.robotics import DriveBase
from pybricks.tools import wait
from pybricks.media.ev3dev import Font
from time import sleep

from bridge import Bridge
from precision_module import PrecisionModule
from line_follower import LineFollower
from color_field import ColorField
from pringler import Pringler
from bridge import Bridge
from config import WHITE, BROWN, BLUE, RED  # Import colors from config

# ---------------------- Hardware setup ----------------------
ev3 = EV3Brick()

left_motor = Motor(Port.B)
right_motor = Motor(Port.C)
motor = Motor(Port.D)
wheel_diameter = 33
axle_track = 160
drive_base = DriveBase(left_motor, right_motor, wheel_diameter, axle_track)

straight_speed = 200
straight_acceleration = 200
turn_rate = 120
turn_acceleration = 120

drive_base.settings(straight_speed, straight_acceleration, turn_rate, turn_acceleration)

color_sensor = ColorSensor(Port.S2)                     # used for band detection
ultrasonic_sensor = UltrasonicSensor(Port.S4)           # used for obstacle detection
gyro_sensor  = GyroSensor(Port.S1)                      # used for navigation via drive_base
touch_sensor = TouchSensor(Port.S3)                   # used for wall alignment?


# Create precision module
precision_module = PrecisionModule(
    left_motor,
    right_motor,
    drive_base,
    straight_speed,
    straight_acceleration,
    turn_rate,
    turn_acceleration,
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
    LINE_FOLLOW, PRINGLER, BRIDGE, COLOR_FIELD, EXIT = range(5)
    ORDER = [LINE_FOLLOW, PRINGLER, BRIDGE, COLOR_FIELD, EXIT]
    NAMES = {
        LINE_FOLLOW: "Linienfolgen",
        PRINGLER: "Pringler",
        BRIDGE: "Brücke",
        COLOR_FIELD: "Farbfeldsuche",
        EXIT: "Beenden",
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
        elif Button.DOWN in b:
            i = (i + 1) % len(Section.ORDER)
            wait_release()
        elif Button.CENTER in b:
            wait_release()
            return Section.ORDER[i]

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
            color_sensor=color_sensor
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
    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return

# ---------------------- Main Loop ----------------------
def main():
    current = menu_select(0)
    
    while True:
        if current == Section.EXIT:
            ev3.screen.clear()
            ev3.screen.print("Programm beendet.")
            break
        elif current == Section.LINE_FOLLOW:
            run_line_follow()
            current = menu_select(Section.ORDER.index(Section.LINE_FOLLOW))
        elif current == Section.PRINGLER:
            run_pringler()
            current = menu_select(Section.ORDER.index(Section.PRINGLER))
        elif current == Section.BRIDGE:
            run_bridge()
            current = menu_select(Section.ORDER.index(Section.BRIDGE))
        elif current == Section.COLOR_FIELD:
            run_color_field()
            current = menu_select(Section.ORDER.index(Section.COLOR_FIELD))


main()
# color_field = ColorField(drive_base, color_sensor, ultrasonic_sensor, touch_sensor,)
#  color_field.run()

# TODO
#   - precision_module testen
#   - menu einbinden
#   - neu kalibrieren (gewicht verschieben?)
#   - greifarm aktuieren
#   - brücke
#   - linien folgen
#   - farbfinden
#   - pringler
#

# TODO Cornelius
#   - combine straight_gyro with abort condition (e.g. color_sensor, touche_sensor -> bool expression)
#   -


