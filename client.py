import socket
import threading

SERVER_HOST = 'localhost'
SERVER_PORT = 8000

def receive_messages(client_socket):
    # Continuously receive and print messages from server
    while True:
        try:
            data = client_socket.recv(1024)
        except:
            print("[INFO] Connection closed by server")
            client_socket.close()
            break

        if data:
            print(data.decode('utf-8'))

def start_client():
    # Create a new client socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((SERVER_HOST, SERVER_PORT))

    # Start a new thread to receive messages from the server
    receive_thread = threading.Thread(target=receive_messages, args=(client_socket,))
    receive_thread.daemon = True
    receive_thread.start()

    # Continuously read user input and send messages to server
    while True:
        message = input()
        client_socket.sendall(message.encode('utf-8'))

if __name__ == '__main__':
    start_client()

