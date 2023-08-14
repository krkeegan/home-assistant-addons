# 0.2.8
Bug fix for change introduced in HA 2022-06

# 0.2.7
- Added time to log entries
- Try and reconnect when connection to alarmdecoder is lost

# 0.2.6
HomeAssistant seems to have changed.  Now optional string config
settings are forced to ''.  Added additional checks.

# 0.2.2
Add retain option to config.
Change zone payloads to `ON` and `OFF` to match HomeAssistant default.

# 0.2.1
An attempt at creating an availability topic

# 0.2.0
This is a stable release, with all of the initial features I plan to add.

- Drop individual topic for ready state, available as an attribute of panel
  now.
- Move zone topics to be under zone

# 0.1.16
Add state attribute to panel topic.  Possible states match those that are
available in Home Assistant.

# 0.1.13
Publish all panel attribute flags on panel topic.  Can be used as json
attributes when defining the panel.

# 0.1.11
Add `expander_zones` config setting which allows users to optionally designate
zones as being on an expander board.  This helps avoid them being erroneously
restored via alphanumeric messages.

# 0.0.1
Setup of Repo
