import time
import timer

# every 5 seconds:
TIMER_1_DELAY = 5
# every 2 seconds:
TIMER_2_DELAY = 2

# add a timer with a decorator
@timer.add_timer(TIMER_1_DELAY, data=1)
def timer_1_callback(now, data):
    print(f"TIMER {data} --> {now:.2f}")

# add a timer with a function call
def timer_2_callback(now, data):
    print(f"TIMER {data} -->       {now:.2f}")
timer_2 = timer.add_timer(TIMER_2_DELAY, data=2, initial=0)(timer_2_callback)

while True:
    timer.update_all()
    # sleep a little bit 
    time.sleep(0.01)
