import socket
import errno
import cryptography
from cryptography.fernet import Fernet
import time
import protocol
from sqlalchemy import create_engine, engine
import threading
import base64
import os
from graphs import *
from sheets_api import get_service
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# Create the engine to connect to the database
engine = create_engine('sqlite:///instance/games.db')

# Create all tables defined in your models
Base.metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

last_update_time = None
load_dotenv()

# Create a socket server instance
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = os.environ.get("SOCKET_IP")
server.bind((server_address, int(os.environ.get("SOCKET_PORT"))))
server.listen(1)


def update_data():
    global last_update_time
    message = "UPDATE|SOON"
    current_time = time.time()
    try:
        if last_update_time is None or current_time - last_update_time >= 120:
            # Two minutes have passed since last update, or it is the first data update
            last_update_time = current_time

            service = get_service()

            load_dotenv()
            sheet_id = os.environ.get('GOOGLE_SPREADSHEET_ID')
            sheet_name = os.environ.get('GOOGLE_SPREADSHEET_NAME')

            # Get number of rows with game info
            checking_range_name = os.environ.get('GOOGLE_CHECKING_RANGE')
            result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=checking_range_name).execute()
            data = result.get('values', [])

            total_num_rows = len(data)
            num_rows = total_num_rows - 1

            # Create a session object
            session = Session()

            # Get the count of rows in the GameData table
            row_count = session.query(GameData).count()

            # Get starting index in list of rows of unadded data
            rows_data_to_add = num_rows - row_count  # Number of rows to retrieve
            if rows_data_to_add != 0:
                start_row_index = total_num_rows - rows_data_to_add

                # Calculate the end row index
                end_row_index = start_row_index + rows_data_to_add - 1

                # Construct the range string
                range_string = f'{sheet_name}!A{start_row_index}:AA{end_row_index}'  # Adjust the range as per your columns

                # Call the Sheets API to retrieve the rows
                result = service.spreadsheets().values().get(spreadsheetId=sheet_id, range=range_string).execute()
                values = result.get('values', [])

                # ADD DATA TO DATABASE
                for row in values:
                    while len(row) < 27:
                        row.append('')

                    game_data = GameData(row)
                    game_data.add_to_game_db(session)

            session.close()
            message = "UPDATE|UPDATED"

    except:
        message = "UPDATE|ERROR"
        print("Sheet Update Error")

    finally:
        full_message = protocol.get_message_with_length(message)

        encoded_message = protocol.encode_message(full_message)
        client_socket.send(encoded_message)
        print(message)


def send_chart_to_client(client_socket, team_num, query):
    filename = generate_filename(team_num, query)
    print("filename =" + filename)
    message = "UPLOAD|ERROR"  # IN CASE OF AN ERROR
    print("Chart Error")
    try:
        create_graph(filename, team_num, query)
        message = protocol.create_chart_send_message(filename)

    finally:
        full_message = protocol.get_message_with_length(message)

        encoded_message = protocol.encode_message(full_message)
        client_socket.sendall(encoded_message)


def handle_client_connection(client_socket):
    while True:
        try:
            encrypted_data = client_socket.recv(1024)  # Receive the rest of the encrypted data

            if not encrypted_data:
                break

            message = protocol.decode_message(encrypted_data)
            message = message.split("|", 3)
            print('Decrypted message:', message)

            # if message not in protocol.POSSIBLE_MESSAGES return error

            if message[1] == "UPDATE":
                update_data()

            if message[1] == "CHART":
                team_num = message[2]
                query = message[3]
                send_chart_to_client(client_socket, team_num, query)

        except socket.error as e:
            if e.errno == errno.WSAENOTSOCK:  # Check if the error is due to not a socket
                print("Not a valid socket.")
            else:
                print("Socket error occurred:", e)
            break

        finally:
            # Close the socket connection
            client_socket.close()


if __name__ == '__main__':
    print('Server started. Listening for connections...')
    while True:
        try:
            client_socket, address = server.accept()
            print('Client connected:', address)

            # Compare client's address with the server's address
            if address[0] == server_address:
                client_thread = threading.Thread(target=handle_client_connection, args=(client_socket,))
                client_thread.start()
            else:
                print('Connection rejected: Client not from the same host as the server.')

        except KeyboardInterrupt:
            s.close()
            break

