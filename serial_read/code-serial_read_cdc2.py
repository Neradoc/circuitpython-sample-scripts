"""
This uses the optional second serial port available in Circuitpython 7.x
Activate it in the boot.py file with the following code

import usb_cdc
usb_cdc.enable(console=True, data=True)

Some boards might require disabling USB endpoints to enable the data port.
"""

import microcontroller
import time
import random
import usb_cdc


past_temp = 20


def generate_some_data():
    """
    dummy data, replace that by reading a sensor
    or buttons, or whatever
    """
    try:  # CPY temperature
        return microcontroller.cpu.temperature
    except:
        pass
    # dummy data
    global past_temp
    past_temp = past_temp + random.random() - 0.5
    return past_temp


while True:
    data_out = {}
    temperature = generate_some_data()
    # prints with () on a solo line to satisfy the Mu grapher
    usb_cdc.data.write(f"({temperature})\r\n".encode())
    # change the sleep time to match your needs
    time.sleep(1)
