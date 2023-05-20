# Python standard libraries
from functools import wraps
import socket
import base64
import os
import threading

# Third-party libraries
from flask import render_template, abort, Blueprint, send_from_directory, request, current_app
from flask_login import (
    current_user,
    login_required
)

from protocol import *
from models import Admin

admin_tools = Blueprint('admin_tools', __name__)


# returns if user received is an admin
def is_admin(user):
    if not user.is_authenticated:
        return False
    admin = Admin.query.filter_by(email=user.email).first()
    return admin is not None


# load default variables and functions
def template(file, **kwargs):
    kwargs['is_admin'] = is_admin
    return render_template(file, **kwargs)


# defines a decorator that checks if the current user is an admin
def admin_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        else:
            if not is_admin(current_user):
                abort(403)
        return func(*args, **kwargs)

    return decorated_function


def recieve_image_data(s):
    # Receive the encrypted image data in chunks
    chunks = []
    while True:
        chunk = s.recv(1024)
        if not chunk:
            break
        chunks.append(chunk)

    encrypted_data = b''.join(chunks)

    decrypted_data = decode_message(encrypted_data)
    return decrypted_data


def save_image(message):
    filename = message[2]
    unevaluated_image_data = message[3]
    images_dir = "images"
    # Convert the string representation to a base64 string
    base64_string = unevaluated_image_data.encode('utf-8')  # Convert to bytes
    image_data = base64.b64decode(base64_string)  # Decode base64 bytes

    file_route = f"{images_dir}/{filename}"
    # Save the decrypted image data as a PNG file
    with open(file_route, 'wb') as file:
        file.write(image_data)
    return filename


@admin_tools.route("/graphs", methods=["GET", "POST"])
@admin_required
@login_required
def graphs():
    if request.method == "POST":
        image_filenames = []
        team_num = request.form.get("team_num")
        query = request.form.get("query")  # includes ALL

        # Function to handle each request in a separate thread
        def handle_request(query):
            # Connect to the socket server
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_address = ('localhost', 5001)
            s.connect(server_address)

            # Send the request for an image
            message = f"CHART|{team_num}|{query}"
            full_message = get_message_with_length(message)
            s.sendall(encode_message(full_message))

            # Receive the image data
            decrypted_data = recieve_image_data(s)
            message_parts = decrypted_data.split("|", 3)
            filename = save_image(message_parts)

            # Add the filename to the list of image filenames
            image_filenames.append(filename)

            # Close the socket
            s.close()

        if query == 'ALL':
            # List of possible queries
            POSSIBLE_QUERIES = ["CONES_ALL", "CONES_PER", "FLOATS_ALL", "FLOATS_PER"]

            # Create a thread for each request
            threads = []
            for query in POSSIBLE_QUERIES:
                thread = threading.Thread(target=handle_request, args=(query,))
                threads.append(thread)
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()

        else:
            thread = threading.Thread(target=handle_request, args=(query,))
            thread.start()
            thread.join()

        return template('image.html', image_filenames=image_filenames)

    return template("graphs_form.html")


@admin_tools.route('/images/<filename>')
@admin_required
@login_required
def display_image(filename):
    image_dir = 'images'  # Directory containing the images
    return send_from_directory(image_dir, filename)


@admin_tools.route('/update')
@admin_required
@login_required
def update_data():
    # Connect to the socket server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('localhost', 5001)
    s.connect(server_address)

    full_message = get_message_with_length('UPDATE')
    s.sendall(encode_message(full_message))
    encrypted_data = ""
    while True:
        try:
            encrypted_data = s.recv(1024)  # Receive encrypted data

            if not encrypted_data:
                break

        except socket.error as e:
            if e.errno == errno.WSAENOTSOCK:  # Check if the error is due to not a socket
                print("Not a valid socket.")
            else:
                print("Socket error occurred:", e)
            break

        finally:
            decrypted_data = decode_message(encrypted_data)
            message_parts = decrypted_data.split("|", 2)
            update_info = message_parts[2]
            message = ""

            if update_info == "ERROR":
                message = "There was an error."
            elif update_info == "SOON":
                message = "Please try again soon."
            elif update_info == "UPDATED":
                message = "The information was updated."

            return render_template('message.html', message=message)
