import time
import json
import os.path
from alarmdecoder import AlarmDecoder
from alarmdecoder.devices import SocketDevice
import paho.mqtt.client as mqtt

# Load Config
f = open('/data/options.json')
CONFIG = json.load(f)
f.close()

# MQTT Client
CLIENT = mqtt.Client()

def main():
    """
    Example application that opens a device that has been exposed to the
    network with ser2sock or similar serial-to-IP software.
    """

    try:
        print("Connecting to MQTT Broker.", flush=True)
        if CONFIG['mqtt_user'] != "":
            CLIENT.username_pw_set(CONFIG['mqtt_user'],
                                   password=CONFIG['mqtt_pass'])
        CLIENT.connect(CONFIG['mqtt_addr'], CONFIG['mqtt_port'], 60)
        CLIENT.loop_start()
    except Exception as ex:
        print('Exception:', ex)
        return

    try:
        print("Connecting to AlarmDecoder.", flush=True)
        # Retrieve an AD2 device that has been exposed with ser2sock
        device = AlarmDecoder(SocketDevice(interface=(CONFIG['alarm_addr'],
                                                      CONFIG['alarm_port'])))

        # Set up an event handler and open the device
        device.on_zone_fault += handle_zone_fault
        device.on_zone_restore += handle_zone_restore
        device.on_ready_changed += handle_ready_changed
        with device.open():
            while True:
                time.sleep(1)

    except Exception as ex:
        print('Exception:', ex)
        return

def handle_zone_fault(device, zone):
    """
    Handles fault signals.
    """
    print("Zone", zone, "Fault.", flush=True)
    CLIENT.publish(CONFIG['mqtt_topic'] + "/" + str(zone), payload="on",
                   qos=0, retain=False)

def handle_zone_restore(device, zone):
    """
    Handles fault signals.
    """
    print("Zone", zone, "Clear.", flush=True)
    CLIENT.publish(CONFIG['mqtt_topic'] + "/" + str(zone), payload="off",
                   qos=0, retain=False)

def handle_ready_changed(device, ready):
    """
    Handles the ready state of the device.
    """
    if ready:
        print("Device Ready", flush=True)
        CLIENT.publish(CONFIG['mqtt_topic'], payload="off", qos=0,
                       retain=False)
    else:
        print("Device Not Ready", flush=True)
        CLIENT.publish(CONFIG['mqtt_topic'], payload="on", qos=0, retain=False)

if __name__ == '__main__':
    main()
