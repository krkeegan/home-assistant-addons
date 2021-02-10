#!/bin/bash
set -e

if [ ! -f '/config/syncthing/config.xml' ]; then
    # Run syncthing to generate initial configuration files, then edit
    # config.xml to remove 127.0.0.1 limit from the GUI address.
    syncthing -generate=/config/syncthing
    sed -i 's|<address>127.0.0.1:8384</address>|<address>:8384</address>' /config/syncthing/config.xml
fi
/usr/sbin/nginx -c /etc/nginx/nginx.conf &
syncthing -no-browser -home=/config/syncthing/
