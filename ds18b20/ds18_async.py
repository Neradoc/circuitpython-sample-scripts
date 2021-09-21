import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board D5.
ow_bus = OneWireBus(board.GP2)
# Scan for sensors and grab them all
ds18 = DS18X20(ow_bus, ow_bus.scan()[0])

# read (request) the temperature every 5 seconds
# set to 0 to read as fast as possible
TEMPERATURE_DELAY = 5

# time when the next read should occur.
ds18_next = time.monotonic()
# should we start the async read or do the actual read ?
ds18_do_read = False
# delay for async read (default, real value will be set later)
ds18_async_delay = 1

# Main loop to print the temperature every 5 second.
while True:
    now = time.monotonic()

    # Is it time to read ?
    if now > ds18_next:
        # if we did request the temperature, now do the read
        if ds18_do_read:
            # fetch the temperatures from the sensor
            temperature = ds18.read_temperature()
            # next request is TEMPERATURE_DELAY after the previous request
            ds18_next = ds18_next - ds18_async_delay + TEMPERATURE_DELAY
            # next action is requesting
            ds18_do_read = False
            # do something with the temperature
            print(temperature)

        # if we have not requested the next one yet, do it
        # (we test ds18_next again, because reading might have changed it)
        if not ds18_do_read and now > ds18_next:
            # request the async read, and receive the delay declared by the sensor
            max_read_delay = ds18.start_temperature_read()
            # reading the sensor will happen after the async delay
            ds18_async_delay = max_read_delay * 1.01 # 1% margin to be sure
            ds18_next = now + ds18_async_delay
            # next action is reading
            ds18_do_read = True
