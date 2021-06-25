import time
import json
from alarmdecoder import AlarmDecoder
from alarmdecoder.devices import SocketDevice

# Load Config
f = open('/data/options.json')
config = json.load(f)
f.close()

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
        device.on_message += handle_message
        with device.open():
            while True:
                time.sleep(1)

    except Exception as ex:
        print('Exception:', ex)


def handle_message(sender, message):
    """
    Handles message events from the AlarmDecoder.
    """
    print(message.raw)


if __name__ == '__main__':
    main()
