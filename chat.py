#Adapted from https://github.com/python-engineer/python-fun
# Permission for private use granted under the MIT License

import threading
from tkinter import *
from rxtxClass import Transmit, Receive

BG_COLOR = "#FFFFFF"
TEXT_COLOR = "#000000"

FONT = "Helvetica 14"
FONT_BOLD = "Helvetica 13 bold"

class ChatApplication:

    def __init__(self):
        self.window = Tk()
        self._setup_main_window()
        self.tx = Transmit()
        
    def run(self):
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
        
        # send button
        send_button = Button(bottom_label, text="Send", font=FONT_BOLD, width=20, bg=BG_COLOR,
                             command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.02, relwidth=0.22)
     
    def _on_enter_pressed(self, event):
        msg = self.msg_entry.get()
        if not msg:
            return
        
        # Check that msg ends in <RETURN>
        msg = msg + "\n"

        if ord(msg[-1]) != 10:
            print("This message does not end in <RETURN>")

        self.msg_entry.delete(0, END)
        msg1 = f"You: {msg}"
        self.text_widget.configure(state=NORMAL)
        self.text_widget.insert(END, msg1)
        self.text_widget.configure(state=DISABLED)
        
        self.text_widget.see(END)
        self.tx.transmit(msg)

# TODO: Function is not being called by thread
def receive_msg(rx,app):
    print("Ready to receive messages.")
    while True:
        buffer = rx.receive()
        app.text_widget.configure(state=NORMAL)
        app.text_widget.insert(END, f"Receive: {buffer}\n")
        app.text_widget.configure(state=DISABLED)

if __name__ == "__main__":
    # Create receiver obj
    rx = Receive()
    
    app = ChatApplication()
    rx_thread = threading.Thread(target=receive_msg, args=(rx,app,), daemon=True)
    rx_thread.start()
    app.run()
