from adafruit_clue import clue
clue.display.bus.send(0x26, b"\x04")
import json
import gc
import time
import usb_cdc
# from _pixelbuff import colorwheel as wheel

clue.pixel[0] = (0,0,0)

"""
VIOLET          GREEN           RED
CYAN            ORANGE          BLUE            MAGENTA
SKY             YELLOW          PURPLE          color
TEAL            WHITE           BLACK           GOLD
PINK            AQUA            JADE            AMBER
RAINBOW
"""

clue_display = clue.simple_text_display(
    text_scale = 3, colors = [ 0xFFFFFF ] * 9
)

# scale 3 -> 6 lines


def parse_color(color):
    if isinstance(color, (list, tuple)) and len(color) == 3:
        return color
    if isinstance(color, int):
        return color
    if isinstance(color, str) and hasattr(clue, color.upper()):
        return getattr(clue, color.upper())
    return 0xFFFFFF


def read_serial():
    data_in = usb_cdc.data.readline()
    try:
        print("Update", time.monotonic())
        data = json.loads(data_in)

        if "lines" in data:
            for index, line in enumerate(data["lines"]):
                if index in range(0,9) and line is not None:
                    clue_display[index].text = line

        if "colors" in data:
            for index, color in enumerate(data["colors"]):
                if index in range(0,9) and color is not None:
                    clue_display[index].color = parse_color(color)

        clue_display.show()

    except ValueError as ex:
        print("Dropping json data:", ex)
        print(data_in)

    finally:
        gc.collect()


while True:
    if usb_cdc.data.in_waiting > 0:
        read_serial()

    pressed = clue.were_pressed
    if pressed:
        print(pressed)
        usb_cdc.data.write(json.dumps({
            "buttons": list(pressed)
        }).encode() + b"\r\n")

    clue.red_led = not clue.red_led

    time.sleep(0.01)
