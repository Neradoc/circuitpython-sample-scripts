import board
import os

# keep these pins, so they don't get freed
keep_pins = {}
# the status LED (can be deinited from the outside or here)
pixels = None

def get_npixels():
	"""
	Find the number of pixels based on hand-filled board information
	"""
	machine = os.uname().machine
	if npixels is None:
		npixels = 1
		npixels_by_machine = {
			"Adafruit MagTag with ESP32S2": 4,
			"Adafruit CircuitPlayground Express with samd21g18": 10,
			"Adafruit Circuit Playground Bluefruit with nRF52840": 10,
			"Adafruit PyGamer with samd51j19": 5,
			"Adafruit PyGamer with samd51j20": 5,
			"Adafruit Pybadge with samd51j19": 5,
			"Adafruit FunHouse with ESP32S2": 5,
			"Adafruit NeoPixel Trinkey M0 with samd21e18": 4,
			"Adafruit Trellis M4 Express with samd51g19": 4*8,
		}
		npixels_by_name = {
			"Adafruit NeoPixel Trinkey": 4,
			"Adafruit FunHouse": 5,
			"Adafruit FunHome": 5, # alternate name for FunHouse (bug)
			"Adafruit PyGamer": 5,
			"Adafruit PyBadge": 5,
			"Adafruit CircuitPlayground": 10, # catch all variants (crickit, displayio)
		}

		# find by fill machine description
		if machine in npixels_by_machine:
			return npixels_by_machine[machine]

		# fallback to search in name
		for name in npixels_by_name:
			if name in machine:
				return npixels_by_name[name]

		return 1


def get_status_led(npixels = None, *, brightness = None):
	"""
	Can force the number of pixels used (to 1 for example on the pybadge LC)
	"""
	global pixels

	if npixels is None:
		npixels = get_npixels()

	if hasattr(board,"NEOPIXEL"):
		"""
		For a board that has a neopixel (eg: QT PY M0)
		"""
		import neopixel
		pixels = neopixel.NeoPixel(board.NEOPIXEL, npixels)
	elif hasattr(board,"APA102_SCK"):
		"""
		For a board that has a APA102 (eg: UnexpectedMaker Feather S2, Trinket M0)
		"""
		import adafruit_dotstar
		pixels = adafruit_dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, npixels)
	elif hasattr(board,"DOTSTAR_CLOCK"):
		"""
		For a board that has DOTSTAR pins (eg: FunHouse)
		"""
		import adafruit_dotstar
		pixels = adafruit_dotstar.DotStar(board.DOTSTAR_CLOCK, board.DOTSTAR_DATA, npixels)
	else:
		raise OSError("No hardware pixel identified")


	if hasattr(board,'LDO2'):
		"""
		Enable LDO2 on the Feather S2 so we can use the status LED
		"""
		from digitalio import DigitalInOut, Direction
		ldo2 = DigitalInOut(board.LDO2)
		ldo2.switch_to_output()
		ldo2.value = True
		keep_pins["ldo2"] = ldo2
		time.sleep(0.035)


	if hasattr(board,"NEOPIXEL_POWER"):
		"""
		On the MagTag, bring down NEOPIXEL_POWER
		"""
		from digitalio import DigitalInOut, Direction
		neopower = DigitalInOut(board.NEOPIXEL_POWER)
		neopower.switch_to_output()
		neopower.value = False
		keep_pins["neopower"] = neopower

	if brightness is not None:
		pixels.brightness = brightness

	return pixels


def deinit_status_led():
	"""
	deinits the status pixels, be careful not to use it after that
	reverses and deinits the enable pins
	"""
	global pixels
	if pixels is not None:
		pixels.deinit()
		pixels = None

	for pin in keep_pins:
		pin.value = not pin.value
		if hasattr(board,'LDO2'):
			time.sleep(0.035)
		pin.deinit()
