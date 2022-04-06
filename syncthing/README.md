# Syncthing
Syncthing is a continuous file synchronization program. It synchronizes files between two or more computers in real time.  More about  [Syncthing](https://syncthing.net/).

# Notes for Home Assistant
- The config files are stored in /config/syncthing so that they can be manually edited or viewed if you so choose using Visual Studio or other addon in Home Assistant.
- By default, the Syncthing front end can only be accessed through ingress using the supervisor page for authenticated Home Assistant users.  This is proxied through nginx inside the addon.  However, if you desire, you can set a port for the GUI access on the Add-On configuration page.  This will enable access to the GUI and the Rest API for use with the syncthing integration.
- The addon is NOT prebuilt.  It is generated on your Home Assistant instance, so slower machines such as Raspberry Pis may take a few minutes to build the addon when first installed.
- You can and should set a username and password in Syncthing, particularly if you enable direct access to the GUI by setting a GUI port as described above.  It will cause the browser authentication box to pop up requesting a username and password.  If the GUI port is not defined, then the only access to it is through Home Assistant, with Home Assistant providing security to the frontend.  You decide how much security you would like.

# Known Issues
- When the Syncthing frontend is first accessed after any reboot you will see a yellow notice stating: "Syncthing should not run as a privileged or system user." I am aware of this.
I intentionally chose to keep syncthing running as root.  Syncthing is running on its own docker instance with nginx and nothing else.  Changing the user running Syncthing would
make it impossible to use Syncthing to backup such things as /config, which are owned by root.  I am fine with the risk for myself, you decide if you are willing to accept this
risk.  You can fork this repository, add `su-exec` to the apk installs, generate a new user in the Dockerfile, and use `su-exec` to run syncthing as that user in run.sh if you
want to avoid this warning.
- I would not advise syncing the `/config/syncthing` folder unless you want interesting things to happen.

