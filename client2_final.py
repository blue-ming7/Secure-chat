import socket
import threading
from encryption import encrypt_message, decrypt_message

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def listen_for_messages(client):
    while True:
        try:
            encrypted_msg = client.recv(2048)
            msg = decrypt_message(encrypted_msg)
            print(f"\n{msg}")
        except:
            print("Connection closed.")
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)

    # Authentication
    prompt = decrypt_message(client.recv(1024))
    username = input(prompt + " ")
    client.send(encrypt_message(username))

    prompt = decrypt_message(client.recv(1024))
    password = input(prompt + " ")
    client.send(encrypt_message(password))

    # Check welcome or fail message
    response = decrypt_message(client.recv(2048))
    if "Failed" in response:
        print(response)
        client.close()
        return
    else:
        print(response)

    thread = threading.Thread(target=listen_for_messages, args=(client,), daemon=True)
    thread.start()

    while True:
        msg = input()
        if msg == DISCONNECT_MESSAGE:
            client.send(encrypt_message(DISCONNECT_MESSAGE))
            break
        client.send(encrypt_message(msg))

    client.close()

if __name__ == "__main__":
    main()
