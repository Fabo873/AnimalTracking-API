import os
from cryptography.fernet import Fernet

class Encryption():
    key = os.environ['ENCRYPTION_KEY'].encode()
    f = Fernet(key)

    @classmethod
    def encode(cls, message: str) -> str:
        message = message.encode()
        token = cls.f.encrypt(message)
        return token.decode()

    @classmethod
    def decode(cls, message: str) -> str:
        message = message.encode()
        token = cls.f.decrypt(message)
        return token.decode()

    @classmethod
    def compare(cls, decrypted: str, encrypted: str) -> bool:
        encrypted = encrypted.encode()
        message = cls.f.decrypt(encrypted).decode()
        return decrypted == message
