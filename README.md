# Chat Control Tool

A tool that allows YouTube or Twitch livestream chat to control a Windows device using chat commands. Control your computer through chat messages with support for opening programs, mouse control, keyboard input, and multi-key press combinations.

## Features

- 🎮 **Dual Platform Support**: Works with both YouTube and Twitch livestreams
- 🖱️ **Mouse Control**: Move cursor and click (left, right, middle buttons)
- ⌨️ **Keyboard Input**: Press keys and key combinations (e.g., Ctrl+C, Alt+Tab)
- 🚀 **Program Launcher**: Open applications via chat commands
- 🔒 **Security Features**: Moderator-only mode, user whitelisting, and command cooldowns
- ⚙️ **Customizable Commands**: Easy YAML configuration for command setup

## Requirements

- Windows operating system
- Python 3.7 or higher
- Active YouTube livestream or Twitch channel

## Installation

1. Clone this repository:
```bash
git clone https://github.com/jesse-dot/ubiquitous-octo-funicular.git
cd ubiquitous-octo-funicular
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

1. Copy or edit `config.yaml` to configure your settings:
   - Set `platform` to either `youtube` or `twitch`
   - For YouTube: Add your livestream's `video_id`
   - For Twitch: Add your `channel` name
   - Customize commands and security settings

### Example Configuration

```yaml
platform: youtube

youtube:
  video_id: "dQw4w9WgXcQ"  # Your YouTube live video ID

twitch:
  channel: "your_channel_name"
  token: ""  # Optional OAuth token

command_prefix: "!"

security:
  require_moderator: false
  enable_cooldown: true
  cooldown_seconds: 2

commands:
  open_notepad:
    action: "open"
    program: "notepad.exe"
    
  mouse_move:
    action: "mouse_move"
    # Usage: !mouse_move 500 300
```

## Usage

1. Start the application:
```bash
python main.py
```

2. The tool will connect to your configured platform and start listening for commands.

3. Chat users can now use commands in the chat:
   - `!open_notepad` - Opens Notepad
   - `!mouse_move 500 300` - Moves mouse to coordinates (500, 300)
   - `!mouse_click left` - Performs a left mouse click
   - `!press_key ctrl+c` - Presses Ctrl+C
   - `!type_text Hello World` - Types "Hello World"

## Available Command Actions

### Program Control
- **Action**: `open`
- **Config**: Specify `program` path
- **Example**: `!open_notepad` opens Notepad

### Mouse Control
- **Action**: `mouse_move`
- **Usage**: `!mouse_move X Y`
- **Example**: `!mouse_move 500 300` moves cursor to (500, 300)

- **Action**: `mouse_click`
- **Usage**: `!mouse_click [left|right|middle]`
- **Example**: `!mouse_click right` performs right-click

- **Action**: `mouse_doubleclick`
- **Usage**: `!mouse_doubleclick`
- **Example**: Performs a double-click at current position

### Keyboard Control
- **Action**: `key_press`
- **Usage**: `!press_key <key_combination>`
- **Examples**:
  - `!press_key a` - Presses 'a' key
  - `!press_key ctrl+c` - Presses Ctrl+C
  - `!press_key alt+tab` - Presses Alt+Tab

- **Action**: `type`
- **Usage**: `!type_text <text>`
- **Example**: `!type_text Hello World` types the text

## Security Features

### Moderator-Only Mode
Set `require_moderator: true` to restrict commands to moderators only:
```yaml
security:
  require_moderator: true
```

### User Whitelist
Restrict commands to specific users:
```yaml
allowed_users:
  - "trusted_user1"
  - "trusted_user2"
```

### Command Cooldown
Prevent command spam with cooldowns:
```yaml
security:
  enable_cooldown: true
  cooldown_seconds: 2
```

## Adding Custom Commands

Edit `config.yaml` to add your own commands:

```yaml
commands:
  my_custom_command:
    action: "open"
    program: "C:\\Path\\To\\Your\\Program.exe"
    
  jump:
    action: "key_press"
    # Usage: !jump (will need args in chat like !press_key space)
```

## Safety Features

- **PyAutoGUI Failsafe**: Move mouse to screen corner to abort
- **Coordinate Clamping**: Mouse movements are bounded to screen dimensions
- **Cooldown System**: Prevents command flooding
- **User Permissions**: Control who can execute commands

## Troubleshooting

### YouTube Connection Issues
- Ensure the `video_id` is correct and the stream is live
- Check your internet connection

### Twitch Connection Issues
- Verify the channel name is correct
- For authenticated features, provide a valid OAuth token

### Commands Not Working
- Check that the command prefix matches (default: `!`)
- Verify the command name exists in `config.yaml`
- Check security settings (moderator-only, allowed users)
- Ensure cooldown has elapsed

### Permission Errors
- Run Python with appropriate permissions for system control
- Some programs may require administrator privileges

## Technical Details

### Architecture
- `main.py`: Application entry point and orchestration
- `command_parser.py`: Command parsing and execution logic
- `windows_controller.py`: Windows control operations (PyAutoGUI)
- `youtube_listener.py`: YouTube chat integration (pytchat)
- `twitch_listener.py`: Twitch chat integration (TwitchIO)

### Dependencies
- `pyautogui`: Windows automation
- `pytchat`: YouTube Live Chat API
- `twitchio`: Twitch IRC/API integration
- `pyyaml`: Configuration file parsing

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues.

## License

This project is open source and available for educational and personal use.

## Disclaimer

⚠️ **Important**: This tool provides external control over your computer. Use with caution:
- Only use on systems you own or have permission to control
- Be careful when sharing livestreams using this tool
- Review all commands in your configuration
- Consider security implications before making streams public
- The authors are not responsible for misuse of this software

## Example Session

```
================================================================
Chat Control Tool - Livestream Chat to Windows Controller
================================================================

Connected to YouTube chat for video: dQw4w9WgXcQ
Listening for commands...

[user123]: !open_notepad
Executing command: open_notepad (action: open) by user123
  -> Command open_notepad executed successfully

[moderator]: !mouse_move 500 300
Executing command: mouse_move (action: mouse_move) by moderator
  -> Command mouse_move executed successfully

[user456]: !press_key ctrl+c
Executing command: press_key (action: key_press) by user456
  -> Command press_key executed successfully
```