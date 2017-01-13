# A GPS tracker library
# This is a neater and more useful implementation of Sixfab's demo code

import serial
import time
import pynmea2
import threading

class GPS(object):
    """An all-powerful GPS interface class"""
