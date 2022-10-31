"""
Example of how to switch between animations
Requires adafruit_led_animation
"""
import board
from digitalio import DigitalInOut, Pull
import time

from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.sequence import AnimationSequence
from adafruit_led_animation.color import AMBER, JADE

# Update to match the pin connected to your NeoPixels
PIXELS_PIN = board.A3
# Update to match the number of NeoPixels you have connected
PIXELS_NUM = 30
# Update to match the button's pin
BUTTON_PIN = board.D6
# Update to match the button value when pressed
BUTTON_ON_VALUE = False

button = DigitalInOut(BUTTON_PIN)
button.switch_to_input(Pull.DOWN if BUTTON_ON_VALUE else Pull.UP)

def button_pressed():
	return button.value == BUTTON_ON_VALUE

pixels = neopixel.NeoPixel(PIXELS_PIN, PIXELS_NUM, brightness=0.5, auto_write=False)

chase = Chase(cp.pixels, speed=0.1, size=3, spacing=6, color=AMBER)
comet = Comet(cp.pixels, speed=0.02, color=JADE, tail_length=10, bounce=True)

animations = AnimationSequence(comet, chase)

while True:
	animations.animate()
	# lookup buttons to switch between animations
	if button_pressed():
		animations.next()
		# wait for button release (kind of debounce)
		while button_pressed():
			time.sleep(0.01)
	# for slow animations, sleep a bit, but not too long to read buttons
	# time.sleep(min(0.1, anim.speed / 10))
