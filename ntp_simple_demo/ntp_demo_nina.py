"""
Modified from https://gist.github.com/netroy/d1bff654fa58b884d63894ca2c890fc6
"""
import board
import rtc
import time

#######################################################################
# Configure your timezone, DST included
#######################################################################
TZ_OFFSET = 3600 * 2

#######################################################################
# Setuo ESP here with your pins
#######################################################################
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = board.SPI()
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

#######################################################################
# Connect to wifi
#######################################################################

print("CONNECT WIFI")
while not esp.is_connected:
	try:
		esp.connect_AP(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
	except RuntimeError as e:
		print("could not connect to AP, retrying: ", e)
		continue

#######################################################################
# Time setting helper
#######################################################################

def try_set_time(esp, tz_offset=0):
    # get_time will raise ValueError if the time isn't available yet.
    try:
        now = time.localtime(esp.get_time()[0] + tz_offset)
    except OSError:
        return False
    rtc.RTC().datetime = now
    return True

while not try_set_time(esp, TZ_OFFSET):
    time.sleep(0.01)

#######################################################################
# Set the time, waiting until it's available
#######################################################################

while not try_set_time(esp, TZ_OFFSET):
    time.sleep(0.01)

print("Synced with NTP")

#######################################################################
# Simple time formatting helper
#######################################################################

def format_time(now):
    return "{hour}:{minutes:02}:{seconds:02}".format(
        hours=now.tm_hour, minutes=now.tm_min, seconds=now.tm_sec
    )

#######################################################################
# Print time
#######################################################################

now = time.localtime()
print(format_time(now))
