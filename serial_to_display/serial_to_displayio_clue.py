from adafruit_clue import clue
clue.display.bus.send(0x26, b"\x04")
import json
import gc
import time
import usb_cdc

clue.pixel[0] = (0,0,0)

"""
VIOLET          GREEN           RED
CYAN            ORANGE          BLUE            MAGENTA
SKY             YELLOW          PURPLE          color
TEAL            WHITE           BLACK           GOLD
PINK            AQUA            JADE            AMBER
RAINBOW
"""

def wheel(wheel_pos):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    wheel_pos = wheel_pos % 255
    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0

clue_display = clue.simple_text_display(
    text_scale = 3, colors = [ 0xFFFFFF ] * 9
)

# 9 lignes

def lights_toggle():
    clue.red_led = not clue.red_led
    clue.white_leds = not clue.white_leds

def every_x(delay):
    t0 = time.monotonic() + delay
    while True:
        t1 = time.monotonic()
        if t1 > t0:
            t0 = t1+delay
            yield True
        yield False


def parse_color(color):
    if isinstance(color, (list, tuple)) and len(color) == 3:
        return color
    if isinstance(color, int):
        return color
    if isinstance(color, str) and hasattr(clue, color.upper()):
        return getattr(clue, color.upper())


while True:
    if usb_cdc.data.in_waiting > 0:
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

        except ValueError as ex:
            print("Dropping json data", ex)


    pressed = clue.were_pressed
    if pressed:
        usb_cdc.data.write(json.dumps({
            "buttons": list(pressed)
        }).encode() + b"\r\n")

    clue_display.show()
    clue.red_led = not clue.red_led

    gc.collect()
    time.sleep(0.01)
