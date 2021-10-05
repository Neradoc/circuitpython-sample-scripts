"""

"""
import time

# every 5 seconds:
TIMER_1_DELAY = 5
# every 2 seconds:
TIMER_2_DELAY = 2

# NOTE: time.monotonic() loses precision after many hours of running.
# Prefer using time.monotonic_ns() on boards that support it.
# Since monotonic_ns is in nano seconds, you have to adapt the delays.

# Change *_next_run to now or 0 if you want to trigger it on the first loop.
# Or "now + X" to trigger at a different time the first time.
now = time.monotonic()
timer_1_next_run = now + TIMER_1_DELAY
timer_2_next_run = now + TIMER_2_DELAY

"""Examples:
- Trigger the first run after the DELAY
    next_run  = now + DELAY
- Trigger the first run in the first loop
    next_run  = 0
- Trigger the first run after 10 seconds
    next_run  = now + 10
"""

while True:
    now = time.monotonic()
    if now > timer_1_next_run:
        # Next time based on current time.
        # This causes drifting, but guarantees a minimum delay between triggers.
        timer_1_next_run = now + TIMER_1_DELAY
        print("TIMER 1 TRIGGERED")
    if now > timer_2_next_run:
        # Next time based on last time
        # This avoids drifting, but can cause multiple triggerings if the rest
        # of the loop takes too long and delays are too short.
        timer_2_next_run = timer_2_next_run + TIMER_2_DELAY
        print("TIMER 2 TRIGGERED")
    # Sleep a little bit to avoid a tight loop.
    # Remove this if the loop does other things.
    time.sleep(0.01)
