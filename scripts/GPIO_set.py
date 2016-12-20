#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import RPi.GPIO as GPIO
import time

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.cleanup()
    GPIO.setup(4, GPIO.OUT)
    GPIO.output(4, GPIO.LOW)
    while(True):
        GPIO.output(4, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(4, GPIO.LOW)
        time.sleep(1)


if __name__ == "__main__":
    main()
