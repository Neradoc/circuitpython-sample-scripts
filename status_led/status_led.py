import board
import os

# keep these pins, so they don't get freed
_keep = {}

def get_status_led(npixels = None):
	"""
	Can force the number of pixels used (to 1 for example)
	"""
	machine = os.uname().machine

	if npixels is None:
		npixels = 1
		if "CircuitPlayground" in machine:
			npixels = 10
		elif "NeoPixel Trinkey" in machine:
			npixels = 4
		elif "MagTag" in machine:
			npixels = 4
		elif "FunHouse" in machine or "FunHome" in machine:
			npixels = 5

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
		_keep["ldo2"] = ldo2


	if hasattr(board,"NEOPIXEL_POWER"):
		"""
		On the MagTag, bring down NEOPIXEL_POWER
		"""
		from digitalio import DigitalInOut, Direction
		neopower = DigitalInOut(board.NEOPIXEL_POWER)
		neopower.switch_to_output()
		neopower.value = False
		_keep["neopower"] = neopower

	return pixels
