import microcontroller
import time
import random


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
    print(f"({temperature})")
    # change the sleep time to match your needs
    time.sleep(1)
