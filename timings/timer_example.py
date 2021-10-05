import time
import timer_class as timer

TIMER_1_DELAY = 5  # every 5 seconds
TIMER_2_DELAY = 2  # every 2 seconds
TIMER_3_DELAY = 7  # every 7 seconds

# add a timer with a decorator
@timer.add_timer(TIMER_1_DELAY)
def timer_1_callback(now, data):
    print(f"TIMER 1 --> {now:.2f}")

# add timers with a function call
def timer_callback(now, data):
    space = "      " * (data-1)
    print(f"TIMER {data} --> {space}{now:.2f}")

timer_2 = timer.add_timer(TIMER_2_DELAY, data=2, initial=0)(timer_callback)
timer_3 = timer.add_timer(TIMER_3_DELAY, data=3)(timer_callback)

while True:
    timer.update_all()
    # sleep a little bit 
    time.sleep(0.01)
