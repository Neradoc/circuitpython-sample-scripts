"""
Switch between animations with the Circuit Playground Express/Bluefruit
Requires adafruit_led_animation
"""
from adafruit_circuitplayground import cp
import time

# for other boards:
# pixels = neopixel.NeoPixel(board.NEOPIXEL, NUMPIXELS)
# button = digitalio.DigitalInOut(board.BUTTON)
# button.switch_to_input(digitalio.Pull.UP)

from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import AMBER, JADE

chase = Chase(cp.pixels, speed=0.06, size=3, spacing=6, color=AMBER)
comet = Comet(cp.pixels, speed=0.02, color=JADE, tail_length=10, bounce=True)

anim = comet

while True:
	anim.animate()
	# lookup buttons to switch between animations
	buttons = cp.were_pressed
	if buttons:
		if 'A' in buttons:
			anim = chase
		if 'B' in buttons:
			anim = comet
	# the switch sets the brightness
	if cp.switch:
		cp.pixels.brightness = 0.2
	else:
		cp.pixels.brightness = 0.8
	# wait a bit, but not too long to read buttons
	time.sleep(min(0.2, anim.speed / 20))
