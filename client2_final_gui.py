import socket
import threading
import tkinter as tk
from tkinter import simpledialog, messagebox
from encryption import encrypt_message, decrypt_message
from cryptography.fernet import Fernet

KEY = b'WH1ez2FWdTRgm2CmQGVSXV5YVGkniUhV73KaJ5GY5uU='
fernet = Fernet(KEY)

def encrypt_message(message: str) -> bytes:
    return fernet.encrypt(message.encode())

def decrypt_message(token: bytes) -> str:
    return fernet.decrypt(token).decode()

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

class ChatClient:
    def __init__(self, master):
        self.master = master
        master.title("Secure Chat Client")

        #custom icon
        self.icon = tk.PhotoImage(file="logo.drawio.png")
        master.iconphoto(False, self.icon)

        self.chat_log = tk.Text(master, state='disabled', width=50, height=20)
        self.chat_log.pack()

        self.msg_entry = tk.Entry(master, width=40)
        self.msg_entry.pack(side=tk.LEFT, padx=10)
        self.msg_entry.bind("<Return>", self.send_message)

        self.send_button = tk.Button(master, text="Send", command=self.send_message)
        self.send_button.pack(side=tk.LEFT)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect(ADDR)
        except:
            messagebox.showerror("Connection error", "Unable to connect to server.")
            master.quit()
            return

        self.authenticate()
        threading.Thread(target=self.listen_for_messages, daemon=True).start()

    def authenticate(self):
        prompt = decrypt_message(self.client.recv(1024))
        username = simpledialog.askstring("Login", prompt)
        self.client.send(encrypt_message(username))

        prompt = decrypt_message(self.client.recv(1024))
        password = simpledialog.askstring("Login", prompt, show='*')
        self.client.send(encrypt_message(password))

        response = decrypt_message(self.client.recv(2048))
        if "Failed" in response:
            messagebox.showerror("Authentication failed", response)
            self.master.quit()
        else:
            self.append_message(response)

    def listen_for_messages(self):
        while True:
            try:
                encrypted_msg = self.client.recv(2048)
                msg = decrypt_message(encrypted_msg)
                self.append_message(msg)
            except:
                self.append_message("Connection lost.")
                break

    def send_message(self, event=None):
        msg = self.msg_entry.get()
        if msg:
            self.client.send(encrypt_message(msg))
            if msg == DISCONNECT_MESSAGE:
                self.master.quit()
            self.msg_entry.delete(0, tk.END)

    def append_message(self, msg):
        self.chat_log.config(state='normal')
        self.chat_log.insert(tk.END, msg + "\n")
        self.chat_log.config(state='disabled')
        self.chat_log.see(tk.END)

def main():
    root = tk.Tk()
    app = ChatClient(root)
    root.mainloop()

if __name__ == "__main__":
    main()
