import errno
import socket
import base64
import protocol

"""
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
server_address = ('localhost', 5001)
client_socket.connect(server_address)
message = "0021|CHART|3075|CONES_ALL"

print('Connected to the server.')
client_socket.send(protocol.encode_message(message))
# Receive data from the server
while True:
    num_str = ""
    data = client_socket.recv(1024)
    if data:
        # Print the received message
        decrypted_data = protocol.decode_message(data)
        print("Received:", decrypted_data)
        while decrypted_data != "|":
            data = client_socket.recv(1024)
            decrypted_data = protocol.decode_message(data)
            num_str += decrypted_data



# Close the client socket
client_socket.close()
print('Connection closed.')
"""

# Connect to the socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 5001)
s.connect(server_address)

message = "0021|CHART|3075|CONES_ALL"
s.sendall(protocol.encode_message(message))

# Receive the encrypted image data in chunks
chunks = []
data_recieved = False
counter = 0
while True:
    chunk = s.recv(1024)
    if not chunk:
        break
    chunks.append(chunk)

encrypted_data = b''.join(chunks)

decrypted_data = protocol.decode_message(encrypted_data)
message = decrypted_data.split("|", 3)
filename = message[2]
unevaluated_image_data = message[3]

# Convert the string representation to a base64 string
base64_string = unevaluated_image_data.encode('utf-8')  # Convert to bytes
image_data = base64.b64decode(base64_string)  # Decode base64 bytes

file_route = ""
# Save the decrypted image data as a PNG file
with open(filename, 'wb') as file:
    file.write(image_data)

# Close the socket
s.close()
