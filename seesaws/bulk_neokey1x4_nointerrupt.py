import board
import digitalio
from adafruit_neokey.neokey1x4 import NeoKey1x4

i2c_bus = board.STEMMA_I2C()
neokey = NeoKey1x4(i2c_bus, addr=0x30)

# button names are arbitrary
BUTTON_A = const(1 << 4)
BUTTON_B = const(1 << 5)
BUTTON_C = const(1 << 6)
BUTTON_D = const(1 << 7)
button_mask = BUTTON_A|BUTTON_B|BUTTON_C|BUTTON_D

# set the buttons to input, pull up
neokey.pin_mode_bulk(button_mask, neokey.INPUT_PULLUP)

# past state of the buttons to detect changes
buttons_pressed_past = button_mask

while True:
    # get the bitmask of the buttons state
    # this resets the interrupt pin (to HIGH)
    buttons_pressed = neokey.digital_read_bulk(button_mask)

    if buttons_pressed_past != buttons_pressed:

        # buttons that just got pressed
        if buttons_pressed & BUTTON_A == 0 and buttons_pressed_past & BUTTON_A:
            print("Button A")
        if buttons_pressed & BUTTON_B == 0 and buttons_pressed_past & BUTTON_B:
            print("Button B")
        if buttons_pressed & BUTTON_C == 0 and buttons_pressed_past & BUTTON_C:
            print("Button C")
        if buttons_pressed & BUTTON_D == 0 and buttons_pressed_past & BUTTON_D:
            print("Button D")

        # buttons that just got released
        if buttons_pressed_past & BUTTON_A == 0 and buttons_pressed & BUTTON_A:
            print("Button A Released")
        if buttons_pressed_past & BUTTON_B == 0 and buttons_pressed & BUTTON_B:
            print("Button B Released")
        if buttons_pressed_past & BUTTON_C == 0 and buttons_pressed & BUTTON_C:
            print("Button C Released")
        if buttons_pressed_past & BUTTON_D == 0 and buttons_pressed & BUTTON_D:
            print("Button D Released")

    # save the state
    buttons_pressed_past = buttons_pressed
