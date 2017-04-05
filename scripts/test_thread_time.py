#!/usr/bin/env python

from multiprocessing.connection import Listener
from threading import Thread
from Queue import Queue
import json
import time
import sys
import socket
import fcntl
import struct


def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])
    
def reset_msg(queue):
    print 'starting reset msg ...'
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
        timediff = ctime - last_update
        if is_dirty and timediff > 5:
            print 'is_dirty:{}, ctime:{}, timediff:{}'.format(is_dirty, ctime, timediff)
            print 'reset screen...'
            is_dirty = False
            
        time.sleep(1)
        pass
    pass

def main(cfg):
    address = ('localhost', 8888)
    keep_running = True
    print ["Init LCD server", '127.0.0.1']
    
    # Start reset thread
    queue = Queue()
    queue.put(int(time.time()))
    t1 = Thread(target=reset_msg, args=(queue,))
    t1.setDaemon(True)
    t1.start()
    
    print '[LCD_SRV]', 'LCD server started and waiting for connections'
    
    while keep_running:
        listener = Listener(address, authkey='passwd'.encode())
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
                    
                    queue.put(int(time.time()))
                    
                    print msg
        except Exception as e:
            print '[ERROR]', e
            listener.close()

    listener.close()
    pass

if __name__ == "__main__":
    main(None)