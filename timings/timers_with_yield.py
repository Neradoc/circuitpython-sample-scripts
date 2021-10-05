import time
from adafruit_ticks import ticks_ms, ticks_add, ticks_less

# every 5 seconds:
TIMER_1_DELAY = 5_000
# every 2 seconds:
TIMER_2_DELAY = 2_000

# this function is the whole extent of this timer "library"
def setup_timer(callback, delay, initial_delay=0, data=()):
    next_run = ticks_add(ticks_ms(), initial_delay)
    while True:
        now = ticks_ms()
        if ticks_less(next_run, now):
            callback(now,data)
            next_run = ticks_add(next_run, delay)
        yield

# callbacks we want to run on a timer
def timer_1_callback(now,data):
    print(f"TIMER {data} --> {time.monotonic():.2f}")

def timer_2_callback(now,data):
    print(f"TIMER {data} -->       {time.monotonic():.2f}")

# setup the timers
timer_1 = setup_timer(timer_1_callback, TIMER_1_DELAY, data=(1))
timer_2 = setup_timer(timer_2_callback, TIMER_2_DELAY, data=(2))

# run the loop
while True:
    next(timer_1)
    next(timer_2)
    # sleep a little bit 
    time.sleep(0.01)
