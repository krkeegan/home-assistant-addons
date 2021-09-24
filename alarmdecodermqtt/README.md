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

- An mqtt topic for each zone on/off payloads
- An mqtt topic for the panel with a json payload of all of the panel
  attributes, including `state` which produces a Home Assistant friendly state
- Ability to define a list of zones that are on an expander board so that they
  are not cleared by alphanumeric messages.
- An available topic that outputs `online` and `offline` status.

# What this is NOT

- This is not a rigorously tested secure addon.  I do my best, but I am not an
IT professional.
- Plans for granting "write" access to the alarm panel are on the back burner.
I use this for sensor inputs only.  So you can't arm or disarm the alarm with
this interface, which should add some security.

# Configuration

__expander_zones__ - (optional) A list of integer zone numbers that should be
marked as expander zones.  Normally the AlarmDecoder interface
learns that a zone is on an expander board when it changes state.  However,
if a zone is in a faulted state on startup, the zone will be initialized using
the alphanumeric message and by default will not be treated as an expander
zone until the zone changes state.  This can be annoying because zones tracked
using the alphanumeric messages are not as reliable.

__retain__ - (boolean) Whether panel and zone states should be retained on the
mqtt broker.

# HomeAssistant Entities

Here are some example configurations for defining entities in HomeAssistant.

**Motion Sensor**
```yaml
binary_sensor motion:
  - platform: mqtt
    name: "Downstairs Motion"
    availability_topic: "alarmdecoder/available"
    state_topic: "alarmdecoder/zone/1"
    device_class: "motion"
    payload_on: "on"
    payload_off: "off"
```

**Door Sensor**
```yaml
binary_sensor door:
  - platform: mqtt
    name: "Frontdoor"
    availability_topic: "alarmdecoder/available"
    state_topic: "alarmdecoder/zone/3"
    device_class: "door"
    payload_on: "on"
    payload_off: "off"
```

**Window Sensor**
```yaml
binary_sensor window:
  - platform: mqtt
    name: "Living Room"
    availability_topic: "alarmdecoder/available"
    state_topic: "alarmdecoder/zone/4"
    device_class: "window"
    payload_on: "on"
    payload_off: "off"
```

**Alarm Panel Entity**
```yaml
alarm_control_panel:
  - platform: mqtt
    name: "Alarm Panel"
    availability_topic: "alarmdecoder/available"
    state_topic: "alarmdecoder/panel"
    value_template: "{{value_json.state}}"
    command_topic: "alarmdecoder/panel/set"
    json_attributes_topic: "alarmdecoder/panel"
    json_attributes_template: >-
      {{
      {
      "ready": value_json.ready,
      "battery_low": value_json.battery_low,
      "armed_away": value_json.armed_away,
      "armed_home": value_json.armed_home,
      "zone_bypassed": value_json.zone_bypassed,
      "ac_power": value_json.ac_power,
      "chime_on": value_json.chime_on,
      "alarm_event_occurred": value_json.alarm_event_occurred,
      "alarm_sounding": value_json.alarm_sounding,
      "entry_delay_off": value_json.entry_delay_off,
      "fire_alarm": value_json.fire_alarm,
      "check_zone": value_json.check_zone,
      "perimeter_only": value_json.perimeter_only,
      "system_fault": value_json.system_fault,
      "timestamp": value_json.timestamp
      } | tojson
      }}
```

*Note the `command_topic` doesn't do anything yet, but it is required.
**Also note, that a keypad will not be displayed unless you define a `code` in the alarm panel entity.  This is a bug in HomeAssistant and I have reported it to them.

# TODO

- Write up some actual documentation for how to use this.
- Better logging (timestamps, control logging level, more messages)
- Consider whether to add support for "writing" to the panel (arm, disarm)
