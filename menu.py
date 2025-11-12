#!/usr/bin/env pybricks-micropython
# EV3: State-machine framework with menu, color-band transitions, and reusable skills

from pybricks.hubs import EV3Brick
from pybricks.ev3devices import Motor, ColorSensor, UltrasonicSensor, GyroSensor
from pybricks.parameters import Port, Button, Color
from pybricks.robotics import DriveBase
from pybricks.tools import wait

# ---------------------- Hardware setup ----------------------
ev3 = EV3Brick()
left_motor  = Motor(Port.B)   # adjust to your wiring
right_motor = Motor(Port.C)
robot = DriveBase(left_motor, right_motor, wheel_diameter=33.25, axle_track=160)
robot.settings(200, 200, 120, 120)

color = ColorSensor(Port.S1)        # used for band detection
ultra = UltrasonicSensor(Port.S2)   # optional
gyro  = GyroSensor(Port.S3)         # optional

# ---------------------- Enum substitute ----------------------
class Section:
    LINE_FOLLOW     = 0
    COLOR_FIELD     = 1
    PUSH_CYLINDER   = 2
    BRIDGE          = 3

    NAMES = {
        LINE_FOLLOW:   "Linienfolgen",
        COLOR_FIELD:   "Farbfeldsuche",
        PUSH_CYLINDER: "Zylinder verschieben",
        BRIDGE:        "Brücke",
    }

    ORDER = [LINE_FOLLOW, COLOR_FIELD, PUSH_CYLINDER, BRIDGE]

    @staticmethod
    def next_of(cur):
        idx = Section.ORDER.index(cur)
        return Section.ORDER[(idx + 1) % len(Section.ORDER)]

# ---------------------- Config & helpers ----------------------
# Define which band colors mark the end of each section (tune to your track)
BAND_OF_SECTION = {
    Section.LINE_FOLLOW:   Color.RED,
    Section.COLOR_FIELD:   Color.BLUE,
    Section.PUSH_CYLINDER: Color.GREEN,
    Section.BRIDGE:        Color.YELLOW,
}

def pressed_enter() -> bool:
    return Button.CENTER in ev3.buttons.pressed()

def any_button() -> bool:
    return len(ev3.buttons.pressed()) > 0

def wait_button_release():
    # Debounce: wait until no button is pressed
    while any_button():
        wait(20)

# --------- Reusable "skills" (keep section-agnostic) ---------
def drive_mm(mm, speed=200):
    old = robot.settings()
    robot.settings(speed, speed, old[2], old[3])
    robot.straight(mm)
    robot.settings(*old)

def turn_deg(deg, rate=120):
    old = robot.settings()
    robot.settings(old[0], old[1], rate, rate)
    robot.turn(deg)
    robot.settings(*old)

def follow_line_step(target_reflection=30, kp=1.2, base_speed=140):
    """
    Simple proportional line follow step using reflection (black/white contrast).
    Call repeatedly in a loop.
    """
    ref = color.reflection()
    error = target_reflection - ref
    steer = kp * error
    robot.drive(base_speed, steer)

def saw_band(section) -> bool:
    """
    Detect the colored band that ends the current section.
    You can use color.color() or thresholds on reflection.
    """
    band = BAND_OF_SECTION.get(section, None)
    if band is None:
        return False
    return color.color() == band

# ---------------------- Menu ----------------------
def draw_menu(idx):
    ev3.screen.clear()
    ev3.screen.print("Abschnitt waehlen:")
    ev3.screen.print("> " + Section.NAMES[Section.ORDER[idx]])
    ev3.screen.print("")
    ev3.screen.print("Links/Rechts: Auswahl")
    ev3.screen.print("Back: Start  | Enter: Ende")

