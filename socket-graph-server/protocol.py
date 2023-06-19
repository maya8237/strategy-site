from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import base64

POSSIBLE_MESSAGES = ["UPDATE", "CHART"]
IMAGE_FOLDER = "images/"


def get_message_with_length(message):
    # Calculate the total length of the message
    total_length = len(message) + 5
    ret_message = f"{total_length:04}|" + message
    return ret_message


def create_chart_send_message(filename, status):
    data = ""
    if status is not None:
        file_route = f"{IMAGE_FOLDER}/{filename}.png"
        with open(file_route, 'rb') as file:
            data = file.read()

        # Convert PNG bytes to a base64-encoded string
        data = base64.b64encode(data).decode('utf-8')

    message = f"UPLOAD|{filename}.png|{data}"

    return message


def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def encrypt_rsa(public_key, message):
    ciphertext = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return ciphertext


def decrypt_rsa(private_key, ciphertext):
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext


def pad_message(message):
    padder = PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    return padded_data


def unpad_message(padded_data):
    unpadder = PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


class Connection:
    def __init__(self):
        # Generate RSA key pair
        private_key, public_key = generate_rsa_keypair()
        self.private_key = private_key
        self.public_key = public_key
        self.aes_key = None
        self.aes_iv = None

    def encrypt_aes(self, message):
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(self.aes_iv))
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(message) + encryptor.finalize()
        return ciphertext

    def decrypt_aes(self, ciphertext):
        cipher = Cipher(algorithms.AES(self.aes_key), modes.CBC(self.aes_iv))
        decryptor = cipher.decryptor()
        plaintext = decryptor.update(ciphertext) + decryptor.finalize()
        return plaintext

    def create_connection_with_client(self, client_socket):
        # Serialize the public key
        public_key_bytes = self.public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        # Send the public key to the client
        client_socket.sendall(public_key_bytes)

        # Receive the encrypted AES key and IV from the client
        encrypted_key = client_socket.recv(1024)
        encrypted_iv = client_socket.recv(1024)

        # Ensure the ciphertext length matches the key size
        key_size = self.private_key.key_size // 8  # Convert key size from bits to bytes
        if len(encrypted_key) != key_size or len(encrypted_iv) != key_size:
            raise ValueError("Invalid ciphertext length.")

        # Decrypt the AES key and IV using RSA private key
        self.aes_key = decrypt_rsa(self.private_key, encrypted_key)
        self.aes_iv = decrypt_rsa(self.private_key, encrypted_iv)

    def encode_message(self, message):
        # Pad the message
        padded_message = pad_message(message.encode())

        # Encrypt the padded message using AES
        encrypted_message = self.encrypt_aes(padded_message)
        return encrypted_message

    def decode_message(self, message):
        # Decrypt the message using AES
        decrypted_message = self.decrypt_aes(message)

        # Unpad the decrypted message
        unpadded_message = unpad_message(decrypted_message)

        decoded_message = unpadded_message.decode()
        return decoded_message
