"""
Configuration file
"""
__author__ = 'Cesar'

import logging

# Logging
logging.basicConfig(format='%(asctime)s - [%(levelname)s]: %(message)s',
                    filename='/home/logs/middleware commands.log',
                    level=logging.DEBUG)

# Device Type - 'Tanque' or 'Pozo'
Device_Type = 'Tanque'

# Device Name - User configurable installation name (no spaces)
Device_Name = 'Tanque_X'


# Information for 'Tanque'
IP_Tanque = '192.168.1.1'
if Device_Type is 'Tanque':
    Tanque_Name = Device_Name
else:
    # If this device is not 'Tanque' then put its name here!
    Tanque_Name = '?'


# Information for 'Pozo'
if Device_Type is 'Pozo':
    Pozo_Name = Device_Name
else:
    # If this device is not 'Pozo' then put its name here!
    Pozo_Name = '?'