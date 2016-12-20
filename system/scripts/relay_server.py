from multiprocessing.connection import Listener
import json
import time
import sys
import RPi.GPIO as GPIO

def main(cfg):
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(cfg['gpio_pin_relay'], GPIO.OUT)
    GPIO.output(cfg['gpio_pin_relay'], GPIO.LOW)
    address = ('localhost', 6001)  # family is deduced to be 'AF_INET'
    keep_running = True

    while keep_running:
        listener = Listener(address, authkey=cfg['process_passwd'].encode())
        conn = listener.accept()
        print '[RELAY_SRV]', 'connection accepted from', listener.last_accepted

        try:
            while True:
                if conn.poll():
                    msg = conn.recv()
                    print '[RELAY_SRV]', 'Received:', msg

                    if msg == 'shutdown':
                        conn.close()
                        keep_running = False
                        listener.close()
                        break
                    if msg == 'open_door':
                        print '[RELAY_SRV]', 'Opening door', time.time()
                        for i in xrange(cfg['relay_pulses']):
                            GPIO.output(cfg['gpio_pin_relay'], GPIO.HIGH)
                            time.sleep(cfg['relay_ms_between_pulses'])
                            GPIO.output(cfg['gpio_pin_relay'], GPIO.LOW)
                            time.sleep(cfg['relay_ms_between_pulses'])

        except Exception as e:
            print '[ERROR]', e
            listener.close()

    GPIO.cleanup()
    listener.close()
    pass

if __name__ == "__main__":
    with open('../config/config.json') as data_file:
        config = json.load(data_file)

    main(config)
