import board
import displayio
import gc
import json
import microcontroller
import os
import terminalio
import time
import traceback
import usb_cdc
from adafruit_display_text.bitmap_label import Label
from adafruit_display_text import wrap_text_to_pixels

NUMLINES = 8
SCALE = 2

SERIAL = usb_cdc.console
if usb_cdc.data:
    SERIAL = usb_cdc.data

display = board.DISPLAY

display.auto_refresh = False
splash = displayio.Group()
line_height = terminalio.FONT.get_bounding_box()[1] * SCALE

colors = {
    "RED": (255, 0, 0),
    "YELLOW": (255, 255, 0),
    "ORANGE": (255, 150, 0),
    "GREEN": (0, 255, 0),
    "TEAL": (0, 255, 120),
    "CYAN": (0, 255, 255),
    "BLUE": (0, 0, 255),
    "PURPLE": (180, 0, 255),
    "MAGENTA": (255, 0, 150),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GOLD": (255, 222, 30),
    "PINK": (242, 90, 255),
    "AQUA": (50, 255, 255),
    "JADE": (0, 255, 40),
    "AMBER": (255, 100, 0),
    "VIOLET": (255, 0, 255),
    "SKY": (0, 180, 255),
}

labels = []
for y in range(NUMLINES):
    label = Label(
        text="", font=terminalio.FONT, color=0x0, scale=SCALE,
        anchored_position=(0, 1.25 * y * line_height), anchor_point=(0, 0),
    )
    labels.append(label)
    splash.append(label)

def show_the_lines(lines):
    for index, line in enumerate(lines[:len(labels)]):
        if line is not None:
            labels[index].text = line

def show_the_text(text):
    lines = wrap_text_to_pixels(text, font=terminalio.FONT, max_width=display.width / SCALE)
    show_the_lines(lines)

display.show(splash)

def parse_color(color):
    if isinstance(color, (list, tuple)) and len(color) == 3:
        return color
    if isinstance(color, int):
        return color
    if color in colors:
        return colors[color]
    return 0xFFFFFF

def read_serial():
    data_in = SERIAL.readline()
    try:
        print("Update", time.monotonic())
        data = json.loads(data_in)

        if "lines" in data:
            show_the_lines(data["lines"])

        if "colors" in data:
            for index, color in enumerate(data["colors"][:len(labels)]):
                labels[index].color = parse_color(color)

    except ValueError as ex:
        # traceback.print_exception(ex,ex,ex.__traceback__)
        print("Dropping json data:", ex)
        print(data_in)

    finally:
        gc.collect()
        display.refresh()


while True:
    if SERIAL.in_waiting > 0:
        read_serial()

    time.sleep(0.01)
