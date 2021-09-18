"""
This will scroll the latest exception on the screen.
If you can't use supervisor.get_previous_traceback

https://circuitpython.readthedocs.io/en/latest/shared-bindings/supervisor/index.html#supervisor.get_previous_traceback
"""

try:
    import yourcode
except Exception as e:
    # Disable the screen
    import board
    board.DISPLAY.show(None)
    # Scroll the Error
    import time
    import traceback
    error = traceback.format_exception(e, e, e.__traceback__)
    error = error.strip().replace("\r\n", " | ")
    while True:
        print("\n----------")
        for word in error.split(" "):
            print(word, end=" ")
            time.sleep(0.5)
        time.sleep(1)
