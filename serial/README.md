## Serial sample codes

Sample codes for USB serial communication between the board and a serial port on the host computer.

Using the data serial channel added with Circuitpython 7 requires copying the `boot.py` file that will enable the second (data) serial port, making it possible to exchange data without interfering with the REPL, including binary data.

All 3 examples have 3 files each.

- The "host" script that must be run on the computer with python 3, by giving the serial port of the board as argument to the command line. The script requires pyserial to be installed.
```
pip3 install pyserial
```
- Two board codes that can be renamed to `code.py` or imported from it.
    - One that will listen or output to the REPL (or console) serial channel.
    - One that will listen or output to the data serial channel.

To help find the serial ports (REPL or data) on the host side, the `find_serial_port.py` script lists the ports per board and per type (if present). It requires the `adafruit_board_toolkit` module.
```
pip3 install adafruit_board_toolkit
```

### Serial Send

Send data from the host computer to the board.
The host computer sends cycling color data regularly to the board, using JSON encoding to change the color on the board. For testing purposes the code will print out the color to the REPL.

The board is expected to have a built-in neopixel. If it doesn't, replace it with external neopixels, a dotstar or a screen, etc. It might require to install the `neopixel` library from the library bundle, though it is included in the Circuitpython firmware on some boards.

### Serial Read

Read data sent by the board to the host computer.
The board is sending sensor data to the serial port, trying the CPU temperature first, and sending a randomly fluctuating value if it was not available. You would of course change the `generate_some_data` function to read a sensor connected to or embeded on the board.

The values are sent in a simple text format that can be displayed in the Mu graphics panel to draw a line graph over time. The host computer code just prints out the values.

### Serial Exchange

Bidirectional serial communication.
This shows a two-way communication using JSON data between the board and the host computer. The computer code uses the `asyncio` module for asynchronous execution and prompts the user for a color by name (list in the code) or `(r,g,b)` values and sends it to the board, which will display the color on it's built-in neopixel. The keyword `blink` will make the on-board monochrome LED (if any) blink once.

The board sends button presses that the host prints out. It makes a best effort to detect an existing built-in button. For example the A button on the Circuit Playground boards.

The board is expected to have a built-in neopixel. If it doesn't, replace it with external neopixels, a dotstar or a screen, etc. It might require to install the `neopixel` library from the library bundle, though it is included in the Circuitpython firmware on some boards.
