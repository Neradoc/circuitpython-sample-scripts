"""
This does 2 actions, in succession, after 10 seconds and 50 seconds.
The difference with the simple example is that the wait until the next event
changes depending on the state of the application.
For example: turn an LED on for 10 seconds every 60s (50s + 10s = 1 minute).
"""
import time
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

# if this is 0, the first action will be executed immediately
START_DELAY = 0
# action for 10 seconds:
TIMER_1_DELAY = 10_000
# action for 50 seconds:
TIMER_2_DELAY = 50_000

# starting state (LED off for example)
current_state = False # off
now = ticks_ms()
next_time = ticks_add(now, START_DELAY)

while True:
    # take the time once per loop, as the reference
    now = ticks_ms()
    if ticks_less(next_time, now):
        if current_state is False:
            # actual action (turn LED on for example)
            print("Do the thing that lasts {} seconds".format(TIMER_1_DELAY/1000))
            print(time.time())
            # timer management
            delta = TIMER_1_DELAY
        else:
            # actual action (turn LED off for example)
            print("Do the thing that lasts {} seconds".format(TIMER_2_DELAY/1000))
            print(time.time())
            # timer management
            delta = TIMER_2_DELAY
        # set the next event
        next_time = ticks_add(next_time, delta)
        # switch the state (2 states here, True or False)
        current_state = not current_state
    # do something else or sleep a little bit to avoid a tight loop
    time.sleep(0.01)
