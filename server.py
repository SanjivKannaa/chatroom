import socket
import threading

SERVER_HOST = '0.0.0.0'  # Bind to all available interfaces
SERVER_PORT = 8000

clients = []

def handle_client(client_socket, address):
    # Add client to list of connected clients
    clients.append(client_socket)
    print(f"[INFO] New connection from {address}")

    while True:
        # Receive incoming message from client
        try:
            data = client_socket.recv(1024)
        except:
            print(f"[INFO] Connection closed from {address}")
            clients.remove(client_socket)
            client_socket.close()
            break

        # Broadcast message to all connected clients
        if data:
            message = f"[{address[0]}:{address[1]}]: {data.decode('utf-8')}"
            print(message)
            for c in clients:
                if c != client_socket:
                    c.sendall(message.encode('utf-8'))

def start_server():
    # Create a new server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Bind the socket to a specific interface and port
    server_socket.bind((SERVER_HOST, SERVER_PORT))

    # Start listening for incoming connections
    server_socket.listen()

    print(f"[INFO] Server listening on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        # Wait for a new connection
        client_socket, address = server_socket.accept()

        # Create a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
        client_thread.daemon = True
        client_thread.start()

if __name__ == '__main__':
    start_server()

