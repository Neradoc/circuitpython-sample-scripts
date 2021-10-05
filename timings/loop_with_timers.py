"""
Timer example using adafruit_ticks for maximum compatibility.
Timings are in milliseconds here (they could be converted but it's fine).
"""
import time
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

# every 5 seconds:
TIMER_1_DELAY = 5000
# every 2 seconds:
TIMER_2_DELAY = 2000

# Change *_next_run to now or 0 if you want to trigger it on the first loop.
# Or "now + X" to trigger at a different time the first time.
"""Examples:
- Trigger the first run after the DELAY
    next_run  = now + DELAY
- Trigger the first run in the first loop
    next_run  = 0
- Trigger the first run after 10 seconds
    next_run  = now + 10_000
"""

now = ticks_ms()
timer_1_next_run = ticks_add(now, TIMER_1_DELAY)
timer_2_next_run = ticks_add(now, TIMER_2_DELAY)

while True:
    # set "now" only once per loop, it's the time reference for the loop.
    now = ticks_ms()
    if ticks_less(timer_1_next_run, now):
        # Next time based on last time
        # This avoids drifting, but can cause multiple triggerings if the rest
        # of the loop takes too long and delays are too short.
        timer_1_next_run = ticks_add(timer_1_next_run, TIMER_1_DELAY)
        print("TIMER 1 TRIGGERED", time.monotonic())
    if ticks_less(timer_2_next_run, now):
        # Next time based on current time.
        # This causes drifting, but guarantees a minimum delay between triggers.
        timer_2_next_run = ticks_add(now, TIMER_2_DELAY)
        print("TIMER 2 TRIGGERED             ", time.monotonic())
