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
    def __init__(self, callback, delay, initial_delay=0, data=()):
        now = monotonic()
        self.callback = callback
        self.delay = time_convert(delay)
        self.initial_delay = time_convert(initial_delay)
        self.data = data
        self.next_run = now + self.initial_delay

    def update(self):
        if monotonic() > self.next_run:
            self.run()

    def run(self):
        self.callback(time_deconvert(self.next_run), self.data)
        self.next_run += self.delay
        

all_timers = []

def add_timer(*args, **kwargs):
    t = Timer(*args, **kwargs)
    all_timers.append(t)
    all_timers.sort(key=lambda t: t.next_run)
    return t

def stop_timer(timer):
    all_timers.remove(timer)

def update():
    now = monotonic()
    for timer in all_timers:
        if now > timer.next_run:
            timer.run()
        else:
            break
    all_timers.sort(key=lambda t: t.next_run)
