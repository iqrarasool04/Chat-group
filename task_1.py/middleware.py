class EventMiddleware:
    def __init__(self):
        self.events = {}

    def subscribe(self, event, callback):
        if event not in self.events:
            self.events[event] = []
        self.events[event].append(callback)

    def publish(self, event, *args, **kwargs):
        if event in self.events:
            for callback in self.events[event]:
                callback(*args, **kwargs)
