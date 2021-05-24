"""
a simple, json based, serial write
"""
import argparse
import json
import re
import serial
import time

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="Serial port of the board", nargs=1)
args = parser.parse_args()
port = args.port

channel = serial.Serial(args.port[0])
channel.timeout = 0.05


def wheel(wheel_pos):
    """Color wheel to allow for cycling through the rainbow of RGB colors."""
    wheel_pos = wheel_pos % 256
    if wheel_pos < 85:
        return 255 - wheel_pos * 3, 0, wheel_pos * 3
    elif wheel_pos < 170:
        wheel_pos -= 85
        return 0, wheel_pos * 3, 255 - wheel_pos * 3
    else:
        wheel_pos -= 170
        return wheel_pos * 3, 255 - wheel_pos * 3, 0


while True:
    for x in range(256):
        color = wheel((x * 8) % 256)

        print(color)
        channel.write(json.dumps({ "color": color }).encode())
        channel.write(b"\r\n")

        time.sleep(0.2)
