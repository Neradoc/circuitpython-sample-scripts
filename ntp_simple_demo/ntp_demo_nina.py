"""
Modified from https://gist.github.com/netroy/d1bff654fa58b884d63894ca2c890fc6
"""
import board
import rtc
import struct
import time
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label

# configure your timezone, DST included
TZ_OFFSET = 3600 * 2


# SETUP ESP HERE
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_esp32spi import adafruit_esp32spi_wifimanager

esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("CONNECT WIFI")
while not esp.is_connected:
	try:
		esp.connect_AP(os.getenv("WIFI_SSID"), os.getenv("WIFI_PASSWORD"))
	except RuntimeError as e:
		print("could not connect to AP, retrying: ", e)
		continue

def get_ntp_time(esp):
    # get_time will raise ValueError if the time isn't available yet so loop until
    # it works.
    now_utc = None
    while now_utc is None:
        try:
            now_utc = time.localtime(esp.get_time()[0])
        except OSError:
            pass
    rtc.RTC().datetime = now_utc

now = get_ntp_time(esp)
print("Synced with NTP")
print(now)

time.sleep(1.0)

display = None
if hasattr(board, "DISPLAY"):
    display = board.DISPLAY
else:
    pass
    # insert external display init

if display:
    display.auto_refresh = False
    group = displayio.Group()
    display.show(group)
    text_area = label.Label(
        terminalio.FONT,
        scale=3,
        color=(255, 255, 255),
        anchor_point=(0.5, 0.5),
        anchored_position=(
            display.width // 2,
            display.height // 2,
        ),
        text="Hello",
    )
    group.append(text_area)
    display.refresh()

previous_clock = ""

while True:
    now = time.localtime()
    clock = "{hour:02d}:{min:02d}:{seconds:02d}".format(
        hour=now.tm_hour, min=now.tm_min, seconds=now.tm_sec
    )
    if clock != previous_clock:
        print(clock)
        if display:
            text_area.text = clock
            display.refresh()
        previous_clock = clock
    time.sleep(0.2)
