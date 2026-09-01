from platform import system

from .config import Config

from anthropic import Anthropic


class Application:
    def __init__(self, config: Config):
        self.config = config
        self.running = False
        self.claude_client = None
        self.messages = []
        
    # Add a user message to the conversation and optionally send it to Claude
    def add_user_message(self, messages: list, message: str):
        messages.append({
            "role": "user",
            "content": message
        })
        
        # return self.send_message(messages)
    

    # Add an assistant message to the conversation and optionally send it to Claude
    def add_assistant_message(self, messages: list, message: str):
        messages.append({
            "role": "assistant",
            "content": message
        })
        # return self.send_message(messages)

        
    # Send a message to Claude with optional system message
    def send_message(self, messages: list, system=  None):
        params = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 1024,
            "messages": messages
        }
        
        if system:
            params["system"] = system
        
        if not self.claude_client:
            raise RuntimeError("Claude client is not initialized")

        # Send a message to the Claude API
        response = self.claude_client.messages.create(**params)
        return response.content[0].text


    # Test the Claude API with predefined messages and user input
    def test_claude(self):
        print(f"Testing Claude API with key: {self.config.claude_api_key}")
        #   Initialize the Claude client with the API key
        self.claude_client = Anthropic(api_key=self.config.claude_api_key)
        print("Claude client initialized successfully")

        print("Testing sending a message to Claude...")
        
        self.add_user_message(self.messages, "Define Quantum Computing!")
        response = self.send_message(self.messages)
        
        # Add the assistant's response to the conversation
        self.add_assistant_message(self.messages, response)
        
        self.add_user_message(self.messages, "Write another sentence")
        
        response = self.send_message(self.messages)
        
        self.add_assistant_message(self.messages, response)
        
        print(f"Conversation so far: {self.messages}")
        
    def test_claude_with_input(self):
        self.claude_client = Anthropic(api_key=self.config.claude_api_key)
        
        system= "You are a math tutor who over explains."
        while True:
            user_input = input(">: ")
            self.add_user_message(self.messages, user_input)
            response = self.send_message(self.messages, system)
            self.add_assistant_message(self.messages, response)
            
            ## Print response
            print("---")
            print(response)
            print("---")

    # Test streaming responses from Claude
    def test_response_streaming(self):
        self.claude_client = Anthropic(api_key=self.config.claude_api_key)
        
        self.add_user_message(self.messages, "Write 1 sentence about the importance of AI")
        
        params = {
            "model": "claude-sonnet-4-5-20250929",
            "max_tokens": 1024,
            "messages": self.messages,
            # "stream": True,
        }
        # stream = self.claude_client.messages.create(**params)
        # for event in stream:
        #         print(event)
        with self.claude_client.messages.stream(**params) as stream:
            for text in stream.text_stream:
                # print(text, end="")
                pass
        
        message = stream.get_final_message()
        
        print(f"Final message: {message}")

                
    def start(self):
        print(f"Starting application in {self.config.environment}")
        print(f"Listening on port {self.config.port}")

        self.running = True

        # Test claude code here
        # self.test_claude()
        
        # Test claude code with input
        # self.test_claude_with_input()
        
        # Test streaming responses from Claude
        self.test_response_streaming()

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