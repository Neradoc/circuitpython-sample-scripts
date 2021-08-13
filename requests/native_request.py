import board
import time
import socketpool
import ssl
import wifi
import adafruit_requests

try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

print("Connecting to ", secrets["ssid"])
wifi.radio.connect(ssid=secrets["ssid"], password=secrets["password"])
socket_pool = socketpool.SocketPool(wifi.radio)
print("Connected with IP ", wifi.radio.ipv4_address)

print("Wifi test")

requests = adafruit_requests.Session(socket_pool, ssl.create_default_context())
response = requests.get("http://wifitest.adafruit.com/testwifi/index.html")
print(response.status_code)
print(response.text)

response = requests.get("https://api.github.com/repos/adafruit/circuitpython")
print(response.status_code)
print("The Circuitpython repo has {} stars.".format(response.json()["stargazers_count"]))

print("done")
