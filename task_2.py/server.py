import socket
import threading
from middleware import EventMiddleware

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = {}
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind((self.host, self.port))
        self.middleware = None

    def start(self):
        self.middleware = EventMiddleware()
        self.middleware.subscribe('message_received', self.broadcast_message)
        print(f"Server started, servicing on port {self.port}")
        while True:
            message, address = self.socket.recvfrom(1024)
            message_parts = message.decode().split(": ", 1)
            user_id = message_parts[0]
            message_text = message_parts[1]
            self.middleware.publish('message_received', f"{user_id}: {message_text}")

    def broadcast_message(self, message):
        for client_address in self.clients.values():
            self.socket.sendto(message.encode(), client_address)

    def add_client(self, user_id, client_address):
        self.clients[user_id] = client_address

if __name__ == "__main__":
    server_host = input("Enter server host: ")
    server_port = int(input("Enter server port: "))
    server = Server(server_host, server_port)
    server.start()
