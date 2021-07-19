"""
Modified from https://gist.github.com/netroy/d1bff654fa58b884d63894ca2c890fc6
"""
import board
import rtc
import struct
import time
import wifi
import socketpool
import displayio
import terminalio
from adafruit_display_text import bitmap_label as label

# configure your timezone, DST included
TZ_OFFSET = 3600 * 2

SECONDS_1970_TO_2000 = 946_684_800
NTP_TIME_CORRECTION = 2_208_988_800
NTP_SERVER = "pool.ntp.org"
NTP_PORT = 123

SECONDS_TO_YEAR_2000 = time.mktime((2000,1,1,0,0,0,0,0,0))
if SECONDS_TO_YEAR_2000 == 0:
    NTP_TIME_CORRECTION += SECONDS_1970_TO_2000

def get_ntp_time(pool):
    packet = bytearray(48)
    packet[0] = 0b00100011

    for i in range(1, len(packet)):
        packet[i] = 0

    with pool.socket(pool.AF_INET, pool.SOCK_DGRAM) as sock:
        sock.settimeout(None)
        sock.sendto(packet, (NTP_SERVER, NTP_PORT))
        sock.recv_into(packet)
        destination = time.monotonic_ns()

    seconds = struct.unpack_from("!I", packet, offset=len(packet) - 8)[0]
    ntp_localtime_tz = seconds - NTP_TIME_CORRECTION + TZ_OFFSET
    # compensate is there's more than 1s since we retrieved the time
    return time.localtime(
        ntp_localtime_tz
        + (time.monotonic_ns() - destination) // 1_000_000_000
    )

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to ", secrets["ssid"])
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
socket_pool = socketpool.SocketPool(wifi.radio)
print("Connected with IP ", wifi.radio.ipv4_address)

now = get_ntp_time(socket_pool)
print(now)
rtc.RTC().datetime = now
print("Synced with NTP")
time.sleep(1.0)

display = None
if hasattr(board, "DISPLAY"):
    display = board.DISPLAY
else:
    pass
    # insert external display init

if display:
    group = displayio.Group()
    display.show(group)
    text_area = label.Label(
        terminalio.FONT,
        scale = 3,
        color = (255,255,255),
        max_glyphs = 50,
        anchor_point = (0.5, 0.5),
        anchored_position = (
            display.width // 2,
            display.height // 2,
        ),
        text = "Hello"
    )
    group.append(text_area)


while True:
    now = time.localtime()
    clock = "{hour:02d}:{min:02d}:{seconds:02d}".format(hour = now.tm_hour, min = now.tm_min, seconds = now.tm_sec)
    print(clock)
    if display:
        text_area.text = clock
    time.sleep(0.2)
