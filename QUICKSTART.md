# Quick Start Guide

Get your chat control tool running in 5 minutes!

## Prerequisites

- Windows 10 or 11
- Python 3.7+ installed
- A YouTube livestream or Twitch channel

## Installation Steps

### 1. Install Python Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `pyautogui` - For Windows automation
- `pytchat` - For YouTube chat
- `twitchio` - For Twitch chat
- `pyyaml` - For configuration

### 2. Configure Your Stream

#### For YouTube:

1. Start your YouTube livestream
2. Get the video ID from your stream URL
   - URL: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
   - Video ID: `dQw4w9WgXcQ`
3. Edit `config.yaml`:
   ```yaml
   platform: youtube
   youtube:
     video_id: "YOUR_VIDEO_ID_HERE"
   ```

#### For Twitch:

1. Edit `config.yaml`:
   ```yaml
   platform: twitch
   twitch:
     channel: "your_channel_name"
   ```

### 3. Customize Commands (Optional)

Edit `config.yaml` to add or modify commands. See `config.example.yaml` for examples.

### 4. Run the Tool

```bash
python main.py
```

You should see:
```
============================================================
Chat Control Tool - Livestream Chat to Windows Controller
============================================================

Connected to YouTube chat for video: dQw4w9WgXcQ
Listening for commands...
```

## Testing Commands

Have someone (or yourself in another window) type these in your stream chat:

- `!open_notepad` - Opens Notepad
- `!mouse_move 500 300` - Moves mouse to (500, 300)
- `!mouse_click left` - Clicks left mouse button
- `!press_key a` - Presses the 'a' key
- `!type_text Hello!` - Types "Hello!"

## Safety Tips

### First Time Setup

1. **Test in a test stream first** - Don't use on your main channel until you've tested
2. **Enable moderator-only mode** - Set `require_moderator: true` in config
3. **Use command cooldown** - Prevents spam (enabled by default)
4. **Test all commands** - Make sure they do what you expect

### Security Settings

```yaml
security:
  require_moderator: true   # Only mods can control
  enable_cooldown: true     # Prevent spam
  cooldown_seconds: 2       # Wait time between commands
```

### Allowed Users (Whitelist)

```yaml
allowed_users:
  - "trusted_friend_1"
  - "trusted_friend_2"
```

## Common Issues

### "No module named 'pyautogui'"
**Solution**: Run `pip install -r requirements.txt`

### "YouTube video_id not configured"
**Solution**: Add your video ID to `config.yaml`

### Commands not working
**Checklist**:
- ✓ Is the stream live?
- ✓ Is the video ID / channel name correct?
- ✓ Are you using the correct command prefix (default: `!`)?
- ✓ Is the user allowed? (check `allowed_users` and `require_moderator`)
- ✓ Is cooldown active? (wait a few seconds)

### Mouse not moving / Keys not pressing
**Solution**: Make sure pyautogui is installed correctly and you're on Windows

## Advanced Usage

### Custom Hotkeys

```yaml
commands:
  screenshot:
    action: "key_press"
    # Usage: !press_key win+printscreen
```

### Opening Custom Programs

```yaml
commands:
  myapp:
    action: "open"
    program: "C:\\Path\\To\\Your\\App.exe"
```

### Multi-Key Combinations

In chat:
- `!press_key ctrl+c` - Copy
- `!press_key ctrl+v` - Paste
- `!press_key alt+tab` - Switch window
- `!press_key ctrl+alt+delete` - Security screen

## Getting Help

1. Check the full README.md for detailed documentation
2. Review config.example.yaml for configuration examples
3. Run test_basic.py to verify your installation:
   ```bash
   python test_basic.py
   ```

## Next Steps

- Customize your commands in `config.yaml`
- Set up security settings for public streams
- Test with friends before going live
- Have fun with your chat-controlled stream!

---

**Remember**: This tool gives others control of your computer. Always use appropriate security settings and only enable it when streaming!
