"""
A simple, json based, serial write.
Loops on a color wheel to send color info to the board.
"""
import argparse
import datetime
import json
import psutil
import serial
import time

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="Serial port of the board", nargs=1)
args = parser.parse_args()
port = args.port

channel = serial.Serial(args.port[0])
channel.timeout = 0.05

"""
VIOLET          GREEN           RED
CYAN            ORANGE          BLUE            MAGENTA
SKY             YELLOW          PURPLE          color
TEAL            WHITE           BLACK           GOLD
PINK            AQUA            JADE            AMBER
RAINBOW
"""

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


index = 0
while True:
    # note: faire le CPU en parallèle
    #cpu = psutil.cpu_percent(4)
    mem = psutil.virtual_memory()[2]

    now = datetime.datetime.now()
    tjour = now.strftime("%a")
    tdate = now.strftime("%d/%m/%Y")
    ttime = now.strftime("%H:%M:%S").rjust(13)

    channel.write(json.dumps({
        "lines": [
            "This is title", # f"CPU: {cpu} %",
            f"RAM: {mem} %",
            None,
            tjour,
            tdate,
            ttime,
        ],
        "colors": [
            "CYAN",
            "ORANGE",
            None,
            None,
            "GREEN",
            "PINK",
        ],
    }).encode() + b"\r\n")
    index += 8

    print(tjour, tdate, ttime)

    if channel.in_waiting:
        data = channel.readline()
        print(data.decode().strip())

    time.sleep(1)
