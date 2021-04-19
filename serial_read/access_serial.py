"""
a simple, string based (no json), serial read
"""
import argparse
import re
import serial
import time

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="Serial port of the board", nargs=1)
args = parser.parse_args()
port = args.port

channel = serial.Serial(args.port[0])
channel.timeout = 0.05

while True:
    line = None
    try:
        line = channel.readline()[:-2]
    except KeyboardInterrupt:
        print("KeyboardInterrupt - quitting")
        exit()
    # NOTE: does not catch serial errors

    if line:
        m = re.match(r"\((\d+(\.\d+)?)\)", line.decode("utf8"))
        if m:
            temperature = float(m.group(1))
            print(f"Temperature: {temperature:.2f}°C")

    time.sleep(0.1)
