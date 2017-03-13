#!/usr/bin/env python

from multiprocessing.connection import Listener
from threading import Thread
from Queue import Queue
import json
import time
import sys
import smbus
import socket
import fcntl
import struct
import logging
import logging.handlers
import subprocess


class LCDControl:

    def __init__(self, i2c_address=0x3f, is_backlight_on=True):
        self.i2c_address = i2c_address
        self.lcd_width = 16
        self.lcd_chr = 1
        self.lcd_cmd = 0
        self.lcd_line_1 = 0x80
        self.lcd_line_2 = 0xC0
        self.lcd_line_3 = 0x94
        self.lcd_line_4 = 0xD4

        self.lcd_backlight = 0x00
        if is_backlight_on:
            self.lcd_backlight = 0x08

        self.enable_bit = 0b00000100
        self.e_pulse = 0.0005
        self.e_delay = 0.0005

        # Rev 1 Pi uses 0, Rev 2 uses 1
        self.bus = smbus.SMBus(1)
        self.init()
        pass

    def init(self):
        self.send_byte(0x33, self.lcd_cmd)  # 110011 Initialise
        self.send_byte(0x32, self.lcd_cmd)  # 110010 Initialise
        self.send_byte(0x06, self.lcd_cmd)  # 000110 Cursor move direction
        self.send_byte(0x0C, self.lcd_cmd)  # 001100 Display On,Cursor Off, Blink Off
        self.send_byte(0x28, self.lcd_cmd)  # 101000 Data length, number of lines, font size
        self.send_byte(0x01, self.lcd_cmd)  # 000001 Clear display
        time.sleep(self.e_delay)

    def send_byte(self, bits, mode):
        # Send byte to data pins
        # bits = the data
        # mode = 1 for data
        #        0 for command

        bits_high = mode | (bits & 0xF0) | self.lcd_backlight
        bits_low = mode | ((bits << 4) & 0xF0) | self.lcd_backlight

        # High bits
        self.bus.write_byte(self.i2c_address, bits_high)
        self.toggle_enable(bits_high)

        # Low bits
        self.bus.write_byte(self.i2c_address, bits_low)
        self.toggle_enable(bits_low)

    def toggle_enable(self, bits):
        # Toggle enable
        time.sleep(self.e_delay)
        self.bus.write_byte(self.i2c_address, (bits | self.enable_bit))
        time.sleep(self.e_pulse)
        self.bus.write_byte(self.i2c_address, (bits & ~self.enable_bit))
        time.sleep(self.e_delay)

    def send_string(self, message, line):
        # Send string to display
        message = message.ljust(self.lcd_width, " ")
        self.send_byte(line, self.lcd_cmd)
        for i in range(self.lcd_width):
            self.send_byte(ord(message[i]), self.lcd_chr)

    def send_string_list(self, msg):
        if len(msg) != 2:
            return

        l1 = msg[0]
        self.send_string(l1, self.lcd_line_1)

        l2 = msg[1]
        self.send_string(l2, self.lcd_line_2)


def get_ip_address(ifname):
    p = subprocess.Popen("ifconfig {} | grep 'inet addr' | cut -d ':' -f 2 | cut -d ' ' -f 1".format(ifname), stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out, err = p.communicate()
    return out.strip()
    
def reset_screen(logger, lcd, queue):
	last_update = 0
	is_dirty = True
	q_time = None
	
	while(True):
		try:
			q_time = queue.get_nowait()
			if q_time is not None:
				last_update = q_time
				is_dirty = True
		except Exception, e:
			q_time = None
		
		ctime = float(time.time())
		timediff = abs(ctime - last_update)
		
		if is_dirty and timediff > 5:
			logger.debug('Resetting screen isdirty:{}, ctime{}, timediff:{}'.format(is_dirty, ctime, timediff))
			is_dirty = False
			lcd.send_string_list(["**** VeRLab ****", "Vision& Robotics"])
			
		time.sleep(1)
		pass
	pass

def main(cfg):
    logger = logging.getLogger('RFID_SRV')
    logger.setLevel(logging.DEBUG)
    handler = logging.handlers.SysLogHandler(address = '/dev/log')
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    
    logger.debug('Starting lcd control...')
    lcd = LCDControl()
    address = ('localhost', cfg['lcd_port'])
    keep_running = True
    logger.debug('Sending init LCD...')
    ip_addr= get_ip_address('eth0')
    logger.debug('IP: {}'.format(ip_addr))
    lcd.send_string_list(["Init LCD server", ip_addr])
    
    # Start reset thread
    queue = Queue()
    queue.put(int(time.time()))
    t1 = Thread(target=reset_screen, args=(logger, lcd, queue,))
    t1.setDaemon(True)
    t1.start()
    
    logger.info('LCD server started and waiting for connections')
    
    while keep_running:
        listener = Listener(address, authkey=cfg['process_passwd'].encode())
        conn = listener.accept()
        logger.debug('connection accepted from {}'.format(listener.last_accepted))

        try:
            while True:
                if conn.poll():
                    msg = conn.recv()
                    logger.debug('Received: {}'.format(msg))

                    if not isinstance(msg, list):
                        if msg == 'shutdown':
                            conn.close()
                            keep_running = False
                            listener.close()
                            break
                        else:
                            logger.debug('Not a list or shutdown msg')
                            break

                    queue.put(float(time.time()))

                    lcd.send_string_list(msg)
        except Exception as e:
            if str(e) != "":
                logger.error(e)
            listener.close()

    listener.close()
    lcd.send_byte(0x01, lcd.lcd_cmd)
    pass

if __name__ == "__main__":
    with open('/home/pi/Git/DoorAccessRpi/system/config/config.json') as data_file:
        config = json.load(data_file)

    main(config)
