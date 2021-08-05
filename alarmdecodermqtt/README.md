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
- Ability to define a list of zones that are on an expander board so that they
  are not cleared by alphanumeric messages.

# What this is NOT

- This is not a rigorously tested secure addon.  I do my best, but I am not an
IT professional.
- Plans for granting "write" access to the alarm panel are on the back burner.
I use this for sensor inputs only.  So you can't arm or disarm the alarm with
this interface, which should add some security.
- This is not an interface that enables all of the possible features of the
AlarmDecoder system.

# Configuration

__expander_zones__ - (optional) A list of integer zone numbers that should be
marked as expander zones.  Normally the AlarmDecoder interface
learns that a zone is on an expander board when it changes state.  However,
if a zone is in a faulted state on startup, the zone will be initialized using
the alphanumeric message and by default will not be treated as an expander
zone until the zone changes state.  This can be annoying because zones tracked
using the alphanumeric messages are not as reliable.
