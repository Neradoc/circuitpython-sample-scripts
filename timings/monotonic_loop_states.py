"""
This does 2 actions, in succession, after 10 seconds and 50 seconds.
For example: turn an LED on for 10 seconds every 60s (50s + 10s = 1 minute)
"""
import time

# if this is 0, the first action will be executed immediately
START_DELAY = 0
# action for 10 seconds:
TIMER_1_DELAY = 10
# action for 50 seconds:
TIMER_2_DELAY = 50

# starting state (LED off for example)
current_state = False # off
next_time = time.monotonic() + START_DELAY

while True:
    # take the time once per loop, as the reference
    now = time.monotonic()
    if now > next_time:
        if current_state is False:
            # actual action (turn LED on for example)
            print("Do the thing that lasts {} seconds".format(TIMER_1_DELAY))
            # timer management
            delta = TIMER_1_DELAY
        else:
            # actual action (turn LED off for example)
            print("Do the thing that lasts {} seconds".format(TIMER_2_DELAY))
            # timer management
            delta = TIMER_2_DELAY
        # set the next event
        next_time = now + delta
        # switch the state (2 states here, True or False)
        current_state = not current_state
    # do something else or sleep a little bit to avoid a tight loop
    time.sleep(0.1)
