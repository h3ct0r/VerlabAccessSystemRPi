from multiprocessing.connection import Client
import json
import time
import sys
import RPi.GPIO as GPIO
from MFRC522 import MFRC522
import os


def check_uid_access(uid):
    data_path = '../data/data.json'

    if not os.path.isfile(data_path):
        print '[RFID_SERVER]', 'Cannot find RFID data'
        return None

    with open(data_path) as data_file:
        data = json.load(data_file)

    if uid in data.keys():
        return data[uid]

    return None

def main(cfg):
    rfid = MFRC522.MFRC522()

    address_relay = ('localhost', cfg['relay_port'])
    address_lcd = ('localhost', cfg['lcd_port'])
    keep_running = True

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
            print '[RFID_SERVER]', 'UID:', uid, hex_uid

            check_res = check_uid_access(hex_uid)
            if check_res is not None:
                print '[RFID_SERVER]', 'Access granted'
                try:
                    conn_relay = Client(address_relay, authkey=cfg['process_passwd'].encode())
                    conn_relay.send('open_door')
                    conn_relay.close()

                    conn_lcd = Client(address_lcd, authkey=cfg['process_passwd'].encode())
                    conn_lcd.send(["Welcome:", check_res["givenName"]])
                    conn_lcd.close()
                except Exception as e:
                    print '[ERROR]', e

                # TODO: Play access granted
            else:
                print '[RFID_SERVER]', 'Access denied'
                try:
                    conn_lcd = Client(address_lcd, authkey=cfg['process_passwd'].encode())
                    conn_lcd.send([" --- ALERT --- ", " ACCESS DENIED "])
                    conn_lcd.close()
                except Exception as e:
                    print '[ERROR]', e
                # TODO: Play access denied
                pass

            time.sleep(7)

            try:
                conn_lcd = Client(address_lcd, authkey=cfg['process_passwd'].encode())
                conn_lcd.send(["**** VeRLab ****", "Vision&Robotics"])
                conn_lcd.close()
            except Exception as e:
                print '[ERROR]', e

    GPIO.cleanup()
    pass


if __name__ == "__main__":
    with open('../config/config.json') as data_file:
        config = json.load(data_file)

    main(config)

