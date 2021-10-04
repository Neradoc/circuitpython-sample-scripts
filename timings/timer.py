"""
A Timer class that will trigger a callback if the time has passed
by calling Timer.update() in a loop.

Rather than use independent timers, you can use module functions to manage
a list of timers, and update them all in one call. Timers are automatically
sorted by next run time to exit early from the update loop.
"""

import time

if hasattr(time,"monotonic_ns"):
    monotonic = time.monotonic_ns
    time_convert = lambda t: int(t * 1000) * 1_000_000
    time_deconvert = lambda t: t / 1_000_000_000
else:
    monotonic = time.monotonic
    time_convert = lambda t: t
    time_deconvert = lambda t: t

class Timer:
    def __init__(self, callback, delay, initial=None, data=()):
        now = monotonic()
        self.callback = callback
        self.delay = time_convert(delay)
        if initial is None:
            self.initial_delay = self.delay
        else:
            self.initial_delay = time_convert(initial)
        self.data = data
        self.next_run = now + self.initial_delay

    def restart(self):
        now = monotonic()
        if self.initial_delay == 0:
            self.run()
        else:
            self.next_run = now + self.initial_delay

    def run(self):
        self.callback(time_deconvert(self.next_run), self.data)
        self.next_run += self.delay

    def update(self):
        if monotonic() > self.next_run:
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
        all_timers.sort(key=lambda t: t.next_run)
        return t
    return _inside

def restart_timer(timer, initial=0):
    """Restart a timer that was stopped"""
    if timer not in all_timer:
        all_timers.append(t)
        all_timers.sort(key=lambda t: t.next_run)

def stop_timer(timer):
    """Stop a timer instance from running."""
    if timer in all_timers:
        all_timers.remove(timer)

def stop_all():
    """Stop all timers."""
    all_timers = []

def update_all():
    now = monotonic()
    run = filter(lambda t: now > t.next_run, all_timers)
    for timer in run:
        timer.run()
    all_timers.sort(key=lambda t: t.next_run)
