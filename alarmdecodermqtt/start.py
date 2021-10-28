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

# Stores the Panel Attribute Flags
PANEL_ATTRIBS = {}

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
        tls_version = TLS_VER_OPTIONS.get(
            CONFIG['mqtt_broker']['tls_version'], None
        )
        if tls_version is not None:
            addl_tls_kwargs['tls_version'] = tls_version
        cert_reqs = CERT_REQ_OPTIONS.get(
            CONFIG['mqtt_broker']['cert_reqs'], None
        )
        if cert_reqs is not None:
            addl_tls_kwargs['cert_reqs'] = cert_reqs
        certfile = CONFIG['mqtt_broker'].get('certfile', None)
        if 'certfile' == '':
            certfile = None
        keyfile = CONFIG['mqtt_broker'].get('keyfile', None)
        if 'keyfile' == '':
            keyfile = None
        ciphers = CONFIG['mqtt_broker'].get('ciphers', None)
        if 'ciphers' == '':
            ciphers = None
        try:
            CLIENT.tls_set(ca_certs=CONFIG['mqtt_broker']['ca_cert'],
                           certfile=certfile,
                           keyfile=keyfile,
                           ciphers=ciphers,
                           **addl_tls_kwargs)
        except FileNotFoundError as e:
            print("Cannot locate a SSL/TLS file = %s." % e, flush=True)
            print("certfile=%s, keyfile=%s, ciphers=%s" % (certfile,
                  keyfile, ciphers))
            return

        except ssl.SSLError as e:
            print("SSL/TLS Config error = %s." % e, flush=True)
            return

    # Set our last will
    CLIENT.will_set(CONFIG['mqtt_topic'] + "/available", payload="offline",
                    qos=0, retain=True)

    # Setup our connect callback
    def on_connect(client, userdata, flags, result):
        if result == 0:
            client.publish(CONFIG['mqtt_topic'] + "/available",
                           payload="online", qos=0, retain=True)
        else:
            print("MQTT connection failed")
    CLIENT.on_connect = on_connect

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
    device = AlarmDecoder(SocketDevice(interface=(
        CONFIG['alarmdecoder']['alarm_addr'],
        CONFIG['alarmdecoder']['alarm_port']
    )))

    # Set up an event handler and open the device
    device.on_zone_fault += handle_zone_fault
    device.on_zone_restore += handle_zone_restore
    device.on_message += handle_message

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

    Also set zones as expanders if defined by user.
    """
    if (zone in CONFIG['expander_zones'] and
            not device.get_zone(zone).expander):
        device.get_zone(zone).expander = True
    print("Zone", zone, "Fault.", flush=True)
    CLIENT.publish(CONFIG['mqtt_topic'] + "/zone/" + str(zone), payload="ON",
                   qos=0, retain=CONFIG['retain'])

def handle_zone_restore(device, zone):
    """
    Handles fault signals.
    """
    print("Zone", zone, "Clear.", flush=True)
    CLIENT.publish(CONFIG['mqtt_topic'] + "/zone/" + str(zone), payload="OFF",
                   qos=0, retain=CONFIG['retain'])

def handle_message(device, message):
    """
    Processes messages received from the panel.

    Each message contains all of these flags.  While on_ready, on_arm, and ...
    events are nice, it is more convenient to get all of the flags at once.
    With all of the flags, we can publish a json packet with all of the flags
    which allows them to be used as json attributes for the panel in addition
    to being available for use as individual entities.
    """
    global PANEL_ATTRIBS
    attributes = {"ready": message.ready,
                  "armed_away": message.armed_away,
                  "armed_home": message.armed_home,
                  "zone_bypassed": message.zone_bypassed,
                  "ac_power": message.ac_power,
                  "chime_on": message.chime_on,
                  "alarm_event_occurred": message.alarm_event_occurred,
                  "alarm_sounding": message.alarm_sounding,
                  "battery_low": message.battery_low,
                  "entry_delay_off": message.entry_delay_off,
                  "fire_alarm": message.fire_alarm,
                  "check_zone": message.check_zone,
                  "perimeter_only": message.perimeter_only,
                  "system_fault": message.system_fault}
    # A Simple comparison of dicts works really well in this case
    if attributes != PANEL_ATTRIBS:
        PANEL_ATTRIBS = attributes.copy()
        print("Updating panel flags.", flush=True)
        attributes['timestamp'] = str(message.timestamp)  # Not used in compare
        # Add the state attribute, matches states available in HomeAssistant
        state = ""
        if message.alarm_sounding:
            state = "triggered"
        elif message.armed_away:
            if message.zone_bypassed:
                state = "armed_custom_bypass"
            else:
                state = "armed_away"
        elif message.armed_home:
            if message.zone_bypassed:
                state = "armed_custom_bypass"
            else:
                state = "armed_home"
        else:
            state = "disarmed"
        attributes['state'] = state
        CLIENT.publish(CONFIG['mqtt_topic'] + "/panel",
                       payload=json.dumps(attributes), qos=0,
                       retain=CONFIG['retain'])

if __name__ == '__main__':
    main()
