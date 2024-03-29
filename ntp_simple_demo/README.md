These scripts require native wifi (on ESP32-S2 boards) and the presence of the usual `secrets.py` file used by adafruit libraries, as [explained in this guide for example](https://learn.adafruit.com/pyportal-titano-weather-station/code-walkthrough-secrets-py).

**NOTE: this sample code is considered obsolete.**

- See the [adafruit_ntp library for native NTP support](https://github.com/adafruit/Adafruit_CircuitPython_NTP).
- See this [Metro ESP32S2 guide for Adafruit IO](https://learn.adafruit.com/adafruit-metro-esp32-s2/getting-the-date-time).

------------------

## Simple NTP native demo

This is a simple script that shows download the current time from NTP servers, and displaying a simple clock on the default display if the board has one. Takes into account the value of the board's Epoch (can be 1970 or 2000). 

Your time zone has to be set by modifying `TZ_OFFSET` to the appropriate number of seconds to adjust from GMT.

Add your own display initialization code if you have an external display or read the time in the REPL.

Notes:
- this will be rewritten to use the `adafruit_ntp` library.
- ESP32SPI/airlift boards can use ESPget_time() ([see these notes](https://github.com/adafruit/Adafruit_CircuitPython_NTP/releases/tag/3.0.0)). (A new example will be added for that)

## Adafruit.io time service demo (native)

This script uses adafruit_requests to get the time from the adafruit IO time service, using code borrowed from the PortalBase library.

It requires the presence of valid credentials `aio_username` and `aio_key` in the secrets file.
