"""
Defines the functions needed for 'Tanque' to communicate with 1000 mqtt Broker
"""

__author__ = 'Cesar'


import mosquitto
import config

# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("mqttTanque")


# Define event callbacks
def on_connect(mosq, obj, rc):
    config.logging.info("Connected, rc: " + str(rc))
    # Subscribe to any change on 'Pozo' state
    mqttc.subscribe(config.Pozo_Name+'/#', 2)


def on_message(mosq, obj, msg):
    m = msg.topic.split('/')
    # Topic structure: /Pozo_Name/{State}
    # State = 'On' or 'Off'
    if m[1] is 'On':
        config.logging.debug("--> {0} --> On".format(config.Pozo_Name))
        # Insert code here to handle the event of Pozo_Name = On
        return
    elif m[1] is 'Off':
        config.logging.debug("--> {0} --> Off".format(config.Pozo_Name))
        # Insert code here to handle the event of Pozo_Name = Off
        return
    return


def on_publish(mosq, obj, mid):
    config.logging.debug("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    config.logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    config.logging.debug(string)


def mqttTanqueDaemon():
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Connect
    mqttc.connect(config.IP_Tanque, 1883)

    mqttc.loop_forever()
