"""
A simple script listing serial ports on the computer.
This requires to install the adafruit-board-toolkit module.

pip3 install adafruit-board-toolkit
"""
import adafruit_board_toolkit.circuitpython_serial

ports = (
	adafruit_board_toolkit.circuitpython_serial.repl_comports()
	+adafruit_board_toolkit.circuitpython_serial.data_comports()
)

if ports:
	print(f"{len(ports)} serial Circuitpython ports found connected to the computer.")

	col1 = max([len(port.device) for port in ports]) + 1
	col1 = max(13, col1)

	col3 = max([len(port.product) for port in ports]) + 1
	col3 = max(7, col3)

	col4 = max([len(port.product+port.manufacturer) for port in ports]) + 3
	col4 = max(10, col4)

	print("")
	print("  Port Location".ljust(col1), "Type ", "  Device")
	print("-" * col1, "-" * 5, "-" * col4)

	for port in adafruit_board_toolkit.circuitpython_serial.repl_comports():
		print(f"{port.device:{col1}s} REPL  {port.product} ({port.manufacturer})")

	print("")

	for port in adafruit_board_toolkit.circuitpython_serial.data_comports():
		print(f"{port.device:{col1}s} DATA  {port.product} ({port.manufacturer})")

else:
	print("No serial port matching a Circuitpython board was found.")
