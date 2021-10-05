## Timing examples

Learn guide on the subject:
https://learn.adafruit.com/multi-tasking-with-circuitpython

These examples show how to trigger short-term events with a timer inside a while loop, to avoid the blocking nature of `time.sleep`. Longer timings (days or more) are better done using an RTC module, or periodical time synchronisation over the net.

Note that in Circuitpython, timing will never be very precise. For one, there is some overhead in the execution of the code, but also this is python, so a garbage collection for example can be trigger at any time unexpectedly (though there are ways around that by dong it manually).

### Getting A Time Stamp

There are three main ways to get timing information in Circuitpython. They all "drift" over time because the internal timer is usually not a high precision RTC but based on the frequency of the microcontroller, but that should be good enough for relative times.

- `time.monotonic()` is a number of seconds, as a float, since the board boot. Because floats are single-precision, the timer looses precision over time. After 5 days it can't differentiate times below 0.1 seconds, and 1 second after a few weeks. [See this discussion](https://github.com/adafruit/circuitpython/issues/342#issuecomment-337228427).
- `time.monotonic_ns()` is a long int in nanoseconds (1_000_000_000 of a second), and does not lose accuracy. It can be used to do any timing measurement with integers. Be careful with non-integer divisions since you might lose accuracy by converting to a float. **It is not available on most non "express" boards due to memoery constraints**.
- `supervisor.ticks_ms()` is an integer timer in milliseconds, that wraps (goes back to 0) every 2**29 milliseconds (around 6 days), so that it does not need long integers. Because of that it can only measure timings below that value, and the math needs to take into account the possibility of wrapping. **It is only available since Circuitpython 7**.

To unify those uses and pick the best default for short-term timings you can use the [`adafruit_ticks` library](https://github.com/adafruit/Adafruit_CircuitPython_Ticks), available in the Adafruit Library Bundle.

### Example Files

The main point of the examples is to trigger two actions "every X seconds" with a different timing, or "delay" each. The basic example has an action trigger every 2 seconds and the other every 5 seconds.

- A timer can start as soon as the loop starts or only after the delay runs once.
- The delay can be a strict period, avoiding drift, useful to keep a strict timing.
- Or guarantee that each run is separated by at least the delay, which can be required to deal with rate limiting for example.

The files include:

- `loop_with_timers.py`: a loop with 2 timers firing at different intervals.
- `loop_with_timer_states.py`: a loop with one timer changing its timing based on a state variable. One action is triggered after 10 seconds, the next after 50, then back to the first action.
- `timers_with_yield.py`: uses a generator with `yield` as a kind of a light-weight timer library. Schedule multiple timers by calling `setup_timer()` and call `next(a_timer)` to update the timer (and call the callback).
- `timer_class.py` and `timer_example.py`: a larger timer library. Register as many timers as you want with the `add_timer()` decorator, and trigger timer events by calling `update_all()` periodically.
- `monotonic_loop.py`: a loop with 2 timers using time.monotonic(). No dependencies, but don't use for long running programs if it can affect your timers.
