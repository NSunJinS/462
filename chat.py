#Adapted from https://github.com/python-engineer/python-fun
# Permission for private use granted under the MIT License

import threading
import logging
from datetime import datetime
from tkinter import *
from rxtxClass import Transmit, Receive
from statistics import mode
import rsa

BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

        # Start receiver thread
        self.rx = Receive()
        rx_thread = threading.Thread(target=self.receive_msg, args=(self.rx,), daemon=True)
        rx_thread.start()
        self.tx = Transmit()
        self.tx_rsa_key = rsa.RSAKey()
        self.rx_rsa_key = rsa.RSAKey()
        
    def run(self):
#        self.window.protocol("WM_DELETE_WINDOW", lambda e: self.closeEvent(e))
        self.window.bind('<Escape>', lambda e: self.closeEvent(e))
        self.window.mainloop()
        
    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=470, height=500, bg=BG_COLOR)
        
        # head label
        head_label = Label(self.window, bg=BG_COLOR, fg=TEXT_COLOR,
                           text="Raspberry Pi Chatbox Interface", font=FONT_BOLD, pady=10)
        head_label.place(relwidth=1)
        
        # tiny divider
        line = Label(self.window, width=450, bg=BG_COLOR)
        line.place(relwidth=1, rely=0.07, relheight=0.012)
        
        # text widget
        self.text_widget = Text(self.window, width=20, height=2, bg=BG_COLOR, fg=TEXT_COLOR,
                                font=FONT, padx=5, pady=5)
        self.text_widget.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_widget.configure(cursor="arrow", state=DISABLED)
        
        # scroll bar
        scrollbar = Scrollbar(self.text_widget)
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.configure(command=self.text_widget.yview)
        
        # bottom label
        bottom_label = Label(self.window, bg=BG_COLOR, height=100)
        bottom_label.place(relwidth=1, rely=0.85)
        
        # message entry box
        self.msg_entry = Entry(bottom_label, bg=BG_COLOR, fg=TEXT_COLOR, font=FONT)
        self.msg_entry.place(relwidth=0.74, relheight=0.02, rely=0.008, relx=0.011)
        self.msg_entry.focus()
        self.msg_entry.bind("<Return>", self._on_enter_pressed)
        
        # Connect button
        connect_button = Button(bottom_label, text="Connect", font=FONT_BOLD, width=20, bg=BG_COLOR,
                             command=lambda: self._on_connect_pressed(None))
        connect_button.place(relx=0.77, rely=0.001, relheight=0.02, relwidth=0.22)

        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_COLOR,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.021, relheight=0.02, relwidth=0.22)

    def _on_connect_pressed(self, event):
        # Generate RSA key and transmit the public key and n
        # This key will be used to RECEIVE messages because we have the private key
        self.rx_rsa_key.generateKey()

        self.rx.disable()

        self.tx.transmit_key(self.rx_rsa_key)

        self.rx.enable()

        return

    def closeEvent(self, event):
        self.window.destroy()
        self.tx.destructor()
        # self.rx.destructor()

    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if not msg:
            return

        if msg[-1] == "\n":
            msg = msg[0:-2]

        self.msg_entry.delete(0, END)

        if self.tx_rsa_key is None:
            err_msg = "No connection established. Please try connecting first.\n"

            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, err_msg)
            self.text_widget.configure(state=DISABLED)
            self.text_widget.see(END)
            return
        
        msg1 = f"You: {msg}\n"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)

        # Encrypt message
        ctext = (self.tx_rsa_key.encryptMsg(msg.encode('utf-8')))
        
        # Turn off receiver while transmitting
        self.rx.disable()

        self.tx.transmit(ctext)

        self.rx.enable()

    def receive_msg(self,rx):
        print("Ready to receive messages.")
        buffer = ""
        while True:
            
            code = rx.receive()

            # Check for public key transmission
            print(f"Received the following array: {code}")
            if True in [x > 1000000 for x in code[0]]:
                # Verify the key array was received properly
                if len(code) < 3:
                    errMsg = "Key was received incorrectly. Retry!"
                    self.text_widget.configure(state=NORMAL)
                    self.text_widget.insert(END, f"{errMsg}\n")
                    self.text_widget.configure(state = DISABLED)
                    continue

                self.tx_rsa_key = rsa.RSAKey()
                self.tx_rsa_key.n = mode(code[1])
                self.tx_rsa_key.e = mode(code[2])
                print("Key established. You're good to transmit messages now!")
                continue
            
            codeClean = []
            for element in code:
                try:
                    codeClean.append(mode(element))
                except:
                    codeClean.append(element[0])

            plaintext = self.rx_rsa_key.decryptMsg(codeClean)
            print(f"Decrypted the following plaintext: {plaintext}")

            for c in plaintext:
                buffer += chr(c)
            
            self.text_widget.configure(state=NORMAL)
            self.text_widget.insert(END, f"Receive: {buffer}\n")
            self.text_widget.configure(state=DISABLED)

            buffer = ""
            # filename = "logs/log " + datetime.now().strftime("%d.%m.%Y %H:%M") + ".log"
            # fl = open(filename, "w")
            # fl.write(buffer)
            # fl.close()
            #filecounter += 1

if __name__ == "__main__":
    # Init RSA keys
    # rsa.initKey()
    
    app = ChatApplication()
    app.run()