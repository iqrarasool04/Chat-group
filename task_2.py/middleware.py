class EventMiddleware:
    def __init__(self):
        self.events = {}
        self.user_addresses = {}

    def subscribe(self, event, callback):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(callback)

    def publish(self, event, *args, **kwargs):
        if event in self.events:
            for callback in self.events[event]:
                callback(*args, **kwargs)

    def add_user_address(self, user_id, address):
        self.user_addresses[user_id] = address

    def send_message_to_user(self, user_id, message):
        address = self.user_addresses.get(user_id)
        if address:
            self.send_message(address, message)

    def send_message(self, address, message):
        pass
