import sys
import tty
import termios
import threading
import time
from rpi_rf import RFDevice

class Transmit:
    def __init__(self):
        tx = RFDevice(17)
        tx.enable_tx()

    def transmit(s):
        For char c in s:
            tx.tx_code(c)
            time.sleep(0.01)

    def destructor():
        tx.cleanup()

class Receive:
    def __init__(self):
        rx = RFDevice(27)
        rx.enable_rx()

    def receive():
        lastTime = None
        buff = ""
        while True:
            currentTime = rx.rx_code_timestamp
            if (
                    currentTime != lastTime and
                    (lastTime is None or currentTime - lastTime > 350000)
            ):
                lastTime = rx.rx_code_timestamp
                if (rx.rx_code == 10):
                    return(buff)
                buff += chr(rx.rx_code)
            time.sleep(0.01)

    def destructor():
        rx.cleanup()
