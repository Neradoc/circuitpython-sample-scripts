import board
import digitalio
from adafruit_neokey.neokey1x4 import NeoKey1x4

i2c_bus = board.STEMMA_I2C()
neokey = NeoKey1x4(i2c_bus, addr=0x30)

# choose the Interrup pin
# IRQ_PIN = board.D5

# copying the constants from adafruit_featherwing, no need to install it
BUTTON_A = const(1 << 4)
BUTTON_B = const(1 << 5)
BUTTON_C = const(1 << 6)
BUTTON_D = const(1 << 7)
button_mask = BUTTON_A|BUTTON_B|BUTTON_C|BUTTON_D

# set the buttons to input, pull up
neokey.pin_mode_bulk(button_mask, neokey.INPUT_PULLUP)
# enable the interrupts on the buttons
neokey.set_GPIO_interrupts(button_mask, True)
neokey.interrupt_enabled = True
# setup the interrupt pin (no pull, it's driven by the wing)
# interrupt = digitalio.DigitalInOut(IRQ_PIN)

# past state of the buttons to detect release
buttons_pressed_past = button_mask

while True:
    # if the interrupt pin is set (to LOW)
    # if not interrupt.value:

    # get the bitmask of the buttons state
    # this resets the interrupt pin (to HIGH)
    buttons_pressed = neokey.digital_read_bulk(button_mask)

    # that if is not necessary if using interrupts:
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
