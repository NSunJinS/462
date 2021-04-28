import sys
import tty
import termios
import threading
import time
from rpi_rf import RFDevice

class Transmit:
    def __init__(self):
        # GPIO pin 17 transmitter
        self.tx = RFDevice(17)
        self.tx.enable_tx()

    def transmit(self, s):
        # Iterate across string and transmit ASCII chars
        for c in s:
            self.tx.tx_code(ord(c))
            time.sleep(0.01)

    def destructor(self):
        self.tx.cleanup()

class Receive:
    def __init__(self):
        # GPIO pin 27 receiver
        self.rx = RFDevice(27)
        self.rx.enable_rx()

        self.currentTime = None
        self.lastTime = None

    def receive(self):
        lastTime = None
        buff = ""
        while True:
            self.currentTime = self.rx.rx_code_timestamp
            
            # Check for new received characters
            if (self.currentTime != self.lastTime):
                self.lastTime = self.rx.rx_code_timestamp
                code = self.rx.rx_code
                if (code >127):
                    continue
                if (code == 10):
                    return(buff)
                buff += (chr(code))
            time.sleep(0.01)

    def destructor(self):
        self.rx.cleanup()
