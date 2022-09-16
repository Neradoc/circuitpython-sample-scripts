"""
Print a number to the REPL.
Format that can be read by the Mu grapher.
Using CPU temperature as a sample data.


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


def generate_some_data():
    """
    dummy data, replace that by reading a sensor
    or buttons, or whatever
    """
    try:  # CPU temperature
        return microcontroller.cpu.temperature
    except Exception:
        pass
    # dummy data if temperature not available
    past_temp = past_temp + random.random() - 0.5
    return random.randint(2000, 2500) / 100


while True:
    data_out = {}
    temperature = generate_some_data()
    temperature_str = f"({temperature})\r\n".encode()
    # prints with () on a solo line to satisfy the Mu grapher
    usb_cdc.data.write(temperature_str)
    # optionally print to the REPL channel for debug purposes
    # print("DEBUG - sending:", temperature_str)
    # change the sleep time to match your needs
    time.sleep(1)
