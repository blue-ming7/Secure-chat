import unittest
from encryption import encrypt_message, decrypt_message
from auth import authenticate

class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt(self):
        msg = "Hello Secure Chat"
        encrypted = encrypt_message(msg)
        decrypted = decrypt_message(encrypted)
        self.assertEqual(msg, decrypted)

    def test_decrypt_invalid_token(self):
        with self.assertRaises(Exception):
            decrypt_message(b"invalidtoken")
class TestAuth(unittest.TestCase):
    def test_valid_user(self):
        self.assertTrue(authenticate("ali", "ali123"))
        self.assertTrue(authenticate("sara", "sara123"))

    def test_invalid_user(self):
        self.assertFalse(authenticate("ali", "wrongpass"))
        self.assertFalse(authenticate("nonexistent", "nopass"))
if __name__ == "__main__":
    unittest.main()
