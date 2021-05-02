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

    def transmit_key(self, key):
        print("Transmitting key")
        self.tx.tx_code(2,1) # specify key transmission
        time.sleep(0.01)
        self.tx.tx_code(10,1)
        time.sleep(0.01)
        self.tx.tx_code(key.n,1)
        time.sleep(0.01)
        self.tx.tx_code(10,1)
        time.sleep(0.01)
        self.tx.tx_code(key.e,1)
        time.sleep(0.01)
        self.tx.tx_code(10,1)
        time.sleep(0.01)
        self.tx.tx_code(23,1)

    def transmit(self, s):
        # Iterate across string and transmit ASCII chars
        for c in s:
            self.tx.tx_code(c,1)
            time.sleep(0.01)
            self.tx.tx_code(10,1)
            time.sleep(0.01)
        #Send ascii ETB (End of Transmission block) 
        self.tx.tx_code(23,1)

    def destructor(self):
        self.tx.cleanup()

class Receive:
    def __init__(self):
        # GPIO pin 27 receiver
        self.rx = RFDevice(27)
        self.rx.enable_rx()

        self.currentTime = None
        self.lastTime = None

    def disable(self):
        self.rx.disable_rx()
    
    def enable(self):
        self.rx.enable_rx()

    def receive(self):
        msgBuff = []
        charBuff = []
        while True:
            self.currentTime = self.rx.rx_code_timestamp
            
            # Check for new received characters
            if (self.currentTime != self.lastTime):
                self.lastTime = self.rx.rx_code_timestamp
                protocol = self.rx.rx_proto

                if (protocol != 1):
                    continue

                code = self.rx.rx_code
                
                print(code)
                # Due to repeated chars, only return if buffer contains chars other than <RETURN>
                if (code == 10 and len(charBuff) > 0):
                    msgBuff.append(charBuff)
                    charBuff = []
                    continue
                elif (code == 10):
                    continue
                if (code == 23 and len(msgBuff) > 0):
                    return msgBuff
                elif( code == 23):
                    continue
                charBuff.append(code)
            time.sleep(0.01)

    def destructor(self):
        self.rx.cleanup()
