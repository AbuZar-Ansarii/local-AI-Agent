import subprocess
import json
import logging

logger = logging.getLogger(__name__)

def run_termux_cmd(cmd_list):
    try:
        result = subprocess.run(cmd_list, capture_output=True, text=True)
        if result.returncode != 0:
            logger.error(f"Termux API error: {' '.join(cmd_list)} - {result.stderr}")
            return f"Error: {result.stderr}"
        return result.stdout.strip()
    except Exception as e:
        logger.error(f"Failed to run Termux API: {str(e)}")
        return f"Error: {str(e)}"

def get_battery():
    """Get device battery status"""
    out = run_termux_cmd(["termux-battery-status"])
    if out.startswith("Error"): return out
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out

def get_notifications():
    """Get active notifications"""
    out = run_termux_cmd(["termux-notification-list"])
    if out.startswith("Error"): return out
    try:
        return json.loads(out)
    except json.JSONDecodeError:
        return out

def toggle_wifi(enable: bool):
    """Enable or disable WiFi"""
    cmd = "true" if enable else "false"
    return run_termux_cmd(["termux-wifi-enable", cmd])

def set_brightness(level: int):
    """Set screen brightness (0-255)"""
    level = max(0, min(255, int(level)))
    return run_termux_cmd(["termux-brightness", str(level)])

def media_play_pause():
    """Play or pause media"""
    return run_termux_cmd(["termux-media-player", "play"])

def media_next():
    return run_termux_cmd(["termux-media-player", "next"])

def media_prev():
    return run_termux_cmd(["termux-media-player", "prev"])
