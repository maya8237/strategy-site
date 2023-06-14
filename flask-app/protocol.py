from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7
import os

POSSIBLE_MESSAGES = ["UPDATE", "CHART"]
aes_key = None
aes_iv = None


def generate_aes_key_iv():
    global aes_iv, aes_key
    aes_key = os.urandom(16)  # 16 bytes for AES-128
    aes_iv = os.urandom(16)
    return aes_key, aes_iv


def encrypt_rsa(public_key, message):
    ciphertext = public_key.encrypt(message,
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                                 label=None))
    return ciphertext


def decrypt_rsa(private_key, ciphertext):
    plaintext = private_key.decrypt(ciphertext,
                                    padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(),
                                                 label=None))
    return plaintext


def encrypt_aes(key, iv, message):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(message) + encryptor.finalize()
    return ciphertext


def decrypt_aes(key, iv, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    return plaintext


def pad_message(message):
    padder = PKCS7(128).padder()
    padded_data = padder.update(message) + padder.finalize()
    return padded_data


def unpad_message(padded_data):
    unpadder = PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()
    return data


def create_client_connection(client_socket):
    # Receive the server's public key
    server_public_key_bytes = client_socket.recv(2048)

    # Deserialize the server's public key
    server_public_key = serialization.load_pem_public_key(server_public_key_bytes)

    # Generate AES key and IV
    aes_key, aes_iv = generate_aes_key_iv()

    # Encrypt AES key and IV using the server's public key
    encrypted_key = encrypt_rsa(server_public_key, aes_key)
    encrypted_iv = encrypt_rsa(server_public_key, aes_iv)

    # Send the encrypted AES key and IV to the server
    client_socket.sendall(encrypted_key)
    client_socket.sendall(encrypted_iv)


def encode_message(message):
    # Pad the message
    padded_message = pad_message(message.encode())
    # Encrypt the padded message using AES
    encrypted_message = encrypt_aes(aes_key, aes_iv, padded_message)
    return encrypted_message


def decode_message(message):
    # Decrypt the message using AES
    decrypted_message = decrypt_aes(aes_key, aes_iv, message)
    # Unpad the decrypted message
    unpadded_message = unpad_message(decrypted_message)

    decoded_message = unpadded_message.decode()
    return decoded_message


def get_message_with_length(message):
    # Calculate the total length of the message
    total_length = len(message) + 5
    ret_message = f"{total_length:04}|" + message
    return ret_message
