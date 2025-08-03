import unittest
import socket
import threading
from encryption import encrypt_message, decrypt_message
from auth import authenticate

TEST_PORT = 6060
TEST_SERVER = "localhost"
TEST_ADDR = (TEST_SERVER, TEST_PORT)
DISCONNECT_MESSAGE = "!DISCONNECT"

def handle_client_for_test(conn):
    try:
        conn.send(encrypt_message("Username:"))
        username = decrypt_message(conn.recv(1024))
        conn.send(encrypt_message("Password:"))
        password = decrypt_message(conn.recv(1024))

        if not authenticate(username, password):
            conn.send(encrypt_message("Authentication Failed!"))
            conn.close()
            return

        conn.send(encrypt_message(f"Welcome {username}!"))

        while True:
            encrypted_msg = conn.recv(2048)
            if not encrypted_msg:
                break
            msg = decrypt_message(encrypted_msg)
            if msg == DISCONNECT_MESSAGE:
                break
            conn.send(encrypt_message(f"ECHO: {msg}"))

    finally:
        conn.close()

class TestServerClientCommunication(unittest.TestCase):

    def setUp(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(TEST_ADDR)
        self.server.listen()

        def server_thread():
            conn, _ = self.server.accept()
            handle_client_for_test(conn)

        self.thread = threading.Thread(target=server_thread, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.close()

    def test_auth_and_echo(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(TEST_ADDR)

        prompt = decrypt_message(client.recv(1024))
        self.assertEqual(prompt, "Username:")

        client.send(encrypt_message("sara"))

        prompt = decrypt_message(client.recv(1024))
        self.assertEqual(prompt, "Password:")

        client.send(encrypt_message("sara123"))

        welcome = decrypt_message(client.recv(2048))
        self.assertIn("Welcome sara", welcome)

        test_msg = "Hello Server"
        client.send(encrypt_message(test_msg))

        echo = decrypt_message(client.recv(2048))
        self.assertEqual(echo, f"ECHO: {test_msg}")

        client.send(encrypt_message(DISCONNECT_MESSAGE))
        client.close()

if __name__ == "__main__":
    unittest.main()
