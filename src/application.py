from .config import Config


class Application:
    def __init__(self, config: Config):
        self.config = config
        self.running = False
    
    def test_claude(self):
        print(f"Testing Claude API with key: {self.config.claude_api_key}")

        

    def start(self):
        print(f"Starting application in {self.config.environment}")
        print(f"Listening on port {self.config.port}")

        self.running = True

        # Test claude code here
        self.test_claude()

        # Initialize things here:
        # database
        # queues
        # workers
        # HTTP server
        # etc.

    def stop(self):
        print("Shutting down application...")

        self.running = False

        # Close:
        # database connections
        # workers
        # sockets
        # etc.