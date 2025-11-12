#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait

ev3 = EV3Brick()

# --- Enum substitute ---
class Section:
    LINE_FOLLOW, COLOR_FIELD, PUSH_CYLINDER, BRIDGE = range(4)
    ORDER = [LINE_FOLLOW, COLOR_FIELD, PUSH_CYLINDER, BRIDGE]
    NAMES = {
        LINE_FOLLOW:   "Linienfolgen",
        COLOR_FIELD:   "Farbfeldsuche",
        PUSH_CYLINDER: "Zylinder verschieben",
        BRIDGE:        "Bruecke",
    }

def wait_release():
    while ev3.buttons.pressed():
        wait(20)

# --- Menu ---
def draw_menu(idx):
    ev3.screen.clear()
    ev3.screen.print("Abschnitt waehlen:")
    ev3.screen.print("> " + Section.NAMES[Section.ORDER[idx]])
    ev3.screen.print("")
    ev3.screen.print("Hoch/Runter: Auswahl")
    ev3.screen.print("Enter: Start | Back: Ende")

def menu_select(initial=0):
    i = initial
    wait_release()
    while True:
        draw_menu(i)
        wait(120)
        b = ev3.buttons.pressed()
        if Button.UP in b:
            i = (i - 1) % len(Section.ORDER); wait_release()
        elif Button.DOWN in b:
            i = (i + 1) % len(Section.ORDER); wait_release()
        elif Button.CENTER in b:   # Start chosen section
            wait_release(); return Section.ORDER[i]
        elif Button.BACKSPACE in b:      # Enter in menu = end program
            wait_release(); return None

# --- Section stub (for testing) ---
def run_section(sec):
    ev3.screen.clear()
    ev3.screen.print("Abschnitt:")
    ev3.screen.print(Section.NAMES[sec])
    ev3.screen.print("")
    ev3.screen.print("Enter: Menu")
    # Wait until ENTER pressed -> back to menu
    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return  # return to menu

# --- Main loop ---

def main():
    current = menu_select(0)
    if current is None:
        ev3.screen.clear(); ev3.screen.print("Programm beendet."); return

    while True:
        run_section(current)  # just shows text until Enter
        # after section, go back to menu (Enter there ends program)
        current = menu_select(Section.ORDER.index(current))
        if current is None:
            ev3.screen.clear(); ev3.screen.print("Programm beendet."); break

main()
