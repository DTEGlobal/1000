"""
Defines the functions needed for 'Pozo' to communicate with 1000 mqtt Broker
"""

__author__ = 'Cesar'


import mosquitto
import config

# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("mqttPozo")


# Define event callbacks
def on_connect(mosq, obj, rc):
    config.logging.info("Connected, rc: " + str(rc))
    # Subscribe to any change on any 'Flotador' with qos = 2
    mqttc.subscribe(config.Tanque_Name+'/#', 2)


def on_message(mosq, obj, msg):
    m = msg.topic.split('/')
    # Topic structure: /Tanque_Name/{Flotador}/{Status}
    # Flotador = 'Flotador_Alto' of 'Flotador_Bajo'
    # Status = 'Up' or 'Down'
    if m[1] is 'Flotador_Alto':
        if m[2] is 'Up':
            config.logging.debug("--> Flotador Alto --> Up")
            # Insert code here to handle the event of Flotador_Alto = Up
            return
        elif m[2] is 'Down':
            config.logging.debug("--> Flotador Alto --> Down")
            # Insert code here to handle the event of Flotador_Alto = Down
            return
    if m[1] is 'Flotador_Bajo':
        if m[2] is 'Up':
            config.logging.debug("--> Flotador Bajo --> Up")
            # Insert code here to handle the event of Flotador_Bajo = Up
            return
        elif m[2] is 'Down':
            config.logging.debug("--> Flotador Bajo --> Down")
            # Insert code here to handle the event of Flotador_Bajo = Down
            return
    return


def on_publish(mosq, obj, mid):
    config.logging.debug("mid: " + str(mid))


def on_subscribe(mosq, obj, mid, granted_qos):
    config.logging.info("Subscribed: " + str(mid) + " " + str(granted_qos))


def on_log(mosq, obj, level, string):
    config.logging.debug(string)


def mqttPozoDaemon():
    # Assign event callbacks
    mqttc.on_message = on_message
    mqttc.on_connect = on_connect
    mqttc.on_publish = on_publish
    mqttc.on_subscribe = on_subscribe

    # Connect
    mqttc.connect(config.IP_Tanque, 1883)

    mqttc.loop_forever()
