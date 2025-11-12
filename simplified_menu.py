#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.parameters import Button
from pybricks.tools import wait
from pybricks.media.ev3dev import Font

ev3 = EV3Brick()

# Display tuning
FONT_SIZE = 12
FONT = Font(size=FONT_SIZE)
ev3.screen.set_font(FONT)

LINE_H  = FONT_SIZE + 2     # line height
LIST_Y0 = 14                # first item y
TEXT_X  = 10                # text x
BAR_W   = 6                 # selection bar width

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

# Fake bold by drawing twice with 1-px offset
def draw_text_bold(x, y, text):
    ev3.screen.draw_text(x,     y, text)
    ev3.screen.draw_text(x + 1, y, text)

# --- Menu ---
def draw_menu(idx):
    ev3.screen.clear()
    ev3.screen.draw_text(0, 0, "Abschnitt waehlen:")

    for j, sec in enumerate(Section.ORDER):
        y = LIST_Y0 + j * LINE_H
        name = Section.NAMES[sec]

        if j == idx:
            # NOTE: pass 4 ints, not tuples
            ev3.screen.draw_box(0, y - 1, BAR_W, y + LINE_H - 3, fill=True)
            draw_text_bold(TEXT_X, y, "> " + name)
        else:
            ev3.screen.draw_text(TEXT_X, y, "  " + name)

    # footer (2 lines)
    footer_y = 128 - 2 * LINE_H  # EV3 vertical size ~128 px
    ev3.screen.draw_text(0, footer_y,          "Hoch/Runter: Auswahl")
    ev3.screen.draw_text(0, footer_y + LINE_H, "Enter: Start | Back: Ende")

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
        elif Button.CENTER in b:        # Enter = start
            wait_release(); return Section.ORDER[i]
        elif Button.BEACON in b:        # Use this as Back/Ende (if BACK not available)
            wait_release(); return None

# --- Section stub (for testing) ---
def run_section(sec):
    ev3.screen.clear()
    ev3.screen.print("Abschnitt:")
    ev3.screen.print(Section.NAMES[sec])
    ev3.screen.print("")
    ev3.screen.print("Enter: Menu")
    while True:
        wait(80)
        if Button.CENTER in ev3.buttons.pressed():
            wait_release()
            return

# --- Main loop ---
def main():
    current = menu_select(0)
    if current is None:
        ev3.screen.clear(); ev3.screen.print("Programm beendet."); return

    while True:
        run_section(current)
        current = menu_select(Section.ORDER.index(current))
        if current is None:
            ev3.screen.clear(); ev3.screen.print("Programm beendet."); break

main()
