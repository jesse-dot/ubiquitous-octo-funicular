"""
Main Application
Entry point for the Chat Control Tool.
"""
import yaml
import sys
import os
from command_parser import CommandParser
from youtube_listener import YouTubeChatListener
from twitch_listener import TwitchChatListener


def load_config(config_path: str = 'config.yaml') -> dict:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        Configuration dictionary
    """
    # Check for local override
    local_config = 'config.local.yaml'
    if os.path.exists(local_config):
        config_path = local_config
        print(f"Using local configuration: {local_config}")
    
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing configuration file: {e}")
        sys.exit(1)


def main():
    """Main application entry point."""
    print("=" * 60)
    print("Chat Control Tool - Livestream Chat to Windows Controller")
    print("=" * 60)
    print()
    
    # Load configuration
    config = load_config()
    
    # Initialize command parser
    parser = CommandParser(config)
    
    # Define message handler
    def handle_message(message: str, username: str, is_moderator: bool):
        """Handle incoming chat messages."""
        if parser.is_command(message):
            print(f"[{username}{'*' if is_moderator else ''}]: {message}")
            result = parser.parse_and_execute(message, username, is_moderator)
            if result:
                print(f"  -> {result}")
    
    # Determine platform and start appropriate listener
    platform = config.get('platform', 'youtube').lower()
    
    try:
        if platform == 'youtube':
            video_id = config.get('youtube', {}).get('video_id', '')
            if not video_id:
                print("Error: YouTube video_id not configured")
                print("Please edit config.yaml and add your YouTube live video ID")
                sys.exit(1)
            
            listener = YouTubeChatListener(video_id, handle_message)
            listener.start()
            
        elif platform == 'twitch':
            channel = config.get('twitch', {}).get('channel', '')
            token = config.get('twitch', {}).get('token', '')
            
            if not channel:
                print("Error: Twitch channel not configured")
                print("Please edit config.yaml and add your Twitch channel name")
                sys.exit(1)
            
            listener = TwitchChatListener(channel, handle_message, token)
            listener.start()
            
        else:
            print(f"Error: Unknown platform '{platform}'")
            print("Supported platforms: youtube, twitch")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\nShutting down...")
        sys.exit(0)


if __name__ == '__main__':
    main()
