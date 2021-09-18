try:
    import yourcode
except KeyboardInterrupt:
    pass
except Exception as e:
    import traceback
    error = traceback.format_exception(e, e, e.__traceback__)

    import board
    import displayio
    import adafruit_displayio_sh1106
    import time

    displayio.release_displays()
    spi = board.SPI()
    display_bus = displayio.FourWire(
        spi,
        command=board.OLED_DC,
        chip_select=board.OLED_CS,
        reset=board.OLED_RESET,
        baudrate=1000000,
    )
    WIDTH = 128
    HEIGHT = 64
    display = adafruit_displayio_sh1106.SH1106(display_bus, width=WIDTH, height=HEIGHT)

    error = error.strip().replace("\r\n", " | ")
    while True:
        print("\n----------")
        for word in error.split(" "):
            print(word, end=" ")
            time.sleep(0.5)
        time.sleep(1)
