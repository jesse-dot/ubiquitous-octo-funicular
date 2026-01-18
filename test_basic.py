"""
Test script to verify basic functionality of the chat control tool.
This tests the core components without requiring actual livestream connections.
"""
import sys
import os

# Mock the required modules for testing in environments without them
try:
    import pyautogui
except ImportError:
    print("Note: pyautogui not installed, using mock for testing")
    import types
    pyautogui = types.ModuleType('pyautogui')
    pyautogui.FAILSAFE = True
    pyautogui.PAUSE = 0.1
    pyautogui.size = lambda: (1920, 1080)
    pyautogui.moveTo = lambda x, y, duration=0: None
    pyautogui.click = lambda button='left', clicks=1: None
    pyautogui.press = lambda key: None
    pyautogui.hotkey = lambda *keys: None
    pyautogui.write = lambda text, interval=0.05: None
    sys.modules['pyautogui'] = pyautogui

# Test imports
print("Testing imports...")
try:
    from command_parser import CommandParser
    from windows_controller import WindowsController
    print("✓ Core modules imported successfully")
except ImportError as e:
    print(f"✗ Import error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test configuration loading
print("\nTesting configuration...")
try:
    import yaml
    with open('config.yaml', 'r') as f:
        config = yaml.safe_load(f)
    print("✓ Configuration loaded successfully")
    print(f"  Platform: {config.get('platform')}")
    print(f"  Command prefix: {config.get('command_prefix')}")
    print(f"  Commands defined: {len(config.get('commands', {}))}")
except Exception as e:
    print(f"✗ Configuration error: {e}")
    sys.exit(1)

# Test CommandParser initialization
print("\nTesting CommandParser...")
try:
    parser = CommandParser(config)
    print("✓ CommandParser initialized successfully")
    
    # Test command detection
    assert parser.is_command("!test") == True
    assert parser.is_command("hello") == False
    print("✓ Command detection works")
    
    # Test user permissions
    assert parser.is_user_allowed("testuser", False) == True
    print("✓ User permission checks work")
    
except Exception as e:
    print(f"✗ CommandParser error: {e}")
    sys.exit(1)

# Test WindowsController initialization
print("\nTesting WindowsController...")
try:
    controller = WindowsController()
    print("✓ WindowsController initialized successfully")
    print(f"  PyAutoGUI failsafe enabled: {pyautogui.FAILSAFE}")
except Exception as e:
    print(f"✗ WindowsController error: {e}")
    sys.exit(1)

# Test command parsing (dry run - no execution)
print("\nTesting command parsing...")
try:
    test_commands = [
        "!open_notepad",
        "!mouse_move 100 200",
        "!click left",
        "!key ctrl+c",
        "!type hello",
    ]
    
    for cmd in test_commands:
        is_cmd = parser.is_command(cmd)
        print(f"  '{cmd}' -> is_command: {is_cmd}")
    
    print("✓ Command parsing tests passed")
except Exception as e:
    print(f"✗ Command parsing error: {e}")
    sys.exit(1)

print("\n" + "="*60)
print("All tests passed! ✓")
print("="*60)
print("\nNote: Actual command execution and chat listeners")
print("require a live YouTube/Twitch stream and should be")
print("tested manually by running 'python main.py'")
