import time
import json
import ssl
from alarmdecoder import AlarmDecoder
from alarmdecoder.devices import SocketDevice
import paho.mqtt.client as mqtt

# Load Config
f = open('/data/options.json')
CONFIG = json.load(f)
f.close()

# MQTT Client
CLIENT = mqtt.Client()

# map for Paho acceptable TLS cert request options
CERT_REQ_OPTIONS = {'none': ssl.CERT_NONE, 'required': ssl.CERT_REQUIRED}

# Map for Paho acceptable TLS version options. Some options are
# dependent on the OpenSSL install so catch exceptions
TLS_VER_OPTIONS = dict()
try:
    TLS_VER_OPTIONS['tls'] = ssl.PROTOCOL_TLS
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['tlsv1'] = ssl.PROTOCOL_TLSv1
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['tlsv11'] = ssl.PROTOCOL_TLSv1_1
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['tlsv12'] = ssl.PROTOCOL_TLSv1_2
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['sslv2'] = ssl.PROTOCOL_SSLv2
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['sslv23'] = ssl.PROTOCOL_SSLv23
except AttributeError:
    pass
try:
    TLS_VER_OPTIONS['sslv3'] = ssl.PROTOCOL_SSLv3
except AttributeError:
    pass

def main():
    """
    Example application that opens a device that has been exposed to the
    network with ser2sock or similar serial-to-IP software.
    """

    print("Connecting to MQTT Broker.", flush=True)
    if 'mqtt_user' in CONFIG['mqtt_broker']:
        print("Using Username/Password.", flush=True)
        CLIENT.username_pw_set(CONFIG['mqtt_broker']['mqtt_user'],
                               password=CONFIG['mqtt_broker']['mqtt_pass'])

    if 'ca_cert' in CONFIG['mqtt_broker']:
        print("Using SSL/TLS Connection.", flush=True)
        addl_tls_kwargs = {}
        if 'tls_version' in CONFIG['mqtt_broker']:
            tls_version = TLS_VER_OPTIONS.get(
                CONFIG['mqtt_broker']['tls_version'], None
            )
            if tls_version is not None:
                addl_tls_kwargs['tls_version'] = tls_version
        if 'cert_reqs' in CONFIG['mqtt_broker']:
            cert_reqs = CERT_REQ_OPTIONS.get(
                CONFIG['mqtt_broker']['cert_reqs'], None
            )
            if cert_reqs is not None:
                addl_tls_kwargs['cert_reqs'] = cert_reqs
        certfile = None
        if 'certfile' in CONFIG['mqtt_broker']:
            certfile = CONFIG['mqtt_broker']['certfile']
        keyfile = None
        if 'keyfile' in CONFIG['mqtt_broker']:
            keyfile = CONFIG['mqtt_broker']['keyfile']
        ciphers = None
        if 'ciphers' in CONFIG['mqtt_broker']:
            ciphers = CONFIG['mqtt_broker']['ciphers']
        try:
            CLIENT.tls_set(ca_certs=CONFIG['mqtt_broker']['ca_cert'],
                           certfile=certfile,
                           keyfile=keyfile,
                           ciphers=ciphers,
                           **addl_tls_kwargs)
        except FileNotFoundError as e:
            print("Cannot locate a SSL/TLS file = %s." % e, flush=True)
            return

        except ssl.SSLError as e:
            print("SSL/TLS Config error = %s." % e, flush=True)
            return

    try:
        CLIENT.connect(CONFIG['mqtt_broker']['mqtt_addr'],
                       CONFIG['mqtt_broker']['mqtt_port'], 60)
    except Exception as ex:
        print('Unable to connect to MQTT Broker:', ex)
        return

    # Start the loop
    CLIENT.loop_start()

    print("Connecting to AlarmDecoder.", flush=True)

    # Retrieve an AD2 device that has been exposed with ser2sock
    device = AlarmDecoder(SocketDevice(interface=(CONFIG['alarm_addr'],
                                                  CONFIG['alarm_port'])))

    # Set up an event handler and open the device
    device.on_zone_fault += handle_zone_fault
    device.on_zone_restore += handle_zone_restore
    device.on_ready_changed += handle_ready_changed

    try:
        with device.open():
            while True:
                # This is the main loop, we stay here until terminated
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
