"""
Print a number to the REPL.
Format that can be read by the Mu grapher.
Using CPU temperature as a sample data.
"""
import json
import microcontroller
import time
import random


def generate_some_data():
    """
    dummy data, replace that by reading a sensor
    or buttons, or whatever
    """
    try:  # CPU temperature
        return microcontroller.cpu.temperature
    except:
        pass
    # dummy data if temperature not available
    past_temp = past_temp + random.random() - 0.5
    return random.randint(2000, 2500) / 100


while True:
    data_out = {}
    temperature = generate_some_data()
    # prints with () on a solo line to satisfy the Mu grapher
    print(f"({temperature})")
    # change the sleep time to match your needs
    time.sleep(1)
