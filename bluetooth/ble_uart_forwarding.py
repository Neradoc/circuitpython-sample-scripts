import board
import time
import busio

# common configuration
SERVICE_NAME = "My UART" # 8 chars max

# setup UART
uart = busio.UART(board.TX, board.RX)

# setup bluetooth
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.color_packet import ColorPacket
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

ble = BLERadio()
ble.name = "UART With BLE"
uart_service = UARTService()
advertisement = ProvideServicesAdvertisement(uart_service)
advertisement.short_name = SERVICE_NAME
# advertisement.complete_name = "UART BLE" # no more than 8 to not go into extended adv ?

was_connected = False
while True:
	# Advertise BLE when not connected.
	if not ble.connected:
		was_connected = False

		if not ble.advertising:
			print(f'Start advertising as "{SERVICE_NAME}"')
			ble.start_advertising(advertisement, interval=0.5, timeout=5)

		# dismiss uart buffer when not connected
		if uart.in_waiting:
			uart.reset_input_buffer()

	else:
		if not was_connected:
			was_connected = True
			print("Connected")
			ble.stop_advertising()

		# pass-through uart data when connected
		if nbytes := uart.in_waiting:
			# data = uart.read(nbytes)
			data = uart.readline()
			if data:
				print("Broadcasting", data)
				uart_service.write(data)

	time.sleep(0.1)
