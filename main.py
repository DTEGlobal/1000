"""
Entry point to the program
"""

__author__ = 'Cesar'

import threading
import mqttPozo
import mqttTanque
import config

if config.Device_Type is 'Tanque':
    mqttTanqueDaemon = threading.Thread(target=mqttTanque.mqttTanqueDaemon)
    mqttTanqueDaemon.daemon = True
    mqttTanqueDaemon.start()

elif config.Device_Type is 'Pozo':
    mqttPozoDaemon = threading.Thread(target=mqttPozo.mqttPozoDaemon)
    mqttPozoDaemon.daemon = True
    mqttPozoDaemon.start()

while True:
    a = 0  # Do nothing
