"""
YouTube Chat Listener Module
Listens to YouTube livestream chat and processes commands.
"""
import pytchat
from typing import Callable, Optional
import time


class YouTubeChatListener:
    """Listens to YouTube livestream chat."""
    
    def __init__(self, video_id: str, message_handler: Callable[[str, str, bool], None]):
        """
        Initialize the YouTube chat listener.
        
        Args:
            video_id: YouTube video ID of the livestream
            message_handler: Callback function to handle messages (message, username, is_moderator)
        """
        self.video_id = video_id
        self.message_handler = message_handler
        self.chat = None
        self.running = False
        
    def start(self):
        """Start listening to the chat."""
        if not self.video_id:
            print("Error: No YouTube video ID provided")
            return
        
        print(f"Connecting to YouTube chat for video: {self.video_id}")
        
        try:
            self.chat = pytchat.create(video_id=self.video_id)
            self.running = True
            print("Connected to YouTube chat. Listening for commands...")
            
            while self.running and self.chat.is_alive():
                for chat_data in self.chat.get().sync_items():
                    # Extract message details
                    message = chat_data.message
                    username = chat_data.author.name
                    is_moderator = chat_data.author.isChatModerator or chat_data.author.isChatOwner
                    
                    # Process the message
                    self.message_handler(message, username, is_moderator)
                
                time.sleep(0.1)  # Small delay to prevent excessive CPU usage
                
        except Exception as e:
            print(f"Error in YouTube chat listener: {e}")
        finally:
            self.stop()
    
    def stop(self):
        """Stop listening to the chat."""
        self.running = False
        if self.chat:
            self.chat.terminate()
            print("YouTube chat listener stopped")
