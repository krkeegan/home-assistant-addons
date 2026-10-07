#!/bin/bash
set -e

export HOME=/config/syncthing/
export STNOPORTPROBING=1

if [ ! -f '/config/syncthing/config.xml' ]; then
    # Run syncthing to generate initial configuration files, then edit
    # config.xml to remove 127.0.0.1 limit from the GUI address.
    syncthing --home=/config/syncthing generate --no-port-probing
    sed -i 's|<address>127.0.0.1:8384</address>|<address>:8384</address>' /config/syncthing/config.xml
fi

# Syncthing issues a startup warning when run as root ("Syncthing should not run
# as a privileged or system user"). Since Home Assistant requires root to read
# and write mapped volumes (/config, /share), we dismiss this cosmetic warning
# on startup via the REST API once Syncthing is healthy.
dismiss_privileged_warning() {
    local api_key=""
    for i in $(seq 1 30); do
        if [ -f '/config/syncthing/config.xml' ]; then
            api_key=$(sed -n 's:.*<apikey>\(.*\)</apikey>.*:\1:p' /config/syncthing/config.xml)
            [ -n "$api_key" ] && break
        fi
        sleep 1
    done

    [ -z "$api_key" ] && return 0

    for i in $(seq 1 30); do
        if curl -s -f "http://127.0.0.1:8384/rest/noauth/health" > /dev/null 2>&1; then
            break
        fi
        sleep 1
    done

    sleep 2

    local errors
    errors=$(curl -s -H "X-API-Key: $api_key" "http://127.0.0.1:8384/rest/system/error" 2>/dev/null || true)
    if echo "$errors" | grep -q "privileged or system user"; then
        curl -s -X POST -H "X-API-Key: $api_key" "http://127.0.0.1:8384/rest/system/error/clear" > /dev/null 2>&1 || true
    fi
}

dismiss_privileged_warning &

exec syncthing --no-browser --no-upgrade --home=/config/syncthing/
