from multiprocessing.connection import Client
import json
import time
import sys
import os


def main(cfg):
    address_lcd = ('localhost', 8888)
    try:
        conn_lcd = Client(address_lcd, authkey='passwd'.encode())
        conn_lcd.send(["Welcome:", 'aaaa'])
        conn_lcd.close()
    except Exception as e:
        print '[ERROR]', e


if __name__ == "__main__":
    main(None)

