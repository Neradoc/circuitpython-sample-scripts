"""
Read the REPL to receive color data for the neopixel.
Not using the usb_cdc module.
"""

import board
import json
import time
import supervisor
import sys

################################################################
# select the serial REPL port
################################################################

serial = sys.stdin

################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################

pix = None
if hasattr(board, "NEOPIXEL"):
    import neopixel
    pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pix.fill((32, 16, 0))
else:
    print("This board is not equipped with a Neopixel.")

################################################################
# loop-y-loop
################################################################

while True:
    # read the REPL serial line by line when there's data
    # note that this assumes that the host always sends a full line
    if supervisor.runtime.serial_bytes_available:
        data_in = serial.readline()

        # try to convert the data to a dict (with JSON)
        data = None
        if data_in:
            try:
                data = json.loads(data_in)
            except ValueError:
                data = {"raw": data_in}

        # by using a dictionary, you can add any entry and data into it
        # to transmit any command you want and parse it here
        if isinstance(data, dict):

            # change the color of the neopixel
            if "color" in data:
                print("Color received:", data["color"])
                if pix is not None:
                    pix.fill(data["color"])

    # this is where the rest of your code goes
    # if the code does a lot you don't need a call to sleep, but if possible
    # it's good to have the microcontroller sleep from time to time so it's
    # not constantly chugging
    time.sleep(0.01)
