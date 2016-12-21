from multiprocessing.connection import Listener
import json
import time
import sys
import smbus
import socket
import fcntl
import struct

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
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])


def main(cfg):

    lcd = LCDControl()
    address = ('localhost', cfg['lcd_port'])
    keep_running = True
    lcd.send_string_list(["Init LCD server", get_ip_address('eth0')])

    while keep_running:
        listener = Listener(address, authkey=cfg['process_passwd'].encode())
        conn = listener.accept()
        print '[LCD_SRV]', 'connection accepted from', listener.last_accepted

        try:
            while True:
                if conn.poll():
                    msg = conn.recv()
                    print '[LCD_SRV]', 'Received:', msg

                    if not isinstance(msg, list):
                        if msg == 'shutdown':
                            conn.close()
                            keep_running = False
                            listener.close()
                            break
                        else:
                            print '[ERROR]', 'Not a list or shutdown msg'
                            break

                    lcd.send_string_list(msg)
        except Exception as e:
            print '[ERROR]', e
            listener.close()

    listener.close()
    lcd.send_byte(0x01, lcd.lcd_cmd)
    pass

if __name__ == "__main__":
    with open('../config/config.json') as data_file:
        config = json.load(data_file)

    main(config)
