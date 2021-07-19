"""
This file uses code from:
https://github.com/adafruit/Adafruit_CircuitPython_PortalBase.git

That code is under MIT license.
Copyright (c) 2020 Melissa LeBlanc-Williams for Adafruit Industries
Modified by Neradoc (2021)

To use it you need the usual secrets.py file, with adafruit IO credentials.
These are used to access the time service while performing rate limiting.
"""
import gc
import rtc
import socketpool
import ssl
import time
import wifi
import adafruit_requests


# you'll need to pass in an io username and key
TIME_SERVICE = (
    "https://io.adafruit.com/api/v2/%s/integrations/time/strftime?x-aio-key=%s"
)
# our strftime is %Y-%m-%d %H:%M:%S.%L %j %u %z %Z see http://strftime.net/ for decoding details
# See https://apidock.com/ruby/DateTime/strftime for full options
TIME_SERVICE_FORMAT = "%Y-%m-%d %H:%M:%S.%L %j %u %z %Z"


try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to ", secrets["ssid"])
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
socket_pool = socketpool.SocketPool(wifi.radio)
print("Connected with IP ", wifi.radio.ipv4_address)
requests = adafruit_requests.Session(socket_pool, ssl.create_default_context())


def get_strftime(time_format, location=None):
    """
    Fetch a custom strftime relative to your location.

    :param str location: Your city and country, e.g. ``"America/New_York"``.

    """
    # pylint: disable=line-too-long
    api_url = None
    reply = None
    try:
        aio_username = secrets["aio_username"]
        aio_key = secrets["aio_key"]
    except KeyError:
        raise KeyError(
            "\n\nOur time service requires a login/password to rate-limit. Please register for a free adafruit.io account and place the user/key in your secrets file under 'aio_username' and 'aio_key'"  # pylint: disable=line-too-long
        ) from KeyError

    if location is None:
        location = secrets.get("timezone", location)
    if location:
        print("Getting time for timezone", location)
        api_url = (TIME_SERVICE + "&tz=%s") % (aio_username, aio_key, location)
    else:  # we'll try to figure it out from the IP address
        print("Getting time from IP address")
        api_url = TIME_SERVICE % (aio_username, aio_key)
    api_url += "&fmt=" + url_encode(time_format)

    try:
        response = requests.get(api_url, timeout=10)
        if response.status_code != 200:
            print(response)
            error_message = (
                "Error connecting to Adafruit IO. The response was: " + response.text
            )
            raise RuntimeError(error_message)
        reply = response.text
    except KeyError:
        raise KeyError(
            "Was unable to lookup the time, try setting secrets['timezone'] according to http://worldtimeapi.org/timezones"  # pylint: disable=line-too-long
        ) from KeyError
    # now clean up
    response.close()
    response = None
    gc.collect()

    return reply


def url_encode(url):
    """
    A function to perform minimal URL encoding
    """
    url = url.replace(" ", "+")
    url = url.replace("%", "%25")
    url = url.replace(":", "%3A")
    return url


def get_local_time(location=None):
    # pylint: disable=line-too-long
    """
    Fetch and "set" the local time of this microcontroller to the local time at the location, using an internet time API.

    :param str location: Your city and country, e.g. ``"America/New_York"``.

    """
    reply = get_strftime(TIME_SERVICE_FORMAT, location=location)
    if reply:
        times = reply.split(" ")
        the_date = times[0]
        the_time = times[1]
        year_day = int(times[2])
        week_day = int(times[3])
        is_dst = None  # no way to know yet
        year, month, mday = [int(x) for x in the_date.split("-")]
        the_time = the_time.split(".")[0]
        hours, minutes, seconds = [int(x) for x in the_time.split(":")]
        now = time.struct_time(
            (year, month, mday, hours, minutes, seconds, week_day, year_day, is_dst)
        )

        if rtc is not None:
            rtc.RTC().datetime = now

    return reply


tt = get_local_time()
print(tt)
