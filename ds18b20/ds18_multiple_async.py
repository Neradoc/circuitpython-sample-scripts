import time
import board
from adafruit_onewire.bus import OneWireBus
from adafruit_ds18x20 import DS18X20

# Initialize one-wire bus on board D5.
ow_bus = OneWireBus(board.GP2)
# Scan for sensors and grab them all
ds18 = [DS18X20(ow_bus, found) for found in ow_bus.scan()]
# 10-bit resolution (default 12)
ds18.resolution = 10

# read (request) the temperature every 5 seconds
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
            temperatures = [ds.read_temperature() for ds in ds18]
            # next request is TEMPERATURE_DELAY after the previous request
            ds18_next = ds18_next - ds18_async_delay + TEMPERATURE_DELAY
            # next action is requesting
            ds18_do_read = False
            # do something with the temperature
            average_temp = sum(temperatures) / len(ds18)
            print(average_temp)

        # if we have not requested the next one yet, do it
        # (we test ds18_next again, because reading might have changed it)
        if not ds18_do_read and now > ds18_next:
            # request the async read, and receive the delay declared by the sensors
            max_read_delay = max(ds.start_temperature_read() for ds in ds18)
            # reading the sensors will happen after the async delay
            ds18_async_delay = max_read_delay * 1.01 # 1% margin to be sure
            ds18_next = now + ds18_async_delay
            # next action is reading
            ds18_do_read = True
