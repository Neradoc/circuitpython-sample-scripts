import board
import displayio
import microcontroller
import terminalio
import time

from adafruit_display_text.bitmap_label import Label
import adafruit_fancyled.adafruit_fancyled as fancy

blue = fancy.CRGB(0, 0, 1.0)
red = fancy.CRGB(1.0, 0, 0)
yellow = fancy.CRGB(1.0, 1.0, 0)
white = fancy.CRGB(1.0, 1.0, 1.0)

oled = board.DISPLAY
splash = displayio.Group()

title_label = Label(
    text="My Title", font=terminalio.FONT, color=0x00FF80, scale=3,
    anchored_position=(oled.width // 2, 0), anchor_point=(0.5, 0),
)
temp_label = Label(
    text="Temperature:", font=terminalio.FONT, color=0xFFFFFF, scale=2,
    anchored_position=(0, 70), anchor_point=(0, 0.5),
)
temp_value = Label(
    text="0 C", font=terminalio.FONT, color=0xFFFFFF, scale=2,
    anchored_position=(oled.width, 70), anchor_point=(1, 0.5),
)

splash.append(title_label)
splash.append(temp_label)
splash.append(temp_value)
oled.show(splash)

def display_temperature(the_temp):
    if the_temp > 30:
        color = red.pack()
    elif the_temp > 20:
        color = fancy.mix(red, yellow, (30 - the_temp) / 10).pack()
    elif the_temp < 0:
        color = blue.pack()
    elif the_temp < 10:
        color = fancy.mix(blue, white, (the_temp) / 10).pack()
    elif the_temp < 20:
        color = fancy.mix(white, yellow, (the_temp - 10) / 10).pack()
    else:
        color = yellow.pack()
    temp_value.color = color
    temp_value.text = f"{the_temp:.1f} C"

# test code showing the thing
for cpu_temp in range(-5, 32*2):
    cpu_temp = cpu_temp / 2
    display_temperature(cpu_temp)
    time.sleep(0.1)

while True:
    cpu_temp = microcontroller.cpu.temperature
    display_temperature(cpu_temp)
    time.sleep(0.5)
