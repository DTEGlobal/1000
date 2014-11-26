"""
Defines the functions needed for 'Tanque' to communicate with 1000 mqtt Broker
"""
import threading

__author__ = 'Cesar'


import mosquitto
import config
import g4Serial
import time

# Create Mosquitto Client object
mqttc = mosquitto.Mosquitto("mqttTanque")


# Define event callbacks
def on_connect(mosq, obj, rc):
    config.logging.info("Connected, rc: " + str(rc))
    # Subscribe to any change on 'Pozo' state
    mqttc.subscribe(config.Pozo_Name+'/#', 2)


def on_message(mosq, obj, msg):
    m = msg.topic.split('/')
    # Topic structure: /Tanque_Name/{Flotador}/{Status}
    # Flotador = 'Flotador_Alto' of 'Flotador_Bajo'
    # Status = 'Up' or 'Down'
    if m[1] is 'Flotador_Alto':
        if m[2] is 'Up':
            config.logging.debug("--> Flotador Alto --> Up")
            # TODO Insert code here to handle the event of Flotador_Alto = Up
            return
        elif m[2] is 'Down':
            config.logging.debug("--> Flotador Alto --> Down")
            # TODO Insert code here to handle the event of Flotador_Alto = Down
            return
    if m[1] is 'Flotador_Bajo':
        if m[2] is 'Up':
            config.logging.debug("--> Flotador Bajo --> Up")
            # TODO Insert code here to handle the event of Flotador_Bajo = Up
            return
        elif m[2] is 'Down':
            config.logging.debug("--> Flotador Bajo --> Down")
            # TODO Insert code here to handle the event of Flotador_Bajo = Down
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
        temp = g4Serial.getED1()
        if temp is '1':
            # TODO Determine what 1 means (Up or Down)
            to_publish = 'Up'
        elif temp is '0':
            # TODO Determine what 0 means (Up or Down)
            to_publish = 'Down'
    except ValueError as e:
        config.logging.error('Tanque Publish - Serial communications failure - {0}'.format(e.message))
    else:
        config.logging.debug("Publishing Tanque data to MQTT Broker")
    mqttc.publish('{0}/Flotador_Alto/{1}'.format(config.Tanque_Name, to_publish))

    try:
        temp = g4Serial.getED1()
        if temp is '1':
            # TODO Determine what 1 means (Up or Down)
            to_publish = 'Up'
        elif temp is '0':
            # TODO Determine what 0 means (Up or Down)
            to_publish = 'Down'
    except ValueError as e:
        config.logging.error('Tanque Publish - Serial communications failure - {0}'.format(e.message))
    else:
        config.logging.debug("Publishing Tanque data to MQTT Broker")
    mqttc.publish('{0}/Flotador_Bajo/{1}'.format(config.Tanque_Name, to_publish))


def mqttTanqueDaemon():

    config.logging.info("Tanque Thread Running ...")

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


