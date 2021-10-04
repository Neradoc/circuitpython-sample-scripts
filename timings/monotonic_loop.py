import time

# every 5 seconds:
TIMER_1_DELAY = 5
# every 2 seconds:
TIMER_2_DELAY = 2

# change *_next_run to 0 if you want to trigger it on the first loop
# or "now + X" to trigger at a different time the first time
now = time.monotonic()
timer_1_next_run = now + TIMER_1_DELAY
timer_2_next_run = now + TIMER_2_DELAY

while True:
    now = time.monotonic()
    if now > timer_1_next_run:
        # next time
        timer_1_next_run = now + TIMER_1_DELAY
        print("TIMER 1 TRIGGERED")
    if now > timer_2_next_run:
        # next time
        timer_2_next_run = now + TIMER_2_DELAY
        print("TIMER 2 TRIGGERED")
    # sleep a little bit to avoid a tight loop
    time.sleep(0.1)
