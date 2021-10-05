"""
A Timer class that will trigger a callback if the time has passed
by calling Timer.update() in a loop.

Rather than use independent timers, you can use module functions to manage
a list of timers, and update them all in one call.
"""

import time


try:
    # this is for most boards and computers
    # long ints require memory allocation, but sorting is straightforward
    ticks_ms = lambda: time.monotonic_ns() // 1_000_000
    ticks_add = lambda a,b: a + b
    ticks_less = lambda a,b: a < b
    Tick = lambda x: x.next_run
except (ImportError, NameError):
    try:
        # this is for M0 non express boards where adafruit_ticks is installed
        # the memory advantage of ticks is lost due to the sorting trick
        from adafruit_ticks import ticks_ms, ticks_add, ticks_less
        # required for sorting relative values
        class Tick:
            def __init__(self, by):
                self.val = by.next_run
            def __lt__(self, other):
                return ticks_less(self.val, other.val)
            def __gt__(self, other):
                return not ticks_less(self.val, other.val)
            def __eq__(self, other):
                return self.val == other.val
    except (ImportError, NameError):
        # this is for M0 non express boards without adafruit_ticks
        # maybe you are still using 6.3.0 or just like pain ?
        ticks_ms = lambda: int(time.monotonic() * 1000)
        ticks_add = lambda a,b: a + b
        ticks_less = lambda a,b: a < b
        Tick = lambda x: x.next_run


class Timer:
    def __init__(self, callback, delay, initial=None, data=()):
        now = ticks_ms()
        self.callback = callback
        self.delay = int(delay * 1000)
        if initial is None:
            self.initial_delay = self.delay
        else:
            self.initial_delay = int(initial * 1000)
        self.data = data
        self.next_run = ticks_add(now, self.initial_delay)

    def restart(self):
        now = ticks_ms()
        if self.initial_delay == 0:
            self.run()
        else:
            self.next_run = ticks_add(now, self.initial_delay)

    def run(self):
        self.callback(self.next_run / 1000, self.data)
        self.next_run = ticks_add(self.next_run, self.delay)

    def update(self, now = ticks_ms()):
        if ticks_less(self.next_run, now):
            self.run()

all_timers = []

def add_timer(delay, initial=None, data=()):
    """
    Add a timer with a decorator.
    If initial is 0 (default) it will fire once the first time.
    Otherwise it will wait that amount of time, regardless of the delay,
    to start running every delay seconds.
    If initial is None, the delay value is used as the initial delay.

    :param delay: float number of seconds between runs of the timer.
    :param initial: float number of seconds before the first run (0).

    Example:

        @timer.add_timer(TIMER_1_DELAY, data=1)
        def timer_1_callback(now, data):
            print(f"TIMER {data} --> {now:.2f}")
    """
    def _inside(callback):
        t = Timer(callback, delay, initial, data)
        all_timers.append(t)
        all_timers.sort(key=Tick)
        return t
    return _inside

def restart_timer(timer, initial=0):
    """Restart a timer that was stopped"""
    if timer not in all_timer:
        all_timers.append(t)
        all_timers.sort(key=Tick)

def stop_timer(timer):
    """Stop a timer instance from running."""
    if timer in all_timers:
        all_timers.remove(timer)

def stop_all():
    """Stop all timers."""
    all_timers = []

def update_all():
    updated = False
    now = ticks_ms()
    for timer in all_timers:
        if ticks_less(timer.next_run, now):
            timer.run()
            updated = True
        else:
            break
    if updated:
        all_timers.sort(key=Tick)