def menu_select(initial=0):
    idx = initial
    wait_button_release()
    while True:
        draw_menu(idx)
        wait(150)
        btns = ev3.buttons.pressed()

        if Button.LEFT in btns:
            idx = (idx - 1) % len(Section.ORDER)
            wait_button_release()
        elif Button.RIGHT in btns:
            idx = (idx + 1) % len(Section.ORDER)
            wait_button_release()
        elif Button.CENTER in btns:  # Start
            wait_button_release()
            return Section.ORDER[idx]
        elif Button.BACKSPACE in btns:  # Quit program from menu
            wait_button_release()
            return None

# ---------------------- Sections (return next section) ----------------------
def run_line_follow():
    ev3.screen.clear(); ev3.screen.print("Abschnitt: Linienfolgen")
    wait(300)

    # DEMO LOOP: replace with your real line follower
    while True:
        if pressed_enter():  # global emergency exit
            return None
        # Follow line
        follow_line_step()
        wait(10)
        # Transition?
        if saw_band(Section.LINE_FOLLOW):
            robot.stop()
            ev3.screen.print("Band erkannt: Rot -> weiter")
            wait(500)
            return Section.next_of(Section.LINE_FOLLOW)

def run_color_field():
    ev3.screen.clear(); ev3.screen.print("Abschnitt: Farbfeldsuche")
    wait(300)

    # DEMO: drive slowly and “scan”
    robot.drive(80, 0)
    while True:
        if pressed_enter():
            robot.stop(); return None
        # Your color-field logic here (find target color, center, etc.)
        if saw_band(Section.COLOR_FIELD):
            robot.stop()
            ev3.screen.print("Band erkannt: Blau -> weiter")
            wait(500)
            return Section.next_of(Section.COLOR_FIELD)
        wait(10)

def run_push_cylinder():
    ev3.screen.clear(); ev3.screen.print("Abschnitt: Zylinder verschieben")
    wait(300)

    # DEMO: approach + push (replace with your gripper or pushing code)
    drive_mm(300, speed=150)
    # TODO: use ultrasonics/limit switch to confirm contact, then push further
    drive_mm(150, speed=100)

    # Wait for band
    while True:
        if pressed_enter(): return None
        if saw_band(Section.PUSH_CYLINDER):
            ev3.screen.print("Band erkannt: Gruen -> weiter")
            wait(500)
            return Section.next_of(Section.PUSH_CYLINDER)
        wait(10)

def run_bridge():
    ev3.screen.clear(); ev3.screen.print("Abschnitt: Bruecke")
    wait(300)

    # DEMO: careful drive; replace with your slope logic (gyro)
    drive_mm(400, speed=120)
    # TODO: use gyro angle/speed to detect slope up/down and end of bridge

    while True:
        if pressed_enter(): return None
        if saw_band(Section.BRIDGE):
            ev3.screen.print("Band erkannt: Gelb -> zurueck")
            wait(500)
            return Section.next_of(Section.BRIDGE)
        wait(10)

# ---------------------- Main loop ----------------------
def main():
    # 1) Choose entry section from menu (can “reset” to any section)
    current = menu_select(initial=0)
    if current is None:
        ev3.screen.clear(); ev3.screen.print("Programm beendet."); return

    # 2) State machine: run sections until ENTER pressed
    while True:
        if current == Section.LINE_FOLLOW:
            nxt = run_line_follow()
        elif current == Section.COLOR_FIELD:
            nxt = run_color_field()
        elif current == Section.PUSH_CYLINDER:
            nxt = run_push_cylinder()
        elif current == Section.BRIDGE:
            nxt = run_bridge()
        else:
            nxt = None

        # ENTER anywhere = exit
        if nxt is None:
            ev3.screen.clear(); ev3.screen.print("Programm beendet."); break

        # After each section, go back to menu or auto-continue — your choice:
        # Option A: auto-continue:
        # current = nxt

        # Option B (recommended): go back to menu so tutors can jump around:
        current = menu_select(initial=Section.ORDER.index(nxt))
        if current is None:
            ev3.screen.clear(); ev3.screen.print("Programm beendet."); break

main()
