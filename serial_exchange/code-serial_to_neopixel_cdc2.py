import board
import digitalio
import json
import time
import usb_cdc

################################################################
# init board's LEDs for visual output
# replace with your own pins and stuff
################################################################

pix = None
if hasattr(board,"NEOPIXEL"):
    import neopixel
    pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
    pix.fill((32, 16, 0))

led = None
if hasattr(board,"LED"):
    led = digitalio.DigitalInOut(board.LED)
    led.switch_to_output()
    led.value = False

################################################################
# init board's button for acknowledging user interaction
# replace with your own pins and stuff
# - the code tries its best to find a default button
# - two fixed default values on some boards (for my tests)
################################################################

# boards with buttons:
BUTTONS_CANDIDATES = ["BUTTON", "BUTTON_USR", "BUTTON_USER", "BUTTON_A", "BUTTON_X", "BUTTON_UP", "BUTTON1", "BUTTON_1"]
for btn_pin in BUTTONS_CANDIDATES:
    if hasattr(board, btn_pin):
        button = digitalio.DigitalInOut(getattr(board, btn_pin))
        button.switch_to_input(digitalio.Pull.UP)
        button_id = btn_pin
        break
else: # no break
    """
    Change the BUTTON pin to match your setup, and button_id
    """
    # this is an example for the pico
    if hasattr(board,"GP3"): pin = board.GP3
    # this is an example for most boards/feathers
    elif hasattr(board,"A2"): pin = board.A2
    # pin = board.SOMEPIN
    button = digitalio.DigitalInOut(pin)
    button.switch_to_input(digitalio.Pull.UP)
    button_id = repr(pin).replace("board.","")

################################################################
# prepare values for the loop
################################################################

usb_cdc.data.timeout = 0.1
if button:
    button_past = button.value

################################################################
# loop-y-loop
################################################################

while True:
    data_out = {}

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
        if isinstance(data,dict):
            if "color" in data and pix is not None:
                pix.fill(data["color"])
            if "blink" in data and led is not None:
                # blinking without sleep is left as an exercise
                led.value = True
                time.sleep(0.25)
                led.value = False
                time.sleep(0.25)

    # read the buttons and send the info to the serial
    if button and button_past != button.value:
        button_past = button.value
        if not button.value:
            data_out["buttons"] = [{"status": "PRESSED", "id": button_id}]
        else:
            data_out["buttons"] = [{"status": "RELEASED", "id": button_id}]
    if data_out:
        print(json.dumps(data_out))
        usb_cdc.data.write(json.dumps(data_out).encode()+b"\r\n")

    time.sleep(0.1)