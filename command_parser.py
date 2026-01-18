"""
Command Parser Module
Parses chat messages and executes corresponding commands.
"""
import time
from typing import Dict, Any, Optional, Callable
from windows_controller import WindowsController


class CommandParser:
    """Parses and executes chat commands."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the command parser.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config
        self.controller = WindowsController()
        self.command_prefix = config.get('command_prefix', '!')
        self.commands = config.get('commands', {})
        self.last_command_time = 0
        self.cooldown_enabled = config.get('security', {}).get('enable_cooldown', True)
        self.cooldown_seconds = config.get('security', {}).get('cooldown_seconds', 2)
        
    def is_command(self, message: str) -> bool:
        """
        Check if a message is a command.
        
        Args:
            message: The chat message
            
        Returns:
            True if message starts with command prefix
        """
        return message.strip().startswith(self.command_prefix)
    
    def can_execute_command(self) -> bool:
        """
        Check if a command can be executed based on cooldown.
        
        Returns:
            True if cooldown has passed
        """
        if not self.cooldown_enabled:
            return True
        
        current_time = time.time()
        if current_time - self.last_command_time >= self.cooldown_seconds:
            self.last_command_time = current_time
            return True
        
        return False
    
    def is_user_allowed(self, username: str, is_moderator: bool = False) -> bool:
        """
        Check if a user is allowed to execute commands.
        
        Args:
            username: Username of the chat user
            is_moderator: Whether the user is a moderator
            
        Returns:
            True if user is allowed
        """
        security = self.config.get('security', {})
        
        # Check if moderator-only mode is enabled
        if security.get('require_moderator', False) and not is_moderator:
            return False
        
        # Check allowed users list
        allowed_users = self.config.get('allowed_users', [])
        if allowed_users and username not in allowed_users:
            return False
        
        return True
    
    def parse_and_execute(self, message: str, username: str = "unknown", is_moderator: bool = False) -> Optional[str]:
        """
        Parse and execute a command from a chat message.
        
        Args:
            message: The chat message
            username: Username of the sender
            is_moderator: Whether the user is a moderator
            
        Returns:
            Response message or None
        """
        if not self.is_command(message):
            return None
        
        if not self.is_user_allowed(username, is_moderator):
            print(f"User {username} is not allowed to execute commands")
            return None
        
        if not self.can_execute_command():
            print("Command on cooldown")
            return None
        
        # Remove prefix and parse
        message = message.strip()[len(self.command_prefix):]
        parts = message.split(maxsplit=1)
        command_name = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ""
        
        # Check if command exists in config
        if command_name not in self.commands:
            print(f"Unknown command: {command_name}")
            return None
        
        command_config = self.commands[command_name]
        action = command_config.get('action')
        
        print(f"Executing command: {command_name} (action: {action}) by {username}")
        
        # Execute the appropriate action
        success = False
        
        if action == 'open':
            program = command_config.get('program', '')
            success = self.controller.open_program(program)
            
        elif action == 'mouse_move':
            # Parse x y coordinates
            try:
                coords = args.split()
                if len(coords) >= 2:
                    x, y = int(coords[0]), int(coords[1])
                    success = self.controller.move_mouse(x, y)
            except ValueError:
                print("Invalid coordinates for mouse_move")
                
        elif action == 'mouse_click':
            button = args.strip().lower() if args else 'left'
            if button not in ['left', 'right', 'middle']:
                button = 'left'
            success = self.controller.mouse_click(button)
            
        elif action == 'mouse_doubleclick':
            success = self.controller.mouse_click('left', clicks=2)
            
        elif action == 'key_press':
            if args:
                success = self.controller.press_key(args.strip())
                
        elif action == 'type':
            if args:
                success = self.controller.type_text(args)
        
        if success:
            return f"Command {command_name} executed successfully"
        else:
            return f"Command {command_name} failed"
