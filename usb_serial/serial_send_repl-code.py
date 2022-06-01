"""
Read the REPL to receive color data for the neopixel.
Not using the usb_cdc module.
"""
import board
import json
import time
import supervisor

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
    if supervisor.runtime.serial_bytes_available:
        data_in = input()

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
            if "color" in data:
                print("Color received:", data["color"])
                if pix is not None:
                    pix.fill(data["color"])

    time.sleep(0.01)
