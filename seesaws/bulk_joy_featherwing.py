import board
import countio
import time
import digitalio
from adafruit_seesaw.seesaw import Seesaw
# from adafruit_featherwing.joy_featherwing import *

# choose the Interrup pin
IRQ_PIN = board.D5

# copying the constants from adafruit_featherwing, no need to install it
BUTTON_A = const(1 << 6)
BUTTON_B = const(1 << 7)
BUTTON_Y = const(1 << 9)
BUTTON_X = const(1 << 10)
BUTTON_SELECT = const(1 << 14)
button_mask = BUTTON_A|BUTTON_B|BUTTON_X|BUTTON_Y|BUTTON_SELECT

i2c_bus = board.I2C()
seesaw = Seesaw(i2c_bus)

# set the buttons to input, pull up
seesaw.pin_mode_bulk(button_mask, seesaw.INPUT_PULLUP)
# enable the interrupts on the buttons
seesaw.set_GPIO_interrupts(button_mask, True)
seesaw.interrupt_enabled = True
# setup the interrupt pin (no pull, it's driven by the wing)
interrupt = digitalio.DigitalInOut(IRQ_PIN)
# past state of the buttons to detect release
buttons_pressed_past = button_mask

while True:
    # if the interrupt pin is set (to LOW)
    if not interrupt.value:
        # get the bitmask of the buttons state
        # this resets the interrupt pin (to HIGH)
        buttons_pressed = seesaw.digital_read_bulk(button_mask)

        # buttons that just got pressed
        if buttons_pressed & BUTTON_A == 0:
            print("Button A")
        if buttons_pressed & BUTTON_B == 0:
            print("Button B")
        if buttons_pressed & BUTTON_X == 0:
            print("Button X")
        if buttons_pressed & BUTTON_Y == 0:
            print("Button Y")
        if buttons_pressed & BUTTON_SELECT == 0:
            print("Select")

        # buttons that just got released
        if buttons_pressed_past & BUTTON_A == 0 and buttons_pressed & BUTTON_A:
            print("Button A Released")
        if buttons_pressed_past & BUTTON_B == 0 and buttons_pressed & BUTTON_B:
            print("Button B Released")
        if buttons_pressed_past & BUTTON_X == 0 and buttons_pressed & BUTTON_X:
            print("Button X Released")
        if buttons_pressed_past & BUTTON_Y == 0 and buttons_pressed & BUTTON_Y:
            print("Button Y Released")
        if buttons_pressed_past & BUTTON_SELECT == 0 and buttons_pressed & BUTTON_SELECT:
            print("Select Released")

        # save the state
        buttons_pressed_past = buttons_pressed

    # no need to sleep if the loop does other time consuming things
    time.sleep(0.02)

    # x = seesaw.analog_read(2)
    # y = seesaw.analog_read(3)

    time.sleep(0.02)
