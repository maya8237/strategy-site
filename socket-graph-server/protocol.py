from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.padding import PKCS7

aes_key = None
aes_iv = None
POSSIBLE_MESSAGES = ["UPDATE", "CHART"]
IMAGE_FOLDER = "images/"


def generate_rsa_keypair():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key


def get_message_with_length(message):
    # Calculate the total length of the message
    total_length = len(message) + 5
    ret_message = f"{total_length:04}|" + message
    return ret_message


def create_chart_send_message(filename):
    file_route = f"{IMAGE_FOLDER}/{filename}.png"
    with open(file_route, 'rb') as file:
        data = file.read()

    # Convert PNG bytes to a base64-encoded string
    data = base64.b64encode(data).decode('utf-8')

    message = f"UPLOAD|{filename}.png|{data}"

    return message


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


def create_connection(client_socket):
    # Generate RSA key pair
    private_key, public_key = generate_rsa_keypair()

    # Serialize the public key
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    # Send the public key to the client
    client_socket.sendall(public_key_bytes)

    # Receive the encrypted AES key and IV from the client
    encrypted_key = client_socket.recv(1024)
    encrypted_iv = client_socket.recv(1024)

    global aes_iv, aes_key

    # Decrypt the AES key and IV using RSA private key
    aes_key = decrypt_rsa(private_key, encrypted_key)
    aes_iv = decrypt_rsa(private_key, encrypted_iv)


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
