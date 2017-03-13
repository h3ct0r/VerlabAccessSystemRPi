#!/usr/bin/env python

from multiprocessing.connection import Listener
import json
import time
import sys
import RPi.GPIO as GPIO
import logging
import logging.handlers


def main(cfg):
    logger = logging.getLogger('RELAY_SRV')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(cfg['gpio_pin_relay'], GPIO.OUT)
    GPIO.output(cfg['gpio_pin_relay'], GPIO.HIGH)
    address = ('localhost', cfg['relay_port'])
    keep_running = True
    
    logger.info('Relay server started and waiting for connections')
    
    while keep_running:
        listener = Listener(address, authkey=cfg['process_passwd'].encode())
        conn = listener.accept()
        logger.debug('connection accepted from {}'.format(listener.last_accepted))

        try:
            while True:
                if conn.poll():
                    msg = conn.recv()
                    logger.debug('Received: {}'.format(msg))

                    if msg == 'shutdown':
                        conn.close()
                        keep_running = False
                        listener.close()
                        break
                    if msg == 'open_door':
                        logger.debug('Opening door: {}'.format(time.time()))
                        for i in xrange(cfg['relay_pulses']):
                            GPIO.output(cfg['gpio_pin_relay'], GPIO.LOW)
                            time.sleep(cfg['relay_ms_between_pulses'])
                            GPIO.output(cfg['gpio_pin_relay'], GPIO.HIGH)
                            time.sleep(cfg['relay_ms_between_pulses'])

        except Exception as e:
            if str(e) != "":
                logger.error(e)
            listener.close()

    GPIO.cleanup()
    listener.close()
    pass

if __name__ == "__main__":
    with open('/home/pi/Git/DoorAccessRpi/system/config/config.json') as data_file:
        config = json.load(data_file)

    main(config)
