"""
Example of how to switch between animations
Requires adafruit_led_animation
"""
import board
import digitalio
import time

from adafruit_led_animation.animation.chase import Chase
from adafruit_led_animation.animation.comet import Comet
from adafruit_led_animation.color import AMBER, JADE

# Update to match the pin connected to your NeoPixels
pixel_pin = board.A3
# Update to match the number of NeoPixels you have connected
pixel_num = 30
# Update to match the button's pin
# If the Pull direction had to be changed, change the button tests too
button = digitalio.DigitalInOut(board.D6)
button.switch_to_input(digitalio.Pull.UP)

pixels = neopixel.NeoPixel(pixel_pin, pixel_num, brightness=0.5, auto_write=False)

chase = Chase(cp.pixels, speed=0.1, size=3, spacing=6, color=AMBER)
comet = Comet(cp.pixels, speed=0.02, color=JADE, tail_length=10, bounce=True)

anims = [chase, comet]
anim = 0

while True:
	anims[anim].animate()
	if not button.value:
		anim = (anim + 1) % len(anims)
		# wait for button release
		while not button.value:
			time.sleep(0.1)
	time.sleep(0.01)
