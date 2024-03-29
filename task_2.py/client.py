import socket
import threading
from middleware import EventMiddleware

class Client:
    def __init__(self, username, server_host, server_port, user_id):
        self.username = username
        self.server_host = server_host
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(('0.0.0.0', 0))  
        self.middleware = None
        self.user_id = user_id

    def connect(self):
        self.middleware = EventMiddleware()
        self.middleware.subscribe('message_received', self.on_message_received)
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()
        print(f"Connected to {self.server_host}:{self.server_port}")

    def receive_messages(self):
        while True:
            message, _ = self.socket.recvfrom(1024)
            self.middleware.publish('message_received', message.decode())

    def send_message(self, message):
        self.socket.sendto(message.encode(), (self.server_host, self.server_port))

    def on_message_received(self, message):
        print(message)

    def start(self):
        self.connect()
        while True:
            message = input()
            if message.startswith("@"):
                parts = message.split(" ", 1)
                user_id = parts[0][1:]
                message = parts[1]
                self.middleware.send_message_to_user(user_id, f"{self.username}: {message}")
            else:
                self.send_message(f"{self.username}: {message}")

if __name__ == "__main__":
    username = input("Enter your username: ")
    server_host = input("Enter server host: ")
    server_port = int(input("Enter server port: "))
    user_id = input("Enter your user ID: ")
    client = Client(username, server_host, server_port, user_id)
    client.start()
