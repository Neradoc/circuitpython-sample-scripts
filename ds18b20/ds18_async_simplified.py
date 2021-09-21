import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board D5.
ow_bus = OneWireBus(board.GP2)
# Scan for sensors and grab them all
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# initiate the first measure
max_read_delay = ds18.start_temperature_read()
# reading the sensor will happen after the async delay
ds18_next = time.monotonic() + max_read_delay

# Main loop to print the temperature every 5 second.
while True:
    now = time.monotonic()

    # Is it time to read ?
    if now > ds18_next:
        # fetch the temperatures from the sensor
        temperature = ds18.read_temperature()
        # request the async read, and receive the delay declared by the sensor
        max_read_delay = ds18.start_temperature_read()
        # reading the sensor will happen after the async delay
        ds18_next = now + max_read_delay
        # do something with the temperature
        print(f"{temperature:.2f}°C / {temperature * 9/5 + 30:.2f}°F")
