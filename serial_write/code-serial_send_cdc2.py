"""
Read the Serial port to receive color data for the neopixel.


This uses the optional second serial port available in Circuitpython 7.x
Activate it in the boot.py file with the following code

import usb_cdc
usb_cdc.enable(console=True, data=True)

Some boards might require disabling USB endpoints to enable the data port.
"""

import board
import json
import time
import supervisor
import usb_cdc

################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################

pix = None
if hasattr(board, "NEOPIXEL"):
    import neopixel

    pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pix.fill((32, 16, 0))

################################################################
# loop-y-loop
################################################################

while True:
    # read the secondary serial line by line
    # when there's data, with a timeout
    if usb_cdc.data.in_waiting > 0:
        data_in = usb_cdc.data.readline()

        # try to convert the data to a dict (with JSON)
        data = None
        if len(data_in) > 0:
            try:
                data = json.loads(data_in)
            except:
                data = {"raw": data_in.decode()}

        # interpret
        if isinstance(data, dict):

            # change the color of the neopixel
            if "color" in data and pix is not None:
                pix.fill(data["color"])

    time.sleep(0.01)