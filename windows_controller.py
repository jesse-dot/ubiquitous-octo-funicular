"""
Windows Control Module
Handles all Windows-specific actions like program launching, mouse control, and keyboard input.
"""
import pyautogui
import subprocess
import os
import time
from typing import List, Optional


class WindowsController:
    """Controls Windows system actions via chat commands."""
    
    def __init__(self):
        """Initialize the Windows controller."""
        # Set PyAutoGUI safety settings
        pyautogui.FAILSAFE = True  # Move mouse to corner to abort
        pyautogui.PAUSE = 0.1  # Small delay between actions
        
    def open_program(self, program_path: str) -> bool:
        """
        Open a program by path or name.
        
        Args:
            program_path: Path to the executable or program name
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Try to run the program
            subprocess.Popen(program_path, shell=True)
            return True
        except Exception as e:
            print(f"Error opening program {program_path}: {e}")
            return False
    
    def move_mouse(self, x: int, y: int, duration: float = 0.5) -> bool:
        """
        Move the mouse to specified coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            duration: Time to take moving (seconds)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            screen_width, screen_height = pyautogui.size()
            # Clamp coordinates to screen bounds
            x = max(0, min(x, screen_width - 1))
            y = max(0, min(y, screen_height - 1))
            
            pyautogui.moveTo(x, y, duration=duration)
            return True
        except Exception as e:
            print(f"Error moving mouse to ({x}, {y}): {e}")
            return False
    
    def mouse_click(self, button: str = "left", clicks: int = 1) -> bool:
        """
        Perform a mouse click.
        
        Args:
            button: Which button to click ('left', 'right', 'middle')
            clicks: Number of clicks (1 for single, 2 for double)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            valid_buttons = ['left', 'right', 'middle']
            if button not in valid_buttons:
                button = 'left'
            
            pyautogui.click(button=button, clicks=clicks)
            return True
        except Exception as e:
            print(f"Error clicking mouse: {e}")
            return False
    
    def press_key(self, key_combination: str) -> bool:
        """
        Press a key or key combination.
        
        Args:
            key_combination: Key or combination (e.g., 'a', 'ctrl+c', 'alt+tab')
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Split by + for key combinations
            keys = [k.strip() for k in key_combination.split('+')]
            
            if len(keys) == 1:
                # Single key press
                pyautogui.press(keys[0])
            else:
                # Multiple key combination
                pyautogui.hotkey(*keys)
            
            return True
        except Exception as e:
            print(f"Error pressing key(s) {key_combination}: {e}")
            return False
    
    def type_text(self, text: str, interval: float = 0.05) -> bool:
        """
        Type text as if typing on keyboard.
        
        Args:
            text: Text to type
            interval: Interval between key presses (seconds)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            pyautogui.write(text, interval=interval)
            return True
        except Exception as e:
            print(f"Error typing text: {e}")
            return False
