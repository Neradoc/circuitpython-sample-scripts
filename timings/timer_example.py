import time
import timer

# every 5 seconds:
TIMER_1_DELAY = 5
# every 2 seconds:
TIMER_2_DELAY = 2

def timer_1_callback(now, data):
    print(f"TIMER {data} TRIGGERED {now:f}")

def timer_2_callback(now, data):
    print(f"TIMER {data} TRIGGERED {now:f}")

timer_1 = timer.add_timer(timer_1_callback, TIMER_1_DELAY, data=(1))
timer_2 = timer.add_timer(timer_2_callback, TIMER_2_DELAY, data=(2))

while True:
    timer.update()
    # sleep a little bit 
    time.sleep(0.01)
