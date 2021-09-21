A few sample scripts to read one or more DS18B20 temperature sensors connected to the same bus, asynchronously.

The sensor is used by:

- A requesting to start a new measure
- B waiting until the conversion is finished (either by asking repeatedly or waiting the time given)
- C asking for and receiving the temperature from the sensor memory

DS18X20.temperature does all that synchronously (it blocks the code until the conversion has finished).

The async code here:

- Checks if the reading delay has passed (line 27) (which handles B)
- Reads the temperature from the sensor (line 31) if it was previously requested (line 29) (part C)
- Sets the time for the next request (line 33) (which can be 0). Which handles how often you want to update.
- The second block requests the next measure (line 43) (part A)
- And sets the time for when the next read is possible (line 45-46) (this is the duration of part B).

It might seem weird to do A after C, but that's because I want to request the next measure immediately after the read if the delay is 0 (and not wait a full run of the while loop). The variable "ds18_do_read" could be called "ds18_next_measure_has_been_requested", and its initial value (False) ensures that we don't try to read the sensor before requesting the first measure.

Note that the time needed for the conversion depends of the resolution of the temperature. You can change the resolution with "ds18.resolution = 9" for example, if that resolution is good enough for you. From testing it seems that 9 bits gives a 0.5 °C accuracy, 10 is 0.25 and so on.

Here is the conversion time per resolution:

- 9-bit: 93.75 ms
- 10-bit: 187.5 ms
- 11-bit: 375 ms
- 12-bit: 750 ms (default)
