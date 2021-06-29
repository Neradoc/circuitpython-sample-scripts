## Serial sample codes

Sample codes for USB serial communication between the board and a serial port on the host computer.

Using the data serial channel added with Circuitpython 7 requires installing the `boot.py` file that will enable the second (data) serial port, making it possible to exchange data without interfering with the REPL, including binary data.

### Serial Send

Send data from the host computer to the board.

### Serial Read

Read data sent by the board onto the host computer.

### Serial Exchange

Bidirectional serial communication.
