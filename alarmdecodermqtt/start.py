import time
import json
import os.path
from alarmdecoder import AlarmDecoder
from alarmdecoder.devices import SocketDevice

# Load Config
if os.path.isfile('/data/options.json'):
    f = open('/data/options.json')
    config = json.load(f)
    f.close()
else:
    # Allow for local testing
    config = {"alarm_addr": "alarmdecoder", "alarm_port": 10000}

# Configuration values
HOSTNAME = config['alarm_addr']
PORT = config['alarm_port']

def main():
    """
    Example application that opens a device that has been exposed to the network
    with ser2sock or similar serial-to-IP software.
    """
    try:
        # Retrieve an AD2 device that has been exposed with ser2sock on localhost:10000.
        device = AlarmDecoder(SocketDevice(interface=(HOSTNAME, PORT)))

        # Set up an event handler and open the device
        device.on_zone_fault += handle_zone_fault
        device.on_zone_restore += handle_zone_restore
        device.on_ready_changed += handle_ready_changed
        with device.open():
            print("Starting AlarmDecoder.")
            while True:
                time.sleep(1)

    except Exception as ex:
        print('Exception:', ex)

def handle_zone_fault(device, zone):
    """
    Handles fault signals.
    """
    print("Zone ", zone, "Fault.", flush=True)

def handle_zone_restore(device, zone):
    """
    Handles fault signals.
    """
    print("Zone ", zone, "Clear.", flush=True)

def handle_ready_changed(device, ready):
    """
    Handles the ready state of the device.
    """
    if ready:
        print("Device Ready", flush=True)
    else:
        print("Device Not Ready", flush=True)

if __name__ == '__main__':
    main()
