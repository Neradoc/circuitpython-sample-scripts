"""
Minimal keypad example
"""
import board
import keypad
import usb_hid

############################################################
# Input pins, the keypad part

KEY_PINS = (
    board.GP0,
    board.GP1,
    # etc. choose your pins
)

# Here, they are setup as pull-UP, switch Flase/True if pull down
keys = keypad.Keys(KEY_PINS, value_when_pressed=False, pull=True)

############################################################
# Output keys, the keyboard part

from adafruit_hid.keycode import Keycode
from adafruit_hid.keyboard import Keyboard

keyboard = Keyboard(usb_hid.devices)

keys_to_press = (
    (Keycode.ALT, Keycode.TAB),
    (Keycode.F14,),
    # etc. each entry matches a button, and has to be a tuple or list
)

############################################################
# The loop

while True:
    event = keys.events.get()
    if event:
        to_press = keys_to_press[event.key_number]
        print(event, to_press)

        if to_press:
            if event.pressed:
                # the * unpacks the tuple into a list of arguments
                keyboard.send(*to_press)
                # alternate choice: hold the key while button pressed (6 keys max)
                # keyboard.press(*to_press)
            else:
                pass
                # release the key(s) if it was being held
                # keyboard.release(*to_press)
