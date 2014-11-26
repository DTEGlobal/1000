"""
Defines the functions needed for 'Pozo' to communicate with 1000 mqtt Broker
"""
import threading

__author__ = 'Cesar'


import mosquitto
import config
import time
import g4Serial

# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("mqttPozo")


# Define event callbacks
def on_connect(mosq, obj, rc):
    config.logging.info("Connected, rc: " + str(rc))
    # Subscribe to any change on any 'Flotador' with qos = 2
    mqttc.subscribe(config.Tanque_Name+'/#', 2)


def on_message(mosq, obj, msg):
    m = msg.topic.split('/')
    # Topic structure: /Pozo_Name/{State}
    # State = 'On' or 'Off'
    if m[1] is 'On':
        config.logging.debug("--> {0} --> On".format(config.Pozo_Name))
        # TODO Insert code here to handle the event of Pozo_Name = On
        return
    elif m[1] is 'Off':
        config.logging.debug("--> {0} --> Off".format(config.Pozo_Name))
        # TODO Insert code here to handle the event of Pozo_Name = Off
        return
    return


def on_publish(mosq, obj, mid):
    config.logging.debug("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    config.logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    config.logging.debug(string)


# Daemons
def publishDaemon():
    time.sleep(config.publishDelay)
    try:
        wellStatus = g4Serial.getED1()
        if wellStatus is '1':
            # TODO Determine what 1 means (On or Off)
            to_publish = 'On'
        elif wellStatus is '0':
            # TODO Determine what 0 means (On or Off)
            to_publish = 'Off'
    except ValueError as e:
        config.logging.error('Pozo Publish - Serial communications failure - {0}'.format(e.message))
    else:
        config.logging.debug("Publishing Pozo data to MQTT Broker")
        mqttc.publish('{0}/{1}'.format(config.Pozo_Name, to_publish))


def mqttPozoDaemon():

    config.logging.info("Pozo Thread Running ...")

    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Connect
    mqttc.connect(config.IP_Tanque, 1883)

    # Network loop
    NL = threading.Thread(target=mqttc.loop_forever)
    NL.daemon = True
    NL.start()

    # Publish loop
    publish = threading.Thread(target=publishDaemon)
    publish.daemon = True
    publish.start()
