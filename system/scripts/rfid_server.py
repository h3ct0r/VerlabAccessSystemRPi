#!/usr/bin/env python

from multiprocessing.connection import Client
import json
import time
import sys
import RPi.GPIO as GPIO
from MFRC522 import MFRC522
import os
import socket
from threading import Thread
import logging
import logging.handlers


def check_uid_access(uid):
    data_path = '/var/doorsystem/data/data.json'

    if not os.path.isfile(data_path):
        print '[RFID_SERVER]', 'Cannot find RFID data'
        return None

    with open(data_path) as data_file:
        data = json.load(data_file)

    for k,v in data.items():
        if v['accessToken'] == str(uid):
            return v

    return None

def send_socket_msg(address, key, msg):
    try:
        conn_lcd = Client(address, authkey=key)
        conn_lcd.send(msg)
        conn_lcd.close()
    except Exception as e:
        print '[ERROR]', e
    pass

def main(cfg):
    logger = logging.getLogger('RFID_SRV')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    rfid = MFRC522.MFRC522()

    address_relay = ('localhost', cfg['relay_port'])
    address_lcd = ('localhost', cfg['lcd_port'])
    keep_running = True
    
    logger.info('RFID server started and waiting for RFID tags')

    while keep_running:
        # Scan for cards
        (status, tag_type) = rfid.MFRC522_Request(rfid.PICC_REQIDL)

        # If a card is found get UID
        if status == rfid.MI_OK:
            (status, uid) = rfid.MFRC522_Anticoll()

        # If we have the UID, continue
        if status == rfid.MI_OK:
            # Prepare UID, delete last bit (inconsistency with previous readings??)
            if len(uid) > 2:
                uid.pop()

            hex_uid = ''.join(format(x, 'x') for x in uid)
            logger.debug('UID: {} {}'.format(uid, hex_uid))

            check_res = check_uid_access(hex_uid)
            if check_res is not None:
                logger.info('Access granted')
                try:
                    t1 = Thread(target=send_socket_msg, args=(address_relay, cfg['process_passwd'].encode(), 'open_door'))
                    t1.setDaemon(True)
                    t1.start()
                    
                    #t2 = Thread(target=send_socket_msg, args=(address_lcd, cfg['process_passwd'].encode(), ["Welcome:", check_res["givenName"]]))
                    #t2.setDaemon(True)
                    #t2.start()
                except Exception as e:
                    if str(e) != "":
                        logger.debug(e)
                # TODO: Play access granted
            else:
                logger.debug('Access denied')
                #t1 = Thread(target=send_socket_msg, args=(address_lcd, cfg['process_passwd'].encode(), [" --- ALERT --- ", " ACCESS DENIED "]))
                #t1.setDaemon(True)
                #t1.start()
                # TODO: Play access denied
                pass
            
            time.sleep(1)
        else:
            time.sleep(0.2)           

    GPIO.cleanup()
    pass


if __name__ == "__main__":
    with open('/var/doorsystem/config/config.json') as data_file:
        config = json.load(data_file)

    main(config)

