import board
import busio
import openlcd_mini
import time
import usb_cdc

i2c = busio.I2C(sda=board.SDA1, scl=board.SCL1)

mini = openlcd_mini.OpenLCD(i2c,114)
mini.clear()

mini.print("Starting")
mini.print("...")
mini.backlight = (0, 255, 255)

import neopixel
pix = neopixel.NeoPixel(board.NEOPIXEL, 1)
pix.fill((32, 16, 0))

while True:
    if usb_cdc.data.in_waiting > 0:
        data_in = usb_cdc.data.readline()
        mini.clear()
        mini.print(data_in.decode())
