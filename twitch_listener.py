"""
Twitch Chat Listener Module
Listens to Twitch channel chat and processes commands.
"""
from twitchio.ext import commands
from typing import Callable, Optional


class TwitchChatBot(commands.Bot):
    """Twitch bot that listens to chat."""
    
    def __init__(self, channel: str, message_handler: Callable[[str, str, bool], None], token: Optional[str] = None):
        """
        Initialize the Twitch chat bot.
        
        Args:
            channel: Twitch channel name
            message_handler: Callback function to handle messages (message, username, is_moderator)
            token: OAuth token for the bot (optional)
        """
        # Use anonymous token if none provided
        if not token:
            token = "anonymous"
        
        super().__init__(
            token=token,
            prefix='',  # We'll handle command parsing ourselves
            initial_channels=[channel]
        )
        
        self.message_handler = message_handler
        self.target_channel = channel
        
    async def event_ready(self):
        """Called when the bot is ready."""
        print(f'Connected to Twitch as {self.nick}')
        print(f'Listening to channel: {self.target_channel}')
    
    async def event_message(self, message):
        """
        Called when a message is received.
        
        Args:
            message: The message object
        """
        # Ignore messages from the bot itself
        if message.echo:
            return
        
        # Extract message details
        content = message.content
        username = message.author.name
        is_moderator = message.author.is_mod or message.author.is_broadcaster
        
        # Process the message
        self.message_handler(content, username, is_moderator)


class TwitchChatListener:
    """Wrapper for the Twitch chat bot."""
    
    def __init__(self, channel: str, message_handler: Callable[[str, str, bool], None], token: Optional[str] = None):
        """
        Initialize the Twitch chat listener.
        
        Args:
            channel: Twitch channel name
            message_handler: Callback function to handle messages
            token: OAuth token (optional)
        """
        self.channel = channel
        self.message_handler = message_handler
        self.token = token
        self.bot = None
        
    def start(self):
        """Start listening to the chat."""
        if not self.channel:
            print("Error: No Twitch channel provided")
            return
        
        print(f"Connecting to Twitch channel: {self.channel}")
        
        try:
            self.bot = TwitchChatBot(self.channel, self.message_handler, self.token)
            self.bot.run()
        except Exception as e:
            print(f"Error in Twitch chat listener: {e}")
    
    def stop(self):
        """Stop listening to the chat."""
        if self.bot:
            print("Twitch chat listener stopped")
