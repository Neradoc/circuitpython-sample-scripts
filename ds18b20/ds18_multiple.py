# import midi_testing_stuff

# A 4.7Kohm pullup between DATA and POWER is REQUIRED!
import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board D5.
ow_bus = OneWireBus(board.GP2)
# Scan for sensors and grab them all
devices = ow_bus.scan()
print(devices)
ds18 = [DS18X20(ow_bus, found) for found in devices]

# Main loop to print the temperature every second.
while True:
    temperature = sum(ds.temperature for ds in ds18) / len(ds18)
    print("Temperature: {0:0.3f}C".format(temperature))
    print(tuple(ds.temperature for ds in ds18))
    time.sleep(.1)
