from cryptography.fernet import Fernet

KEY = b'WH1ez2FWdTRgm2CmQGVSXV5YVGkniUhV73KaJ5GY5uU='
fernet = Fernet(KEY)

def encrypt_message(message: str) -> bytes:

    return fernet.encrypt(message.encode())

def decrypt_message(token: bytes) -> str:

    return fernet.decrypt(token).decode()


