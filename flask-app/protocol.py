from dotenv import load_dotenv
import os
from cryptography.fernet import Fernet
import base64
POSSIBLE_MESSAGES = ["UPDATE", "CHART"]


def cipher_suite1():
    load_dotenv()
    encryption_key = os.environ.get("ENCRYPTION_KEY")
    cipher_suite = Fernet(base64.b64decode(encryption_key))
    return cipher_suite


def encode_message(message):
    cipher_suite = cipher_suite1()
    encrypted_bytes = cipher_suite.encrypt(repr(message).encode('utf-8'))
    # encoded_message = base64.b64encode(encrypted_bytes)
    return encrypted_bytes


def decode_message(message):
    cipher_suite = cipher_suite1()
    # encoded_message = base64.b64decode(message.decode())
    decrypted_message = cipher_suite.decrypt(message).decode('utf-8')
    if decrypted_message[0] == "'" and decrypted_message[-1] == "'":
        decrypted_message = decrypted_message[1:-1]
    return decrypted_message


def get_message_with_length(message):
    # Calculate the total length of the message
    total_length = len(message) + 5
    ret_message = f"{total_length:04}|" + message
    return ret_message
