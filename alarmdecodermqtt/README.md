# AlarmDecoder

The AlarmDecoder is a device produced by Nu Tech Software Solutions. The
AlarmDecoder devices provide a serial, TCP/IP socket or USB interface to the
alarm panel, where it emulates an alarm keypad.

Please visit the [AlarmDecoder](https://www.alarmdecoder.com/index.php) website
for further information about the AlarmDecoder devices.

# Home Assistant

Home Assistant already has a built in integration for
[AlarmDecoder](https://www.home-assistant.io/integrations/alarmdecoder/)

# What is this then?

The [AlarmDecoder API](https://github.com/nutechsoftware/alarmdecoder) had
some issues that didn't work for my installation.  Development on the API has
slowed.  In addition, the API is not directly included in HomeAssistant but
instead relies on an
[additional wrapper library](https://github.com/ajschmidt8/adext).  So any
change takes quite a while to get upstreamed all the way into HomeAssistant.

I was not happy waiting for my fixes to be incorporated.  So I made this addon
to allow for faster and easier incorporation of my changes.

You can read about what differences this has from the upstream AlarmDecoder
[here](https://github.com/krkeegan/alarmdecoder).

I also use MQTT heavily in my system.

## Features

This has very basic and rudimentary features:

- An mqtt topic for each zone with json payloads
- An mqtt topic with the global "ready" state of the alarm

# What this is NOT

- This is not a rigorously tested secure addon.  I do my best, but I am not an
IT professional.
- I have no plans for granting "write" access to the alarm panel.  I use this
for sensor inputs only.  So you can't arm or disarm the alarm with this
interface.
- This is not an interface that enables all of the possible features of the
AlarmDecoder system.
