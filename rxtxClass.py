import sys
import tty
import termios
import threading
import time
from rpi_rf import RFDevice

class Transmit:
    def __init__(self):
        self.tx = RFDevice(17)
        self.tx.enable_tx()

    def transmit(self, s):
        for c in s:
            self.tx.tx_code(ord(c))
            time.sleep(0.01)

    def destructor():
        self.tx.cleanup()

class Receive:
    def __init__(self):
        self.rx = RFDevice(27)
        self.rx.enable_rx()

    def receive(self):
        lastTime = None
        buff = ""
        while True:
            currentTime = self.rx.rx_code_timestamp
            if (
                    currentTime != lastTime and
                    (lastTime is None or currentTime - lastTime > 350000)
            ):
                lastTime = self.rx.rx_code_timestamp
                if (self.rx.rx_code == 10):
                    return(buff)
                buff += chr(self.rx.rx_code)
            time.sleep(0.01)

    def destructor():
        self.rx.cleanup()
