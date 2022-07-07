import board
import displayio
import microcontroller
import terminalio
import time
from adafruit_display_text.bitmap_label import Label

display = board.DISPLAY
splash = displayio.Group()

title_label = Label(
    text="My Title",
    font=terminalio.FONT,
    scale=3,
    color=0xFFFFFF,
    anchored_position=(display.width // 2, 0),
    anchor_point=(0.5, 0),
)
temp_label = Label(
    text="Temperature:",
    font=terminalio.FONT,
    scale=2,
    color=0xFFFFFF,
    anchored_position=(0, 70),
    anchor_point=(0, 0.5),
)
temp_value = Label(
    text="0 C",
    font=terminalio.FONT,
    scale=2,
    color=0xFFFFFF,
    anchored_position=(display.width, 70),
    anchor_point=(1, 0.5),
)

splash.append(title_label)
splash.append(temp_label)
splash.append(temp_value)
display.show(splash)

while True:
    cpu_temp = microcontroller.cpu.temperature
    temp_value.text = f"{cpu_temp:.1f} C"
    time.sleep(0.5)
