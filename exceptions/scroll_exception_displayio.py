try:
    import yourcode
except Exception as e:
	import board
    import displayio
    import terminalio
    from adafruit_display_text import label, wrap_text_to_pixels
    group = displayio.Group()
    display = board.DISPLAY
    display.show(group)
    group.append(textarea := label.Label(
        font=terminalio.FONT,
        text="Error",
        scale=1,
        x=0,
        y=7,
    ))
    NLINES = display.height // terminalio.FONT.get_bounding_box()[1]
    # Scroll the Error
    import time
    import traceback
    error0 = traceback.format_exception(e, e, e.__traceback__)
    error = error0.strip().replace("\r", "")
    # error = error.replace("  ", " ")
    lines = wrap_text_to_pixels(
        string=error,
        max_width=display.width,
        font=terminalio.FONT,
    )
    dashes = "-" * (display.width // terminalio.FONT.get_bounding_box()[0])
    lines = [dashes] + lines
    lines_num = len(lines)
    while len(lines) < lines_num + NLINES + 1:
        lines = lines + lines

    print(lines_num, NLINES)
    
    while True:
        print(error0)
        for x in range(max(1, lines_num)):
            board.DISPLAY.refresh()
            textarea.text = "\n".join(lines[x:x+NLINES])
            time.sleep(1)
