import subprocess
import logging
from config.settings import SHIZUKU_ENABLED

logger = logging.getLogger(__name__)

class ShizukuController:
    def __init__(self):
        self.enabled = SHIZUKU_ENABLED
        self.rish_path = "/data/local/tmp/rish"  # Standard path for Shizuku's rish

    def is_available(self):
        if not self.enabled:
            return False
        # Check if rish is accessible and working
        out = self.execute("echo 'shizuku_ready'")
        return "shizuku_ready" in out

    def execute(self, cmd: str):
        """Execute a shell command via Shizuku (rish)"""
        if not self.enabled:
            return "Error: Shizuku is disabled in settings."
        
        # rish is the Shizuku bridge script
        shizuku_cmd = f"sh {self.rish_path} -c '{cmd}'"
        
        try:
            result = subprocess.run(shizuku_cmd, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                logger.error(f"Shizuku error: {result.stderr}")
                return f"Error: {result.stderr}"
            return result.stdout.strip()
        except Exception as e:
            logger.error(f"Shizuku execution failed: {str(e)}")
            return f"Exception: {str(e)}"

    def take_screenshot(self, filepath: str):
        """Take a screenshot using Shizuku and screencap"""
        return self.execute(f"screencap -p {filepath}")
        
    def input_keyevent(self, keycode: int):
        """Send a keyevent"""
        return self.execute(f"input keyevent {keycode}")
        
    def input_text(self, text: str):
        """Input text"""
        # escape spaces
        escaped_text = text.replace(" ", "%s")
        return self.execute(f"input text {escaped_text}")

shizuku = ShizukuController()
