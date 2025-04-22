import socket
import threading
import subprocess

# Fungsi untuk menangani klien WebSocket
def handle_client(client_socket):
    request = client_socket.recv(1024)
    print(f"Received: {request}")
    client_socket.send(b"HTTP/1.1 101 Switching Protocols\r\n"
                       b"Upgrade: websocket\r\n"
                       b"Connection: Upgrade\r\n\r\n")
    while True:
        data = client_socket.recv(1024)
        if not data:
            break
        client_socket.send(data)  # echo kembali data
    client_socket.close()

# Setup server WebSocket
def start_server(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Listening on {host}:{port}...")
    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

# Main
if __name__ == "__main__":
    host = "0.0.0.0"  # bind ke semua IP
    port = 8080  # port yang digunakan
    start_server(host, port)
    
