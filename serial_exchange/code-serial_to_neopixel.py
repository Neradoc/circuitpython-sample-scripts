import board
import digitalio
import json
import neopixel
import time
import re
import supervisor

# echo -e "0,50,50\r" > /dev/cu.usbmodem144443301

pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
pix[0] = (255, 128, 0)

if hasattr(board, "BUTTON"):  # QTPY 2040 button or other
    button = digitalio.DigitalInOut(board.BUTTON)
    button.switch_to_input(digitalio.Pull.UP)
else:
    button = None

pattern = re.compile("(\d+),(\d+),(\d+)")
button_past = button.value
while True:
    data_out = {}
    if supervisor.runtime.serial_bytes_available:
        x = input()
        try:
            data = json.loads(x)
        except:
            data = {"raw": x}
        #
        if "color" in data:
            pix[0] = data["color"]
            # print("Color set:",color)
    if button and button_past != button.value:
        button_past = button.value
        if not button.value:
            data_out["buttons"] = [{"status": "PRESSED", "id": "BOOT"}]
        else:
            data_out["buttons"] = [{"status": "RELEASED", "id": "BOOT"}]
    if data_out:
        print(json.dumps(data_out))
    time.sleep(0.1)
