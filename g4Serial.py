"""
Implements G4 serial communications
"""

__author__ = 'Cesar'

import config
import serial
import time
import mqttTanque
import mqttPozo
import bitState


def errorCleanUp(error):
    
    global Rx

    Rx = False
    port.flushOutput()
    config.logging.warning("TxST: Error->[%s]", error)


def SendCommand():

    global port, Command, Rx, commandResponse, E

    config.logging.info("SendCommand Thread Running ...")
    port = serial.Serial("/dev/ttyAMA0", baudrate=19200, timeout=1)

    port.flushOutput()

    waitingForCommand = False

    while True:
        # mqtt client loop for watchdog keep alive
        time.sleep(1)
        if Command is not '':
            command = Command+"\x0D"
            waitingForCommand = True
            Rx = True
        else:
            command = "00E\x0D"
            Rx = True

        data = command[:-1]
        config.logging.debug("TxST: Tx Data->[{0}]".format(data))
        port.write(command)
        while Rx:
            try:
                MessageFromSerial = port.readline()
                # Remove last 3 chars (CR LF)
                data = MessageFromSerial[:-2]
                config.logging.debug("RxST: Rx Data->[{0}]".format(data))
                # Check Rx contents
                if waitingForCommand:
                    Rx = False
                    if MessageFromSerial == '':
                        commandResponse = 'Error: Time Out'
                    else:
                        commandResponse = MessageFromSerial[:-2]
                    config.logging.info('Command Response: %s', commandResponse)
                    waitingForCommand = False
                    Command = ''
                elif MessageFromSerial[3] == 'E':
                    Rx = False
                    config.logging.debug('E = {0}'.format(MessageFromSerial))
                    E = MessageFromSerial
                else:
                    errorCleanUp(MessageFromSerial)

            except serial.SerialException as e:
                errorCleanUp(e)

            except IndexError as i:
                errorCleanUp(i)
                

def getED1():
    global E
    # TODO locate EDx on E
    return bitState.getBitState(E[14:16], 2)


def getED2():
    global E
    # TODO locate EDx on E
    return bitState.getBitState(E[14:16], 2)
