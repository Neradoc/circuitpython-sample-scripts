"""
A simple, string based (no json), serial read.
Reads the data and interprets it as a float reprensenting the temperature.
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
        try:
            # remove the parenthesis
            m = line.decode("utf8")[1:-1]
            temperature = float(m)
            print(f"Temperature: {temperature:.2f}°C")
        except ValueError:
            # ignore an error if float() fails
            # (with the REPL, you get board reload messages and such)
            pass

    time.sleep(0.1)
