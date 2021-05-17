import argparse
import json
import math
import re
import serial
import sys
import time
from aioconsole import ainput
import asyncio

parser = argparse.ArgumentParser()
parser.add_argument("port", type=str, help="Serial port of the board", nargs=1)
args = parser.parse_args()

port = args.port
channel = None

color_names = {
    "aqua": (0, 255, 255),
    "black": (0, 0, 0),
    "blue": (0, 0, 255),
    "green": (0, 128, 0),
    "orange": (255, 165, 0),
    "pink": (240, 32, 128),
    "purple": (128, 0, 128),
    "red": (255, 0, 0),
    "white": (255, 255, 255),
    "yellow": (255, 255, 0),
}

print("Enter a color in the format: (rrr,ggg,bbb)")
print("Example: (255,125,0) is orange")
print(" ".join([name for name in color_names]))


def setup_serial():
    global channel
    if channel is None:
        try:
            channel = serial.Serial(args.port[0])
            channel.timeout = 0.05
        except Exception as ex:
            print(ex)
            channel = None
    return channel


def error_serial():
    global channel
    if channel != None:
        channel.close()
        channel = None
        print("Exception on read, did the board disconnect ?")


async def read_serial():
    print("read_serial")
    while True:
        setup_serial()
        line = None
        try:
            line = channel.readline()[:-2]
        except KeyboardInterrupt:
            print("KeyboardInterrupt - quitting")
            exit()
        except:
            error_serial()
            await asyncio.sleep(1)
            continue

        data = {}
        if line != b"":
            try:
                data = json.loads(line.decode("utf8"))
            except:
                data = {"raw": line.decode("utf8")}

        # receive button information and print it out
        if "buttons" in data:
            for button in data["buttons"]:
                if button["status"] == "RELEASED":
                    print(f"Button {button['id']} clicked")

        # unidentified data sent by the board, helps with testing
        if "raw" in data:
            print(f"Board sent: {data['raw']}")

        await asyncio.sleep(0.1)


async def read_color():
    """
    Multiple formats for a color to send to the neopixel
    "blink" makes the monochrome LED blink once
    """
    data_out = []
    data_in = await ainput("> ")
    data_in = data_in.strip()

    if re.match("^\((\d+),(\d+),(\d+)\)$", data_in):
        # color formatted as (rrr,ggg,bbb)
        m = re.match("^\((\d+),(\d+),(\d+)\)$", data_in)
        color = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        return json.dumps({"color": color})

    elif data_in.lower() in color_names:
        # color name for simple tests
        color = color_names[data_in.lower()]
        return json.dumps({"color": color})

    elif data_in == "blink":
        # simple blink command
        return json.dumps({"blink":1})

    else:
        # send anything anyway, helps testing the board side code
        return json.dumps({"raw": data_in})

    # should not be reached
    return "\r\n"


async def send_serial():
    print("send_serial")
    while True:
        setup_serial()
        color_string = await read_color()
        try:
            if color_string:
                channel.write((color_string + "\r\n").encode("utf8"))
        except Exception as ex:
            print(ex)
            error_serial()
        await asyncio.sleep(0.1)


boo = asyncio.ensure_future(read_serial())
baa = asyncio.ensure_future(send_serial())
loop = asyncio.get_event_loop()
loop.run_forever()
