import time
from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService

SERVICE_NAME = "My UART"

ble = BLERadio()
uart_connection = None

while True:
	if not uart_connection or not uart_connection.connected:
		print(f'Trying to connect to "{SERVICE_NAME}"...')
		for adv in ble.start_scan(ProvideServicesAdvertisement):
			if UARTService in adv.services and adv.short_name == SERVICE_NAME:
				uart_connection = ble.connect(adv)
				print("Connected")
				break
		ble.stop_scan()

	if uart_connection and uart_connection.connected:
		uart_service = uart_connection[UARTService]
		if uart_service.in_waiting:
			data = uart_service.readline().decode("utf-8").strip()
			if data:
				print(data)

	time.sleep(0.1)
