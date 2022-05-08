## BLE UART Forwarding

These two files let you connect a UART device over bluetooth to a computer. The code is not bidirectional, but that can be added with few changes.

- `ble_uart_forwarding.py` is run on a bluetooth capable board that is connected to a UART peripheral/device and forwards all the data from it to the UART bluetooth service.
- `ble_uart_receiving.py` is run on a bluetooth capable board or computer to receive the data over bluetooth UART, using Circuitpython or Blinka.
