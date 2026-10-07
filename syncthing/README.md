# Syncthing
Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time.  More about  [Syncthing](https://syncthing.net/).

# Notes for Home Assistant
- The config files are stored in /config/syncthing so that they can be manually edited or viewed if you so choose using Visual Studio or other addon in Home Assistant.
- By default, the Syncthing front end can only be accessed through ingress using the supervisor page for authenticated Home Assistant users.  This is proxied through nginx inside the addon.  However, if you desire, you can set a port for the GUI access on the Add-On configuration page.  This will enable access to the GUI and the Rest API for use with the syncthing integration.
- The addon is NOT prebuilt.  It is generated on your Home Assistant instance, so slower machines such as Raspberry Pis may take a few minutes to build the addon when first installed.
- You can and should set a username and password in Syncthing, particularly if you enable direct access to the GUI by setting a GUI port as described above.  It will cause the browser authentication box to pop up requesting a username and password.  If the GUI port is not defined, then the only access to it is through Home Assistant, with Home Assistant providing security to the frontend.  You decide how much security you would like.

# Security and Privileges
- Syncthing runs inside its own isolated Docker container with root privileges within the container. Running as root is necessary so that Syncthing can read and write mapped folders like `/config` and `/share` which are owned by root.
- Syncthing generates a startup warning notice ("Syncthing should not run as a privileged or system user") when running as UID 0. The addon automatically dismisses this notice via the local Syncthing REST API upon container startup once Syncthing is healthy.

# Known Issues
- I would not advise syncing the `/config/syncthing` folder unless you want interesting things to happen.
