from .config import Config

from anthropic import Anthropic


class Application:
    def __init__(self, config: Config):
        self.config = config
        self.running = False
        self.claude_client = None

    def send_message(self):
        # if not self.claude_client:
        #     raise RuntimeError("Claude client is not initialized")

        # Send a message to the Claude API
        response = self.claude_client.messages.create(
            model="claude-sonnet-4-5-20250929",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": "Hello, Claude!"
                }
            ]
          )
        return response.content[0].text

    def test_claude(self):
        print(f"Testing Claude API with key: {self.config.claude_api_key}")
        #   Initialize the Claude client with the API key
        self.claude_client = Anthropic(api_key=self.config.claude_api_key)
        print("Claude client initialized successfully")

        print("Testing sending a message to Claude...")
        response = self.send_message()
        print(f"Received response: {response}")


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