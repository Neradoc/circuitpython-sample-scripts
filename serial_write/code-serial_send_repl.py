import board
import json
import time
import supervisor

################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################

pix = None
if hasattr(board,"NEOPIXEL"):
    import neopixel
    pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pix.fill((32, 16, 0))

################################################################
# loop-y-loop
################################################################

while True:
    # add to that dictionary to send the data at the end of the loop
    data_out = {}

    # read the secondary serial line by line
    # when there's data, with a timeout
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
        if isinstance(data,dict):

            # change the color of the neopixel
            if "color" in data and pix is not None:
                pix.fill(data["color"])

    time.sleep(0.01)
